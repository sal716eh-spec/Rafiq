#!/usr/bin/env node
const fs=require('fs'), path=require('path'), root=path.join(__dirname,'..');
const KEY=process.env.ELEVENLABS_API_KEY;
/* A flag with no value used to swallow the next flag — e.g. a blank --limit
   would eat --model. Treat "next thing starts with --" as no value given. */
const arg=(f,d)=>{
  const i=process.argv.indexOf(f);
  if(i<0) return d;
  const v=process.argv[i+1];
  return (v===undefined || v.startsWith('--')) ? d : v;
};
const has=f=>process.argv.includes(f);

const VOICE=arg('--voice'), MODEL=arg('--model','eleven_multilingual_v2');
const ONLY=(arg('--only','')||'').split(',').filter(Boolean);
const rawLimit=arg('--limit','0');
const LIMIT=Number.isFinite(parseInt(rawLimit,10))?parseInt(rawLimit,10):0;   // blank or junk = no limit
const DRY=has('--dry'), STRIP=has('--strip'), FORCE=has('--force');   // --force re-records clips that already exist (e.g. a new voice)
const outDir=path.join(root,'audio');

const stripTashkeel=s=>s.replace(/[\u064B-\u0652\u0670\u0640]/g,'');

async function listVoices(){
  const r=await fetch('https://api.elevenlabs.io/v1/voices',{headers:{'xi-api-key':KEY}});
  if(!r.ok){console.error('API error',r.status,await r.text());process.exit(1);}
  const {voices}=await r.json();
  voices.forEach(v=>console.log('  '+v.voice_id+'  '+v.name));
}

async function main(){
  if(has('--list-voices')){ if(!KEY){console.error('Set ELEVENLABS_API_KEY first.');process.exit(1);} return listVoices(); }

  let items=JSON.parse(fs.readFileSync(path.join(root,'audio-manifest.json'),'utf8'));
  // --only also sets the order: buckets listed first are rendered first
  if(ONLY.length) items=items.filter(i=>ONLY.includes(i.bucket)).sort((a,b)=>ONLY.indexOf(a.bucket)-ONLY.indexOf(b.bucket));
  fs.mkdirSync(outDir,{recursive:true});
  const todo=FORCE?items:items.filter(i=>!fs.existsSync(path.join(outDir,i.id+'.mp3')));
  const done=items.length-todo.length;
  const batch=LIMIT?todo.slice(0,LIMIT):todo;
  const chars=batch.reduce((a,b)=>a+b.chars,0);

  console.log(items.length+' clips selected · '+done+' already rendered · '+batch.length+' to do · '+chars+' characters');
  if(DRY){console.log('(dry run — nothing sent)');return;}
  if(!KEY){console.error('Set ELEVENLABS_API_KEY first.');process.exit(1);}
  if(!VOICE){console.error('Pass --voice <id>.');process.exit(1);}
  if(!batch.length){console.log('Nothing to do.');return writeIndex();}

  let ok=0,fail=0;
  for(const [n,it] of batch.entries()){
    const text=STRIP?stripTashkeel(it.text):it.text;
    try{
      const r=await fetch('https://api.elevenlabs.io/v1/text-to-speech/'+VOICE,{
        method:'POST',
        headers:{'xi-api-key':KEY,'Content-Type':'application/json','Accept':'audio/mpeg'},
        body:JSON.stringify({text,model_id:MODEL,
          voice_settings:{stability:0.5,similarity_boost:0.75,style:0,use_speaker_boost:true}})
      });
      if(!r.ok){
        const msg=await r.text();
        if(r.status===429 || /quota_exceeded/.test(msg)){console.error('\nRate limited or out of credits. Progress saved — rerun later.');break;}
        console.error('  x '+it.id+' '+r.status+' '+msg.slice(0,120));fail++;continue;
      }
      fs.writeFileSync(path.join(outDir,it.id+'.mp3'),Buffer.from(await r.arrayBuffer()));
      ok++;
      console.log('  '+(n+1)+'/'+batch.length+'  '+it.bucket+'  '+it.text.slice(0,28));
      await new Promise(r=>setTimeout(r,250));
    }catch(e){console.error('  x '+it.id+' '+e.message);fail++;}
  }
  console.log('\nrendered '+ok+', failed '+fail);
  writeIndex();
}

function writeIndex(){
  const ids=fs.readdirSync(outDir).filter(f=>f.endsWith('.mp3')).map(f=>f.replace('.mp3',''));
  fs.writeFileSync(path.join(outDir,'index.json'),JSON.stringify(ids));
  console.log('audio/index.json now lists '+ids.length+' clips');
}
main();
