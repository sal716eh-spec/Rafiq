#!/usr/bin/env node
/* ElevenLabs voice helper (runs in the "ElevenLabs voices" action).
     node tools/voices.js list                       — voices on the account
     node tools/voices.js search "<query>" [lang] [gender]  — the shared voice library
     node tools/voices.js add <public_owner_id> <voice_id> <name>  — add a library voice to the account */
const KEY=process.env.ELEVENLABS_API_KEY, [,,cmd,...a]=process.argv;
const H={'xi-api-key':KEY,'Content-Type':'application/json'};
const get=async u=>{ const r=await fetch(u,{headers:H}); if(!r.ok){console.error(r.status,await r.text());process.exit(1);} return r.json(); };
(async()=>{
  if(cmd==='list'){
    const {voices}=await get('https://api.elevenlabs.io/v1/voices');
    voices.forEach(v=>console.log([v.voice_id,v.name,v.category,JSON.stringify(v.labels||{})].join(' | ')));
  } else if(cmd==='search'){
    const q=new URLSearchParams({page_size:'40',search:a[0]||''}); if(a[1]) q.set('language',a[1]); if(a[2]) q.set('gender',a[2]);
    const {voices}=await get('https://api.elevenlabs.io/v1/shared-voices?'+q);
    voices.forEach(v=>console.log([v.voice_id,v.public_owner_id,v.name,v.gender,v.age,v.accent,v.language,v.use_case,'cloned:'+v.cloned_by_count,(v.description||'').slice(0,90)].join(' | ')));
  } else if(cmd==='add'){
    const r=await fetch(`https://api.elevenlabs.io/v1/voices/add/${a[0]}/${a[1]}`,{method:'POST',headers:H,body:JSON.stringify({new_name:a[2]||'Rafiq voice'})});
    console.log(r.status, await r.text());
  } else { console.error('list | search | add'); process.exit(1); }
})();
