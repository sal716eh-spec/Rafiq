#!/usr/bin/env node
/* Generates sound effects with ElevenLabs (text to sound) from a JSON list:
     [{name, text, duration, loop?}, ...]
   Usage: ELEVENLABS_API_KEY=... node tools/generate-sfx.js <prompts.json> <out-dir> [--force]
   Skips files that already exist unless --force; stops cleanly when credits run out. */
const fs=require('fs'), path=require('path');
const KEY=process.env.ELEVENLABS_API_KEY;
const [,, list, outDir]=process.argv, FORCE=process.argv.includes('--force');
if(!KEY||!list||!outDir){ console.error('Usage: ELEVENLABS_API_KEY=… node tools/generate-sfx.js <prompts.json> <out-dir> [--force]'); process.exit(1); }
const items=JSON.parse(fs.readFileSync(list,'utf8'));
fs.mkdirSync(outDir,{recursive:true});
(async()=>{
  let ok=0, fail=0;
  for(const it of items){
    const file=path.join(outDir, it.name+'.mp3');
    if(!FORCE && fs.existsSync(file)){ console.log('  = '+it.name+' (exists)'); continue; }
    const body={text:it.text, duration_seconds:it.duration, prompt_influence:0.5, model_id:'eleven_text_to_sound_v2'};
    if(it.loop) body.loop=true;
    let r=await fetch('https://api.elevenlabs.io/v1/sound-generation',{method:'POST',
      headers:{'xi-api-key':KEY,'Content-Type':'application/json','Accept':'audio/mpeg'}, body:JSON.stringify(body)});
    if(r.status===422 || r.status===400){          // older API without model_id/loop: try the plain request
      delete body.model_id; delete body.loop;
      r=await fetch('https://api.elevenlabs.io/v1/sound-generation',{method:'POST',
        headers:{'xi-api-key':KEY,'Content-Type':'application/json','Accept':'audio/mpeg'}, body:JSON.stringify(body)});
    }
    if(!r.ok){
      const msg=await r.text();
      if(r.status===429 || /quota_exceeded/.test(msg)){ console.error('\nOut of credits or rate limited — stopping.'); break; }
      console.error('  x '+it.name+' '+r.status+' '+msg.slice(0,160)); fail++; continue;
    }
    fs.writeFileSync(file, Buffer.from(await r.arrayBuffer()));
    ok++; console.log('  ✓ '+it.name+' ('+it.duration+'s)');
  }
  console.log('\ngenerated '+ok+', failed '+fail);
})();
