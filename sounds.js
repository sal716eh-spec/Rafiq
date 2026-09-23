/* sounds.js — a short sound when an answer is checked: a warm wooden tock-tick
   for correct, a soft muted wooden thud for wrong (chosen over chimes and
   buzzers: clear, pleasant to hear dozens of times, and not music).
   RafiqSound.answer(true|false). Off in Settings → Audio → Answer sounds
   (localStorage 'rafiq_sounds' = 'off'). Decoded once and played through Web
   Audio so it lands on the same frame as the colour change. */
(function(){
  const FILES={ok:'sounds/correct.mp3', no:'sounds/wrong.mp3'}, VOL={ok:0.7, no:0.6};
  const on=()=>{ try{ return localStorage.getItem('rafiq_sounds')!=='off'; }catch(_){ return true; } };
  let ctx=null; const buf={}, els={};
  function load(){
    if(ctx||!window.AudioContext&&!window.webkitAudioContext) return;
    try{ ctx=new (window.AudioContext||window.webkitAudioContext)(); }catch(_){ ctx=null; return; }
    Object.entries(FILES).forEach(([k,u])=>fetch(u).then(r=>r.arrayBuffer()).then(a=>ctx.decodeAudioData(a)).then(b=>{buf[k]=b;}).catch(()=>{}));
  }
  function play(k){
    if(!on()) return;
    load();
    if(ctx&&buf[k]){
      if(ctx.state==='suspended') ctx.resume();
      const s=ctx.createBufferSource(), g=ctx.createGain(); g.gain.value=VOL[k];
      s.buffer=buf[k]; s.connect(g).connect(ctx.destination); s.start(); return;
    }
    // before the buffers are ready (or without Web Audio): a plain audio element
    const a=els[k]||(els[k]=new Audio(FILES[k])); a.volume=VOL[k]; try{ a.currentTime=0; a.play().catch(()=>{}); }catch(_){}
  }
  // unlock and decode on the first touch, so the first answer already sounds right
  addEventListener('pointerdown',load,{once:true,capture:true});
  window.RafiqSound={ answer:ok=>play(ok?'ok':'no'), enabled:on,
    set:v=>{ try{ localStorage.setItem('rafiq_sounds', v?'on':'off'); }catch(_){} } };
})();
