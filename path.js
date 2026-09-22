/* path.js — the learning path: which step comes next, what's unlocked, streaks.
   Needs path-data.js (PATH, PIC), drills-data.js (DATA), vocab-data.js (VOCAB)
   and progress.js (Progress, already init()ed).

   A unit is a short run of steps, each about 5–10 minutes:
     meet 10 words → hear the conversation → how it works (grammar) →
     meet the next 10 → practise → … → say it yourself
   Steps are stored in the shared progress store as 'p:<unit>|<step>', so the
   path follows the learner across devices. A unit skipped by the placement
   check is stored as 'p:<unit>|placed'. Each day with any finished step or
   session is 's:<yyyy-mm-dd>', which gives the streak and the daily goal. */
(function(){
  const BATCH = 10;          // words met per step
  const GOAL  = 2;           // steps (or sessions) a day to meet the daily goal

  const unitData = n => DATA.find(u => u.n === n);
  const wordById = (() => { const m = new Map(); VOCAB.forEach(w => m.set(w.id, w)); return id => m.get(id); })();

  function steps(p){
    const nb = Math.ceil(p.words.length / BATCH), out = [];
    const words = i => ({key:'words'+(i+1), kind:'words', batch:i,
      title: nb > 1 ? `New words ${i+1} of ${nb}` : 'New words', mins: 5});
    out.push(words(0));
    out.push({key:'listen',   kind:'listen',   title:'Hear the conversation', mins:4});
    out.push({key:'grammar',  kind:'grammar',  title:'How it works',          mins:5});
    for(let i=1;i<nb;i++){
      out.push(words(i));
      if(i===1) out.push({key:'practise', kind:'practise', title:'Practise', mins:8});
    }
    if(nb<2) out.push({key:'practise', kind:'practise', title:'Practise', mins:8});
    out.push({key:'speak',    kind:'speak',    title:'Say it yourself',       mins:6});
    return out;
  }
  const sid = (n, key) => 'p:' + n + '|' + key;
  const stepDone = (n, key) => Progress.hasSeen(sid(n, key));
  const placed = n => Progress.hasSeen(sid(n, 'placed'));
  function unitDone(p){ return placed(p.n) || steps(p).every(s => stepDone(p.n, s.key)); }

  /* The unit you're on: the first one not finished. Everything before it is
     done; everything after is "coming up" but still openable. */
  function currentIndex(){
    const i = PATH.findIndex(p => !unitDone(p));
    return i < 0 ? PATH.length - 1 : i;
  }
  function next(){
    const i = currentIndex(), p = PATH[i];
    const s = steps(p).find(s => !stepDone(p.n, s.key)) || null;
    return {unit:p, index:i, step:s, finishedAll: i === PATH.length-1 && unitDone(p)};
  }
  const reached = () => PATH.slice(0, currentIndex() + 1);

  function complete(n, key){
    Progress.touch(sid(n, key));
    markDay();
  }
  function place(uptoIndex){          // placement: skip units before this one
    PATH.slice(0, uptoIndex).forEach(p => { if(!unitDone(p)) Progress.touch(sid(p.n, 'placed')); });
  }

  const iso = d => d.toISOString().slice(0,10);
  function markDay(){ Progress.touch('s:' + iso(new Date())); }
  function doneToday(){ const r = Progress.get('s:' + iso(new Date())); return r ? r.seen : 0; }
  function streak(){
    const d = new Date(); let n = 0;
    if(!Progress.hasSeen('s:' + iso(d))) d.setDate(d.getDate()-1);   // today not done yet: count from yesterday
    while(Progress.hasSeen('s:' + iso(d))){ n++; d.setDate(d.getDate()-1); }
    return n;
  }

  function wordsOf(p, batch){
    const ids = batch == null ? p.words : p.words.slice(batch*BATCH, (batch+1)*BATCH);
    return ids.map(wordById).filter(Boolean);
  }

  window.RafiqPath = { BATCH, GOAL, steps, stepDone, unitDone, placed, currentIndex, next, reached,
                       complete, place, markDay, doneToday, streak, wordsOf, unitData, wordById };
})();
