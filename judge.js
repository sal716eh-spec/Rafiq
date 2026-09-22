/* judge.js — asks the rafiq-judge Worker (worker/) whether a learner's answer
   is right, when a fixed string comparison can't tell.

   Every call resolves to null when the judge is unavailable — not deployed,
   offline, slow, or erroring — and the page falls back to its own matching.
   Thresholds come from tools/typesafe-exp; re-check them there if the
   questions in the Worker change. */
(function(){
  // Paste the Worker's URL here once it's deployed; empty means "judge off".
  const ENDPOINT = 'https://rafiq-judge.luq09.workers.dev';
  const TIMEOUT_MS = 3000;

  const ERR = {
    gender_agreement:      'A word has the wrong gender (masculine / feminine).',
    wrong_person_or_tense: 'A verb or pronoun is in the wrong person or tense.',
    wrong_word:            'One word or detail has been swapped for another.',
    different_meaning:     'The sentence now says something different.',
    missing_word:          'Something is missing.',
    spelling:              'A word is misspelled.',
    grammar_other:         'There is a grammar slip.',
    not_done:              "The change asked for hasn't been made yet.",
  };

  /* → the Worker's reply, or null. `need` lists the numeric fields this kind
     of check must return; anything else counts as unavailable. */
  async function post(body, need){
    if(!ENDPOINT || typeof fetch!=='function') return null;
    const ctl = typeof AbortController==='function' ? new AbortController() : null;
    const t = ctl && setTimeout(()=>ctl.abort(), TIMEOUT_MS);
    try{
      const r = await fetch(ENDPOINT, {method:'POST', headers:{'Content-Type':'application/json'},
                                       body:JSON.stringify(body), signal:ctl&&ctl.signal});
      if(!r.ok) return null;
      const j = await r.json();
      return j && need.every(k=>typeof j[k]==='number') ? j : null;
    }catch(e){ return null; }
    finally{ if(t) clearTimeout(t); }
  }

  /* Typed English for an Arabic word → true / false, or null. */
  async function vocab(arabic, en, typed){
    const glosses = (en||'').split('/').map(s=>s.trim()).filter(Boolean);
    const j = await post({kind:'vocab', arabic, glosses, answer:typed}, ['ok']);
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
    const j = await post({kind:'produce', english, model, answer:said}, ['ok']);
    if(!j) return null;
    const verdict = j.ok>=0.8 ? 'right' : j.ok>=0.5 ? 'close' : 'wrong';
    return {verdict, why: verdict==='wrong' ? (ERR[j.err]||'Compare it with the answer.') : ''};
  }

  /* Build-it, when the tiles are in a different order from the book's →
     true (another valid order) / false / null. Needs both the meaning and a
     separate word-order judgment: on its own, meaning let a scrambled order
     through at 0.87 (tools/typesafe-exp/round2b.py). Every valid reorder
     scored order ≥ 0.43, every wrong one ≤ 0.23. */
  async function build(english, model, placed){
    const j = await post({kind:'build', english, model, answer:placed.replace(/^[\s،,]+/,'')}, ['ok','order']);
    return j ? j.ok>=0.8 && j.order>=0.3 : null;
  }

  /* Transform and Fix-it: a typed rewrite of `original` → {verdict, why} or
     null, like produce(). Two judgments must agree: 'ok' alone passed كم حصص
     at 0.89; the 'changes' question catches it (0.08). Known miss: a half-done
     tense change (one verb of two) still passes. */
  async function rewrite(task, original, model, said){
    const j = await post({kind:'rewrite', task, original, model, answer:said}, ['ok','changes']);
    if(!j) return null;
    const p = Math.min(j.ok, j.changes);
    const verdict = p>=0.8 ? 'right' : p>=0.5 ? 'close' : 'wrong';
    return {verdict, why: verdict==='wrong' ? (ERR[j.err]||'Compare it with the answer.') : ''};
  }

  /* Free speaking: an open answer to a prompt → {done:0|1|2, grammarOk, why}
     or null. done: 0 off-task, 1 partly, 2 fully (17/17 right in testing).
     Grammar is flagged below 0.7: correct answers scored 0.73+, answers with
     a slip 0.60 or less. */
  async function prompt(task, model, said){
    const j = await post({kind:'prompt', task, model, answer:said}, ['done','grammar']);
    if(!j) return null;
    const done = j.done<0.67 ? 0 : j.done<1.34 ? 1 : 2;
    const grammarOk = j.grammar>=0.7;
    return {done, grammarOk, why: grammarOk ? '' : (ERR[j.err]||ERR.grammar_other)};
  }

  window.RafiqJudge = { on: !!ENDPOINT, vocab, produce, build, rewrite, prompt };
})();
