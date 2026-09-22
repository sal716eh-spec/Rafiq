/* judge.js — asks the rafiq-judge Worker (worker/) whether a learner's answer
   is right, when a fixed string comparison can't tell.

   Every call resolves to null when the judge is unavailable — not deployed,
   offline, slow, or erroring — and the page falls back to its own matching.
   Thresholds come from tools/typesafe-exp; re-check them there if the
   questions in the Worker change. */
(function(){
  // Paste the Worker's URL here once it's deployed; empty means "judge off".
  const ENDPOINT = '';
  const TIMEOUT_MS = 3000;

  const ERR = {
    gender_agreement:      'A word has the wrong gender (masculine / feminine).',
    wrong_person_or_tense: 'A verb or pronoun is in the wrong person or tense.',
    wrong_word:            'One word or detail has been swapped for another.',
    different_meaning:     'The sentence now says something different.',
    missing_word:          'Something is missing.',
    spelling:              'A word is misspelled.',
    grammar_other:         'There is a grammar slip.',
  };

  async function post(body){
    if(!ENDPOINT || typeof fetch!=='function') return null;
    const ctl = typeof AbortController==='function' ? new AbortController() : null;
    const t = ctl && setTimeout(()=>ctl.abort(), TIMEOUT_MS);
    try{
      const r = await fetch(ENDPOINT, {method:'POST', headers:{'Content-Type':'application/json'},
                                       body:JSON.stringify(body), signal:ctl&&ctl.signal});
      if(!r.ok) return null;
      const j = await r.json();
      return typeof j.ok==='number' ? j : null;
    }catch(e){ return null; }
    finally{ if(t) clearTimeout(t); }
  }

  /* Typed English for an Arabic word → true / false, or null. */
  async function vocab(arabic, en, typed){
    const glosses = (en||'').split('/').map(s=>s.trim()).filter(Boolean);
    const j = await post({kind:'vocab', arabic, glosses, answer:typed});
    return j ? j.ok>=0.5 : null;
  }

  /* English prompt → learner's Arabic. Resolves to
     {verdict:'right'|'close'|'wrong', why} or null.
     'close' is the band where the judge is unsure (measured: a gender slip
     at 0.70, a misspelling near 0.5, the lowest correct answer at 0.71):
     tell the learner to compare with the model answer rather than call it.
     Correct answers often land at 0.85–0.90, so the 'right' line sits at
     0.8; the one known miss above it is a wrong plural (كم غرف, 0.82). */
  async function produce(english, model, said){
    const j = await post({kind:'produce', english, model, answer:said});
    if(!j) return null;
    const verdict = j.ok>=0.8 ? 'right' : j.ok>=0.5 ? 'close' : 'wrong';
    return {verdict, why: verdict==='wrong' ? (ERR[j.err]||'') : ''};
  }

  window.RafiqJudge = { on: !!ENDPOINT, vocab, produce };
})();
