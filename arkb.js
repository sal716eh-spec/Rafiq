/* arkb.js — a small on-screen Arabic keyboard for any input.ar-in on the page,
   including ones that don't exist yet (every drill card is built by JS after
   this script loads, so it can't just scan the DOM once at startup).

   Works by listening for focus on the whole document rather than attaching to
   each input individually — one listener covers every input this page will
   ever create. Click or tap both fire the same 'click' event, so desktop and
   mobile need no separate handling. */
(function(){
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
        '<button type="button" class="arkb-key arkb-wide" data-act="space">مسافة</button>'+
        '<button type="button" class="arkb-key arkb-wide" data-act="back">⌫</button>'+
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
      else if(b.dataset.ch) insert(activeInput, b.dataset.ch);
    });
    document.body.appendChild(p);
    return p;
  }

  function show(input){
    activeInput=input;
    if(!panel) panel=build();
    panel.classList.add('on');
    positionAbove(input);
  }
  function hide(){ panel && panel.classList.remove('on'); }
  function positionAbove(input){
    // fixed to the bottom of the viewport on phones (thumb reach); tucked
    // under the input on wider screens
    if(window.matchMedia('(max-width:860px)').matches) return;   // CSS handles mobile placement
    const r=input.getBoundingClientRect();
    panel.style.top=(window.scrollY+r.bottom+8)+'px';
    panel.style.left=Math.max(8,Math.min(r.left+window.scrollX, window.innerWidth-panel.offsetWidth-8))+'px';
  }

  document.addEventListener('focusin', e=>{
    if(e.target.matches && e.target.matches('input.ar-in')) show(e.target);
  });
  document.addEventListener('focusout', e=>{
    // give a tap on the keyboard itself a moment to register before hiding
    setTimeout(()=>{
      if(panel && !panel.contains(document.activeElement) &&
         !(document.activeElement && document.activeElement.matches && document.activeElement.matches('input.ar-in'))){
        hide();
      }
    },150);
  });
})();
