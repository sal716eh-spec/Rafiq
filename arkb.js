/* arkb.js — a small on-screen Arabic keyboard for any input.ar-in or textarea.ar-in on the page,
   including ones that don't exist yet (every drill card is built by JS after
   this script loads, so it can't just scan the DOM once at startup).

   Works by listening for focus on the whole document rather than attaching to
   each input individually — one listener covers every input this page will
   ever create. Click or tap both fire the same 'click' event, so desktop and
   mobile need no separate handling.

   On touch screens only one keyboard opens: this one (the default; the
   phone's keyboard is held back with inputmode="none") or the phone's own,
   if the learner has picked it. The choice is kept per device in
   localStorage 'rafiq_kb' ('app' | 'phone'): the 🌐 key switches to the
   phone keyboard, the ⌨ button beside a focused box switches back, and
   Settings has the same choice. While this keyboard is open on a phone the
   page gets room at the bottom so the box and its buttons stay visible. */
(function(){
  const KB_KEY = 'rafiq_kb';
  const touch = () => window.matchMedia('(pointer:coarse)').matches;
  const phoneLayout = () => window.matchMedia('(max-width:860px)').matches;
  function mode(){ try{ return localStorage.getItem(KB_KEY)==='phone' ? 'phone' : 'app'; }catch(_){ return 'app'; } }
  function setMode(m){ try{ localStorage.setItem(KB_KEY, m); }catch(_){} }
  const isAr = el => !!(el && el.matches && el.matches('input.ar-in, textarea.ar-in'));
  // the phone keyboard stays shut while ours is in use
  function applyMode(el){
    if(!touch()) return;
    if(mode()==='app') el.setAttribute('inputmode','none'); else el.removeAttribute('inputmode');
  }
  const ROWS = [
    ['ا','ب','ت','ث','ج','ح','خ','د','ذ','ر'],
    ['ز','س','ش','ص','ض','ط','ظ','ع','غ','ف'],
    ['ق','ك','ل','م','ن','ه','و','ي','ء','ة'],
    ['أ','إ','آ','ئ','ؤ','ى','لا']
  ];
  /* Short vowels, sukoon, shadda and tanwin — the part hardest to reach on a
     phone's own Arabic keyboard, and everything in this app is fully vocalised. */
  const HARAKAT = [
    ['َ','فَتْحة'],['ُ','ضَمّة'],['ِ','كَسْرة'],['ْ','سُكون'],
    ['ّ','شَدّة'],['ً','تَنوين فتح'],['ٌ','تَنوين ضمّ'],['ٍ','تَنوين كسر']
  ];

  let panel=null, activeInput=null;

  function insert(input, text){
    const s=input.selectionStart ?? input.value.length;
    const e=input.selectionEnd ?? input.value.length;
    input.value = input.value.slice(0,s) + text + input.value.slice(e);
    const pos = s + text.length;
    input.setSelectionRange(pos,pos);
    input.dispatchEvent(new Event('input',{bubbles:true}));
    input.focus();
  }
  function backspace(input){
    const s=input.selectionStart ?? input.value.length;
    const e=input.selectionEnd ?? input.value.length;
    if(s===e && s>0) input.value = input.value.slice(0,s-1)+input.value.slice(s);
    else input.value = input.value.slice(0,s)+input.value.slice(e);
    const pos = s===e ? Math.max(0,s-1) : s;
    input.setSelectionRange(pos,pos);
    input.dispatchEvent(new Event('input',{bubbles:true}));
    input.focus();
  }

  function build(){
    const p=document.createElement('div');
    p.className='arkb';
    p.innerHTML =
      '<div class="arkb-rows"></div>'+
      '<div class="arkb-harakat"></div>'+
      '<div class="arkb-bottom">'+
        (touch() ? '<button type="button" class="arkb-key arkb-sw" data-act="phone" title="Use my phone\'s keyboard" aria-label="Use my phone\'s keyboard">🌐</button>' : '')+
        '<button type="button" class="arkb-key arkb-wide" data-act="space">مسافة</button>'+
        '<button type="button" class="arkb-key arkb-wide" data-act="back">⌫</button>'+
        '<button type="button" class="arkb-key arkb-wide" data-act="enter" aria-label="Enter">↵</button>'+
        '<button type="button" class="arkb-key arkb-wide" data-act="close">إغلاق</button>'+
      '</div>';
    const rowsEl=p.querySelector('.arkb-rows');
    ROWS.forEach(row=>{
      const r=document.createElement('div');r.className='arkb-row';
      row.forEach(ch=>{
        const b=document.createElement('button');b.type='button';b.className='arkb-key';b.textContent=ch;
        b.dataset.ch=ch;
        r.appendChild(b);
      });
      rowsEl.appendChild(r);
    });
    const hEl=p.querySelector('.arkb-harakat');
    HARAKAT.forEach(([ch,name])=>{
      const b=document.createElement('button');b.type='button';b.className='arkb-key arkb-hk';
      b.textContent='ا'+ch; b.title=name; b.dataset.ch=ch;
      hEl.appendChild(b);
    });
    p.addEventListener('mousedown', e=>e.preventDefault());   // don't steal focus from the input
    p.addEventListener('click', e=>{
      const b=e.target.closest('button'); if(!b || !activeInput) return;
      if(b.dataset.act==='space') insert(activeInput,' ');
      else if(b.dataset.act==='back') backspace(activeInput);
      else if(b.dataset.act==='close') hide();
      else if(b.dataset.act==='enter') enter(activeInput);
      else if(b.dataset.act==='phone') switchTo('phone', activeInput);
      else if(b.dataset.ch) insert(activeInput, b.dataset.ch);
    });
    document.body.appendChild(p);
    return p;
  }

  // ↵ acts like the Enter key: pages listen for it to check an answer
  function enter(input){
    const ev = new KeyboardEvent('keydown', {key:'Enter', code:'Enter', keyCode:13, which:13, bubbles:true, cancelable:true});
    input.dispatchEvent(ev);
    if(!ev.defaultPrevented && input.tagName==='TEXTAREA') insert(input, '\n');
  }

  // swap keyboards on the focused box: refocusing makes the phone apply the new inputmode
  function switchTo(m, input){
    setMode(m);
    if(m==='phone') hide();
    if(!input) return;
    applyMode(input);
    input.blur();
    setTimeout(()=>{ input.focus(); if(m==='app') show(input); }, 60);
  }

  function show(input){
    activeInput=input;
    hideToggle();
    if(!panel) panel=build();
    const wasOn = panel.classList.contains('on');
    panel.classList.add('on');
    positionAbove(input);
    makeRoom(input, wasOn);
  }
  function hide(){
    if(!panel || !panel.classList.contains('on')) return;
    panel.classList.remove('on');
    document.body.style.paddingBottom = savedPad;
  }
  function positionAbove(input){
    // fixed to the bottom of the viewport on phones (thumb reach); tucked
    // under the input on wider screens
    if(phoneLayout()) return;   // CSS handles mobile placement
    const r=input.getBoundingClientRect();
    panel.style.top=(window.scrollY+r.bottom+8)+'px';
    panel.style.left=Math.max(8,Math.min(r.left+window.scrollX, window.innerWidth-panel.offsetWidth-8))+'px';
  }
  // on phones the keyboard covers the bottom of the screen: add that much room
  // to the page and scroll the box (and the buttons on its row) above it
  let savedPad = '';
  function makeRoom(input, wasOn){
    if(!phoneLayout()) return;
    if(!wasOn) savedPad = document.body.style.paddingBottom;   // keep the page's own padding to restore
    const h = panel.offsetHeight;
    document.body.style.paddingBottom = (h + 16) + 'px';
    requestAnimationFrame(()=>{
      const row = input.parentElement || input;
      const bottom = Math.max(input.getBoundingClientRect().bottom, row.getBoundingClientRect().bottom);
      const top = window.innerHeight - h;
      if(bottom > top - 8) window.scrollBy(0, bottom - top + 16);
    });
  }

  // with the phone keyboard chosen: a small ⌨ button on the focused box brings ours back
  let toggle = null;
  function showToggle(input){
    if(!touch()) return;
    if(!toggle){
      toggle = document.createElement('button');
      toggle.type = 'button'; toggle.className = 'arkb-toggle';
      toggle.textContent = '⌨'; toggle.title = 'Use the Rafiq keyboard (with vowel marks)';
      toggle.setAttribute('aria-label', 'Use the Rafiq keyboard, with vowel marks');
      toggle.addEventListener('mousedown', e=>e.preventDefault());
      toggle.addEventListener('pointerdown', e=>e.preventDefault());
      toggle.addEventListener('click', ()=>{ const i = toggle._input; hideToggle(); switchTo('app', i); });
      document.body.appendChild(toggle);
    }
    toggle._input = input;
    const r = input.getBoundingClientRect();
    // the start of an RTL box is its left edge, where the text doesn't reach until it's full
    toggle.style.top  = (window.scrollY + r.top + 4) + 'px';
    toggle.style.left = (window.scrollX + r.left + 4) + 'px';
    toggle.hidden = false;
  }
  function hideToggle(){ if(toggle) toggle.hidden = true; }

  // one small stylesheet so every page that loads this file gets the new pieces
  const css = document.createElement('style');
  css.textContent = '.arkb-sw{flex:0 0 auto;min-width:44px;font-size:17px}' +
    '.arkb-toggle{position:absolute;z-index:150;width:34px;height:34px;border-radius:8px;border:1px solid var(--rule,#ccc);' +
    'background:var(--card,#fff);color:var(--ink,#222);font-size:17px;line-height:1;padding:0;cursor:pointer;opacity:.9}' +
    '.arkb-toggle[hidden]{display:none}';
  document.head.appendChild(css);

  // set inputmode before the tap focuses the box: phones pick a keyboard at focus time
  document.addEventListener('pointerdown', e=>{ const t = e.target.closest && e.target.closest('input.ar-in, textarea.ar-in'); if(t) applyMode(t); }, true);
  document.addEventListener('focusin', e=>{
    if(!isAr(e.target)) return;
    applyMode(e.target);
    if(touch() && mode()==='phone'){ hide(); showToggle(e.target); }
    else show(e.target);
  });
  document.addEventListener('focusout', e=>{
    // give a tap on the keyboard itself a moment to register before hiding
    setTimeout(()=>{
      if(!isAr(document.activeElement)) hideToggle();
      if(panel && !panel.contains(document.activeElement) && !isAr(document.activeElement)){
        hide();
      }
    },150);
  });
  window.RafiqKeyboard = { mode, setMode };
})();
