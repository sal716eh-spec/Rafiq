/* rafiq-judge — a Cloudflare Worker that holds the TypeSafe key and answers
   exactly two questions for the site:

     POST {kind:'vocab',   arabic, glosses:[...], answer}  → {ok}
     POST {kind:'produce', english, model, answer}         → {ok, err}

   ok is TypeSafe's probability (0–1) that the learner's answer is right; the
   page decides what to do with it. The questions are built here, not in the
   browser, so the endpoint can't be used as a general-purpose TypeSafe proxy.
   Question wording comes from tools/typesafe-exp, where it was measured. */

const API = 'https://api.typesafe.ai/v1/systemone';
const ORIGINS = [
  'https://rafiq-arabic.com',
  'https://www.rafiq-arabic.com',
  'https://sal716eh-spec.github.io',
];
const MAX = 300;   // characters per field; every real prompt is far shorter

const VOCAB_Q = {
  ok: {
    type: 'noul',
    instructions: {
      task: 'A beginner learning Arabic was shown `arabic` and typed its English meaning as `answer`. ' +
            'The textbook glosses are in `glosses`. Should a fair teacher mark it correct?',
      accept: ['a synonym or near-synonym with the same meaning',
               "the same word without 'to', 'a' or 'the', or in another form (plural, past tense)",
               'a small spelling slip where the intended English word is obvious',
               'leaving out a gender note such as (m) or (f)'],
      reject: ['a different word, even a related one (bedroom for room)',
               'an opposite or a word from the same topic with another meaning'],
    },
    criteria: { true: 'Mark correct', false: 'Mark wrong' },
  },
};

const PRODUCE_Q = {
  ok: {
    type: 'noul',
    instructions: {
      task: 'A beginner was asked to say `english_prompt` in Modern Standard Arabic and wrote ' +
            "`learner_answer`. `model_answer` is one correct answer. Is the learner's answer correct?",
      ignore: ['missing vowel marks (harakat) and case endings that are not written',
               'hamza forms, ة written as ه, ى as ي, spacing, punctuation',
               'synonyms and any word order Arabic allows'],
      not_ignore: ['wrong gender, person, number or tense',
                   'a changed fact, word or meaning', 'missing words', 'misspelled words'],
    },
    criteria: { true: 'Correct answer', false: 'Contains an error' },
  },
  err: {
    type: 'choice',
    instructions: 'What is the main problem with `learner_answer` as an Arabic rendering of ' +
                  '`english_prompt`, compared with `model_answer`?',
    criteria: {
      none: 'Correct: same meaning as the model answer and grammatical. Missing vowel marks, ' +
            'hamza spelling, ة/ه and attached و are fine; so are synonyms and word orders Arabic allows.',
      gender_agreement: 'A word has the wrong gender (masculine/feminine) for what it refers to',
      wrong_person_or_tense: 'A verb or pronoun is in the wrong person, number or tense',
      wrong_word: 'One word or detail is replaced by a different one, changing a fact',
      different_meaning: 'The words are rearranged or changed so the sentence says something else',
      missing_word: 'Needed words are left out, so the sentence is incomplete',
      spelling: 'A word is misspelled so it is a different or non-existent word',
      grammar_other: 'Some other grammatical error',
    },
  },
};

const str = v => typeof v === 'string' && v.trim() !== '' && v.length <= MAX;

function cors(origin) {
  const h = { 'Vary': 'Origin' };
  if (ORIGINS.includes(origin)) {
    h['Access-Control-Allow-Origin'] = origin;
    h['Access-Control-Allow-Methods'] = 'POST, OPTIONS';
    h['Access-Control-Allow-Headers'] = 'Content-Type';
    h['Access-Control-Max-Age'] = '86400';
  }
  return h;
}

function reply(body, status, origin) {
  return new Response(JSON.stringify(body), {
    status, headers: { 'Content-Type': 'application/json', ...cors(origin) },
  });
}

export default {
  async fetch(req, env) {
    const origin = req.headers.get('Origin') || '';
    if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors(origin) });
    if (req.method !== 'POST') return reply({ error: 'POST only' }, 405, origin);
    if (!ORIGINS.includes(origin)) return reply({ error: 'origin not allowed' }, 403, origin);

    let b;
    try { b = await req.json(); } catch { return reply({ error: 'bad json' }, 400, origin); }

    let state, questions;
    if (b.kind === 'vocab' && str(b.arabic) && str(b.answer) &&
        Array.isArray(b.glosses) && b.glosses.length > 0 && b.glosses.length <= 8 && b.glosses.every(str)) {
      state = { arabic: b.arabic, glosses: b.glosses, answer: b.answer };
      questions = VOCAB_Q;
    } else if (b.kind === 'produce' && str(b.english) && str(b.model) && str(b.answer)) {
      state = { english_prompt: b.english, model_answer: b.model, learner_answer: b.answer };
      questions = PRODUCE_Q;
    } else {
      return reply({ error: 'bad request' }, 400, origin);
    }

    const r = await fetch(API, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${env.TYPESAFE_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ state, model: 'jev-latest', questions }),
    });
    if (!r.ok) return reply({ error: 'upstream ' + r.status }, 502, origin);
    const a = (await r.json()).answers;
    const out = { ok: a.ok.noul };
    if (a.err) out.err = a.err.choice;
    return reply(out, 200, origin);
  },
};
