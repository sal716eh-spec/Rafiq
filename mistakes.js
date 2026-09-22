/* mistakes.js — the mistake profile. judge.js records the type of every
   mistake the judge finds (gender, tense, spelling, …) in localStorage. This
   picks the one that keeps coming back — 3 or more in the last 7 days — and
   offers a short explanation for it. The explanations are written here, not
   generated: the judge only chooses which one applies. */
(function(){
  const KEY='rafiq_mistakes', HIDE='rafiq_focus_hidden';
  const WEEK=7*86400000, MIN=3;
  const HELP={
    gender_agreement:{title:'Masculine and feminine must match',
      body:'Words that describe or point to a noun take its gender, and feminine nouns usually end in ة.',
      ex:[['هَذا بَيْتٌ كَبِيرٌ','This is a big house'],['هَذِهِ غُرْفَةٌ كَبِيرَةٌ','This is a big room'],['هُوَ يَدْرُسُ · هِيَ تَدْرُسُ','He studies · she studies']]},
    wrong_person_or_tense:{title:'Who is doing it, and when?',
      body:'In the present tense the start of the verb shows who: أَ I, تَ you or she, يَ he, نَ we. In the past the ending shows who.',
      ex:[['أَذْهَبُ · تَذْهَبُ · يَذْهَبُ','I go · you go · he goes'],['ذَهَبْتُ · ذَهَبَ','I went · he went']]},
    spelling:{title:'Letters that sound alike',
      body:'Some letters sound close to English ears but are different letters: س and ص, ت and ط, د and ض, ه and ح, ك and ق. Mixing them makes a different word.',
      ex:[['مِصْرُ','Egypt (not مِسْر)'],['صَدِيقٌ','friend (not سَدِيق)']]},
    grammar_other:{title:'Three small rules that trip people up',
      body:'After كَمْ the noun is singular. Numbers 3–10 take the opposite gender to the noun. An indefinite object ends in ًا.',
      ex:[['كَمْ غُرْفَةً؟','How many rooms?'],['ثَلاثَةُ إِخْوَةٍ · ثَلاثُ أَخَواتٍ','three brothers · three sisters'],['أُرِيدُ دَجاجًا','I want chicken']]},
    meaning:{title:'Say exactly what was asked',
      body:'Check every part of the task is in your sentence — who, what, when — and that nothing has changed. Build it in pieces: say the first half, then add the rest.',
      ex:[['أَذْهَبُ · إِلى الْعَمَلِ · بِالْحافِلَةِ','I go · to work · by bus']]},
  };
  const GROUP={wrong_word:'meaning', different_meaning:'meaning', missing_word:'meaning'};
  const read=(k,d)=>{ try{ return JSON.parse(localStorage.getItem(k)) || d; }catch(_){ return d; } };

  function counts(){
    const m=read(KEY,{}), now=Date.now(), out={};
    Object.entries(m).forEach(([err,ts])=>{
      const k=GROUP[err]||err; if(!HELP[k]) return;
      out[k]=(out[k]||0)+ts.filter(t=>now-t<WEEK).length;
    });
    return out;
  }
  /* The one to work on, or null. Hidden for 3 days after "Got it". */
  function focus(){
    const c=counts(), hid=read(HIDE,{}), now=Date.now();
    const top=Object.entries(c).filter(([k,n])=>n>=MIN && !(hid[k] && now-hid[k]<3*86400000))
      .sort((a,b)=>b[1]-a[1])[0];
    return top ? {key:top[0], count:top[1], ...HELP[top[0]]} : null;
  }
  function gotIt(key){ const h=read(HIDE,{}); h[key]=Date.now(); try{ localStorage.setItem(HIDE, JSON.stringify(h)); }catch(_){} }

  window.RafiqMistakes={counts, focus, gotIt, HELP};
})();
