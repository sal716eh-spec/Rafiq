/* path.js — the learning path: which step comes next, what's unlocked, streaks.
   Needs path-data.js (PATH, PIC), drills-data.js (DATA), vocab-data.js (VOCAB)
   and progress.js (Progress, already init()ed).

   A unit is a short run of steps, each about 5–10 minutes:
     meet 10 words → hear the conversation → how it works (grammar) →
     meet the next 10 → practise → … → have the conversation → say it yourself
   Steps are stored in the shared progress store as 'p:<unit>|<step>', so the
   path follows the learner across devices. A unit skipped by the placement
   check is stored as 'p:<unit>|placed'. Each day with any finished step or
   session is 's:<yyyy-mm-dd>', which gives the streak and the daily goal. */
(function(){
  const BATCH = 10;          // words met per step
  // steps (or sessions) a day to meet the daily goal; set at sign-up from minutes a day
  const GOAL  = (() => { try{ const g=parseInt(localStorage.getItem('rafiq_goal'),10); return g>0 ? g : 2; }catch(_){ return 2; } })();

  /* Unit 0, the reading starter, comes first for everyone; readers skip it
     with one tap or through placement. It exists only if alphabet-data.js is
     loaded on the page. */
  const ALPHA = typeof ALPHABET_GROUPS !== 'undefined'
    ? [{n:'00', ar:'الْحُرُوفُ', en:'Reading Arabic', words:[], alpha:true}] : [];
  const UNITS = ALPHA.concat(PATH);
  const units = () => UNITS;
  const unitData = n => DATA.find(u => u.n === n);
  /* Announced, not built yet: shown after the last unit on Home and on the
     pricing page. Update as units ship (and move them into the path). */
  const COMING = [
    {ar:'السَّفَرُ',              en:'Travel & directions',    d:'Airports, hotels, asking the way'},
    {ar:'الصِّحَّةُ',              en:'Health & the body',      d:'At the doctor, how you feel'},
    {ar:'رَمَضانُ وَالْعِيدُ',      en:'Ramadan & Eid',          d:'Fasting, iftar, Eid visits'},
    {ar:'الْحِكاياتُ',             en:'Telling stories',        d:'What happened — the past tense in use'},
  ];
  const wordById = (() => { const m = new Map(); VOCAB.forEach(w => m.set(w.id, w)); return id => m.get(id); })();

  function steps(p){
    if(p.alpha) return ALPHABET_GROUPS.map((g,i) => ({key:'letters'+(i+1), kind:'letters', group:i,
        title:g.title.replace(/^Letters \d+: /,'Letters: '), mins:5}))
      .concat([{key:'vowels', kind:'vowels', title:'The vowel marks', mins:5}]);
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
    out.push({key:'chat',     kind:'chat',     title:'Have the conversation', mins:6});
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
    const i = UNITS.findIndex(p => !unitDone(p));
    return i < 0 ? UNITS.length - 1 : i;
  }
  function next(){
    const i = currentIndex(), p = UNITS[i];
    const s = steps(p).find(s => !stepDone(p.n, s.key)) || null;
    return {unit:p, index:i, step:s, finishedAll: i === UNITS.length-1 && unitDone(p)};
  }
  /* Locks: a unit opens once every unit before it is done (or skipped by
     placement); inside the current unit, steps open in order. Anything
     finished can always be revisited. The Practise area is never locked. */
  const unitIndex = n => UNITS.findIndex(p => p.n === n);
  const unitOpen = n => { const i = unitIndex(n); return i >= 0 && i <= currentIndex(); };
  function stepOpen(n, key){
    const i = unitIndex(n); if(i < 0) return false;
    const cur = currentIndex();
    if(i < cur) return true;
    if(i > cur) return false;
    const p = UNITS[i], first = steps(p).find(s => !stepDone(p.n, s.key));
    return stepDone(n, key) || (first && first.key === key);
  }
  // units whose material sessions may use (the reading starter has none)
  const reached = () => UNITS.slice(0, currentIndex() + 1).filter(p => !p.alpha);

  /* What review may draw on: only what the learner has actually done on the
     path — words they've met in lessons (from units reached) and sentence
     exercises they've already practised there. Nothing from the Practise area
     (verbs, joining words) and nothing they haven't seen yet. */
  function reviewScope(){
    const units = reached();
    const wordIds = new Set(units.flatMap(p => p.words));
    return { units: new Set(units.map(p => p.n)), wordIds };
  }
  const inScope = (id, sc) => id.startsWith('v:') ? sc.wordIds.has(+id.slice(2))
                            : id.startsWith('d:') ? sc.units.has(id.slice(2, 4)) : false;
  /* Items in scope that are due for review today (for the Home nudge). */
  function reviewDue(){ const sc = reviewScope(); return Progress.dueIds().filter(id => inScope(id, sc)).length; }
  /* Anything learned at all (so review isn't offered before the first lesson). */
  function hasLearned(){ const sc = reviewScope();
    return VOCAB.some(w => sc.wordIds.has(w.id) && !Progress.isNew('v:' + w.id)); }

  function complete(n, key){
    Progress.touch(sid(n, key));
    markDay();
  }
  function place(uptoIndex){          // placement: skip units before this one (index into units())
    UNITS.slice(0, uptoIndex).forEach(p => { if(!unitDone(p)) Progress.touch(sid(p.n, 'placed')); });
  }
  const skipReading = () => { if(ALPHA.length && !unitDone(ALPHA[0])) Progress.touch(sid('00','placed')); };

  const iso = d => d.toISOString().slice(0,10);
  function markDay(){ Progress.touch('s:' + iso(new Date())); }
  // one 'w:<date>' row per day; its count is the number of new words met that day
  function wordMet(){ Progress.touch('w:' + iso(new Date())); }
  /* The last 7 days: days active, steps and sessions finished, new words met. */
  function week(){
    let days=0, steps=0, words=0;
    for(let k=0;k<7;k++){
      const d=new Date(); d.setDate(d.getDate()-k); const day=iso(d);
      const s=Progress.get('s:'+day), w=Progress.get('w:'+day);
      if(s && s.seen){ days++; steps+=s.seen; }
      if(w && w.seen) words+=w.seen;
    }
    return {days, steps, words};
  }
  function doneToday(){ const r = Progress.get('s:' + iso(new Date())); return r ? r.seen : 0; }
  /* Streak goals. Each says what the research behind daily, spaced practice
     suggests is happening by then — no invented percentages. Sources: the
     spacing effect (Cepeda et al., 2006, review of 254 studies), the testing
     effect (Roediger & Karpicke, 2006), habit formation (Lally et al., 2010). */
  const STREAK_GOALS = [
    {days:3,   why:'Your first words come back for review. Recalling a word after a gap makes it fade more slowly — the spacing effect, one of the most replicated findings in memory research.'},
    {days:7,   why:'The words from your first day will have come back twice. Spreading practice over days beats cramming the same time into one sitting.'},
    {days:14,  why:'Pulling a word from memory strengthens it more than re-reading it — the testing effect. Two weeks of daily recall adds up.'},
    {days:30,  why:'Your earliest words are on long review gaps by now — a sign they\'re settling into long-term memory.'},
    {days:66,  why:'66 days was the average time for a daily habit to start feeling automatic in a well-known habit study (Lally et al., 2010).'},
    {days:100, why:'A hundred days of Arabic. By now it\'s simply part of your day.'},
  ];
  /* {next, left, from, why} for the goal you're working towards, and the goal
     reached today if the streak has just hit one. */
  function streakGoal(n){
    const next = STREAK_GOALS.find(g => g.days > n) || null;
    const prev = [...STREAK_GOALS].reverse().find(g => g.days <= n);
    return { next, left: next ? next.days - n : 0, from: prev ? prev.days : 0,
             reached: STREAK_GOALS.find(g => g.days === n) || null };
  }
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

  window.RafiqPath = { reviewScope, reviewDue, hasLearned, COMING, STREAK_GOALS, streakGoal, BATCH, GOAL, units, skipReading, unitOpen, stepOpen, steps, stepDone, unitDone, placed, currentIndex, next, reached,
                       complete, place, markDay, wordMet, week, doneToday, streak, wordsOf, unitData, wordById };
})();
