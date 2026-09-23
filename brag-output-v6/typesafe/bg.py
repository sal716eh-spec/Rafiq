import json
exec(open('story.py').read().split('FACTS=')[0])
VIDEO=("A 60-second promotional video for Rafiq, an app for learning Modern Standard Arabic aimed mainly at Muslims in the UK. "
 "Warm paper-and-ink visuals, a calm English narrator, and short clips of a native Arabic voice saying words. "
 "It tells a story: you tried to learn Arabic and forgot the words; Rafiq brings words back before you forget them. "
 "The previous version without any background sound (only faint room tone) felt flat and less captivating.")
OPT={
 "roomtone":"Nothing but faint room tone under the voices (the current version).",
 "fountain":"A courtyard fountain: gently running water, with occasional distant birdsong, like a quiet masjid or Andalusian courtyard at dawn.",
 "qalam":"Close, crisp sounds of a reed pen writing on paper and pages turning, timed to the words appearing on screen.",
 "hum":"A soft, wordless vocal hum (human voices only, no instruments, no lyrics) that swells gently under the narration.",
 "nasheed":"A nasheed with Arabic lyrics sung over the video.",
 "windrain":"Soft rain on a window and a light breeze throughout.",
 "clock":"A soft clock tick in the problem section (words slipping away), easing into birdsong and water once Rafiq appears.",
 "daf":"A frame drum (daf) rhythm with no other instruments.",
 "recitation":"Quran recitation playing quietly in the background.",
 "layered":"Layered natural foley: pen on paper for words appearing, a soft page turn between scenes, and a light courtyard water bed that rises at the end."}
Q={
 "halal":{"type":"noul","instructions":"`video` Background sound: `option`. Would the large majority of practising Sunni Muslims in the UK, including those who avoid music, consider this background sound acceptable?"},
 "respect":{"type":"noul","instructions":"`video` Background sound: `option`. Is this a respectful use, i.e. it does not use sacred content (such as Quran recitation or the adhan) as mere background for an advert?"},
 "engage":{"type":"score","instructions":"`video` Background sound: `option`. How much would this background sound make the video more captivating and emotionally engaging?",
   "criteria":["Not at all: flat, distracting or off-putting","Slightly","Clearly more engaging","Much more engaging: it gives the video atmosphere and momentum"]},
 "fit":{"type":"score","instructions":"`video` Background sound: `option`. How well does it fit a calm, premium, Islamic-friendly Arabic learning brand?",
   "criteria":["Poor fit","Acceptable","Good fit","Perfect fit"]}}
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(6) as ex:
    res=list(ex.map(lambda k:(k,ask({"video":VIDEO,"option":OPT[k]},Q)),OPT))
rows=[]
for k,r in res:
    a=r["answers"]; rows.append((a["engage"]["score"]+a["fit"]["score"],k,a["halal"]["noul"],a["respect"]["noul"],a["engage"]["score"],a["fit"]["score"]))
print("option      halal  respect  engage(0-3)  fit(0-3)")
for t,k,h,rp,e,f in sorted(rows,reverse=True): print(f"{k:11} {h:.2f}   {rp:.2f}     {e:.2f}        {f:.2f}")
