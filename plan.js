/* plan.js — Free and Plus.

   Free: the whole course, plus FREE_CHECKS smart checks a day (a judgment by
   the TypeSafe Worker). Past that, checks fall back to ordinary matching.
   Plus (£4.99/month or £34.99/year): unlimited smart checks and the
   conversation partner.

   BETA = true gives everyone Plus. Turn it off only once payments are live
   and paying accounts are marked Plus (see "Taking payments" in README.md);
   until then isPlus() also honours a 'rafiq_plus' flag for testing. */
(function(){
  const BETA = true;
  const FREE_CHECKS = 10;
  const PRICES = { monthly:'£4.99', yearly:'£34.99' };
  const KEY = 'rafiq_checks';
  const today = () => new Date().toISOString().slice(0,10);
  const read = () => { try{ const r=JSON.parse(localStorage.getItem(KEY)||'{}'); return r.day===today() ? r : {day:today(), n:0}; }catch(_){ return {day:today(), n:0}; } };

  function isPlus(){
    if(BETA) return true;
    try{ return localStorage.getItem('rafiq_plus')==='1'; }catch(_){ return false; }
  }
  const checksLeft = () => isPlus() ? Infinity : Math.max(0, FREE_CHECKS - read().n);
  /* Called by judge.js before each smart check. false = over today's limit. */
  function useCheck(){
    if(isPlus()) return true;
    const r = read();
    if(r.n >= FREE_CHECKS){ notice(); return false; }
    r.n++; try{ localStorage.setItem(KEY, JSON.stringify(r)); }catch(_){}
    return true;
  }
  let shown = false;
  function notice(){
    if(shown || typeof document==='undefined') return; shown = true;
    const d = document.createElement('div');
    d.setAttribute('role','status');
    d.style.cssText = 'position:fixed;left:12px;right:12px;bottom:calc(76px + env(safe-area-inset-bottom));z-index:300;'+
      'background:var(--card);border:1px solid var(--gold);border-radius:12px;padding:12px 14px;font-size:14px;'+
      'box-shadow:0 8px 24px -10px rgba(0,0,0,.35);max-width:520px;margin:0 auto';
    d.innerHTML = `You've used today's ${FREE_CHECKS} smart checks, so answers are now matched word by word. `+
      `<a href="index.html#pricing">Rafiq Plus</a> gives unlimited checking. <button type="button" style="float:right;border:0;background:none;font-size:16px;cursor:pointer" aria-label="Close">✕</button>`;
    d.querySelector('button').onclick = () => d.remove();
    document.body.appendChild(d);
  }
  window.RafiqPlan = { BETA, FREE_CHECKS, PRICES, isPlus, checksLeft, useCheck };
})();
