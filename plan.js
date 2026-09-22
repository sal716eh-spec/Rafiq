/* plan.js — subscriptions. There is no free tier; both plans have a 7-day trial.

     Essentials  £6.99/month or £49.99/year
       the whole course, all practice, audio and review, and
       ESSENTIALS_CHECKS smart checks a day (a judgment by the TypeSafe Worker);
       past that, checks fall back to ordinary matching.
     Complete    £11.99/month or £79.99/year
       everything in Essentials, plus unlimited smart checks, the
       conversation partner, speaking feedback and the mistake focus.

   BETA = true gives everyone Complete and never asks anyone to subscribe.
   Turn it off only once payments are live and paying accounts carry their
   plan (see "Taking payments" in README.md). Until then tier() also reads a
   'rafiq_plan' flag ('essentials' | 'complete'), for testing. */
(function(){
  const BETA = true;
  const ESSENTIALS_CHECKS = 25;
  const PRICES = {
    essentials: { monthly:'£6.99',  yearly:'£49.99' },
    complete:   { monthly:'£11.99', yearly:'£79.99' },
  };
  const KEY = 'rafiq_checks';
  const today = () => new Date().toISOString().slice(0,10);
  const read = () => { try{ const r=JSON.parse(localStorage.getItem(KEY)||'{}'); return r.day===today() ? r : {day:today(), n:0}; }catch(_){ return {day:today(), n:0}; } };

  /* 'complete' | 'essentials' | null (not subscribed) */
  function tier(){
    if(BETA) return 'complete';
    try{ const t=localStorage.getItem('rafiq_plan'); return t==='complete'||t==='essentials' ? t : null; }catch(_){ return null; }
  }
  const isComplete = () => tier()==='complete';
  const checksLeft = () => isComplete() ? Infinity : tier() ? Math.max(0, ESSENTIALS_CHECKS - read().n) : 0;

  /* Called by judge.js before each smart check. false = no check this time. */
  function useCheck(){
    if(isComplete()) return true;
    if(!tier()) return false;
    const r = read();
    if(r.n >= ESSENTIALS_CHECKS){ notice(); return false; }
    r.n++; try{ localStorage.setItem(KEY, JSON.stringify(r)); }catch(_){}
    return true;
  }

  /* App pages call this: without a plan, go to the pricing page. Never
     during the beta, and never on the landing, sign-in or settings pages. */
  function requirePlan(){
    if(tier()) return true;
    location.href = 'index.html#pricing';
    return false;
  }

  let shown = false;
  function notice(){
    if(shown || typeof document==='undefined') return; shown = true;
    const d = document.createElement('div');
    d.setAttribute('role','status');
    d.style.cssText = 'position:fixed;left:12px;right:12px;bottom:calc(76px + env(safe-area-inset-bottom));z-index:300;'+
      'background:var(--card);border:1px solid var(--gold);border-radius:12px;padding:12px 14px;font-size:14px;'+
      'box-shadow:0 8px 24px -10px rgba(0,0,0,.35);max-width:520px;margin:0 auto';
    d.innerHTML = `You've used today's ${ESSENTIALS_CHECKS} smart checks, so answers are now matched word by word. `+
      `<a href="index.html#pricing">Rafiq Complete</a> gives unlimited checking. <button type="button" style="float:right;border:0;background:none;font-size:16px;cursor:pointer" aria-label="Close">✕</button>`;
    d.querySelector('button').onclick = () => d.remove();
    document.body.appendChild(d);
  }
  window.RafiqPlan = { BETA, ESSENTIALS_CHECKS, PRICES, tier, isComplete, checksLeft, useCheck, requirePlan };
})();
