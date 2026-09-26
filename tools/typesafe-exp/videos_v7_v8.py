# Assess the v7 (every feature / tutorial) and v8 (the story) videos. Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/videos_v7_v8.py
from concurrent.futures import ThreadPoolExecutor
import json, os, time, urllib.request
KEY = os.environ.get("TYPESAFE_API_KEY") or os.environ["TYPE_SAFE_KEY"]
def ask(state, qs):
    body = json.dumps({"state": state, "model": "jev-latest", "questions": qs}).encode()
    for a in range(5):
        try:
            r = urllib.request.Request("https://api.typesafe.ai/v1/systemone", body, {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
            with urllib.request.urlopen(r, timeout=60) as f: return json.load(f)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504, 529) and a < 4: time.sleep(2 ** a); continue
            raise


import subprocess
FACTS=("TRUE FACTS ABOUT RAFIQ (Sept 2026): web app (rafiq-arabic.com), no native app. Teaches Modern Standard Arabic to adult beginners, about A1-A2. "
 "Home has one Continue button and one path: a reading starter (28 letters in 7 shape families, each letter with 3 example words with the letter in red and a native-voice recording; "
 "then the vowel marks; then a listening test: hear a word, pick its first letter from look-alike sounds, 9 of 12 to pass), then 12 units (greetings, family, housing, daily life, food, prayer, study, "
 "work, shopping, weather, people & places, hobbies). Steps of 5-10 minutes: meet 10 new words, hear a conversation, one grammar idea, practise, have the conversation, say it yourself. "
 "'Say this in Arabic': word tiles in units 1-3, tiles plus a wrong piece in 4-6, typing from unit 7, adapting to the learner. Spaced repetition on fixed widening gaps (1, 2, 4, 8, 16 days...), "
 "self-rated flashcards plus app-marked quizzes. AI checks typed Arabic and conversation replies and names the mistake type. Practise area: weak-spots review built from repeat mistakes, "
 "spelling bee, 21 common verbs in past/present/future, joining words, real-life scenes (airport, doctor, masjid, restaurant, taxi, family visit), redo a unit. "
 "Plans: Essentials and Complete, 7-day free trial, no permanent free tier (currently everyone gets Complete free during a beta). Audience mostly UK Muslims; no music (halal-conscious).")
VIEWERS={"muslim":"a UK Muslim adult who prays in Arabic, wants to understand it and speak basic Arabic, has quit apps before",
 "revert":"a new Muslim who can't read Arabic script yet",
 "student":"someone taking an Arabic class or madrasa who wants help revising",
 "general":"a busy adult curious about learning Arabic, scrolling on their phone"}
def lines(v):
    t=subprocess.run(['git','show',f'origin/claude/confident-meitner-owkvtb:brag-output-v{v}/vo-script.txt'],capture_output=True,text=True).stdout
    return [l.split('|',2) for l in t.strip().split('\n') if '|' in l]
V={7:("a 90-second 'everything inside' tutorial video: shows the real app screens while a narrator (and Rafiq, the app's voice) walks through the features",
       "Its purpose: a new user watches it and then knows how to use the app and what is in it."),
   8:("an 86-second 'the story' video about why Rafiq exists: the name, the problem of forgetting, the memory research it is built on (spacing, testing, habit, with on-screen citations), then the reading starter",
       "Its purpose: make viewers trust Rafiq, care about it, and try it.")}
QL={"true":{"type":"noul","instructions":"`facts` Voiceover line from a Rafiq video: `line`. Is everything this line says or implies about Rafiq true according to the facts?"},
    "clear":{"type":"score","instructions":"Voiceover line in a short app video: `line`. How clear is it to a beginner hearing it once?","criteria":["Confusing","OK","Clear","Crystal clear"]},
    "cheesy":{"type":"noul","instructions":"Voiceover line in a short app video: `line`. Does it sound cheesy, salesy or generic?"}}
QV={"hook":{"type":"score","instructions":"`facts` Video: `desc` `purpose` Full script: `script`. Viewer: `viewer`. How strongly do the first two lines make this viewer keep watching?","criteria":["Scroll past","Maybe","Keep watching","Hooked"]},
    "purpose":{"type":"score","instructions":"`facts` Video: `desc` `purpose` Full script: `script`. Viewer: `viewer`. How well does the video achieve its purpose for this viewer?","criteria":["Poorly","OK","Well","Very well"]},
    "special":{"type":"score","instructions":"`facts` Video: `desc` Full script: `script`. Viewer: `viewer`. How clearly does it show why Rafiq is different from Duolingo or a Quran app?","criteria":["Not at all","A little","Clearly","Very clearly"]},
    "try":{"type":"score","instructions":"`facts` Video: `desc` Full script: `script`. Viewer: `viewer`. How likely is this viewer to try Rafiq afterwards?","criteria":["Unlikely","Maybe","Likely","Very likely"]},
    "long":{"type":"score","instructions":"Video: `desc` Full script: `script`. Viewer: `viewer`. How does the length and amount of information feel?","criteria":["Far too much","A bit much","About right","Could be longer"]}}
out={}
with ThreadPoolExecutor(8) as ex:
    for v in V:
        L=lines(v); script=' '.join(f'[{w}] {t}' for _,w,t in L)
        rl=list(ex.map(lambda x:ask({"facts":FACTS,"line":x[2]},QL)["answers"],L))
        rv=dict(ex.map(lambda k:(k,ask({"facts":FACTS,"desc":V[v][0],"purpose":V[v][1],"script":script,"viewer":VIEWERS[k]},QV)["answers"]),VIEWERS))
        out[v]=(L,rl,rv)
for v,(L,rl,rv) in out.items():
    print(f"\n===== v{v}")
    print("line  true  clear  cheesy  text")
    for (i,w,t),a in zip(L,rl): print(f"{i:4}  {a['true']['noul']:.2f}  {a['clear']['score']:.2f}   {a['cheesy']['noul']:.2f}    {t[:95]}")
    print("viewer    hook  purpose  special  try   length(2=right)")
    for k in VIEWERS: a=rv[k]; print(f"{k:8}  {a['hook']['score']:.2f}  {a['purpose']['score']:.2f}     {a['special']['score']:.2f}     {a['try']['score']:.2f}  {a['long']['score']:.2f}")
    m=lambda q: sum(rv[k][q]['score'] for k in VIEWERS)/len(VIEWERS)
    print(f"average   {m('hook'):.2f}  {m('purpose'):.2f}     {m('special'):.2f}     {m('try'):.2f}  {m('long'):.2f}")

# ---- round 2: corrected facts, then pick the best of written alternatives for the weak lines
FACTS2=FACTS+(" ALSO TRUE: Rafiq (رَفِيق) means companion / friend in Arabic. Home shows a daily goal (2 steps) and a daily streak with milestone celebrations; "
 "the Progress page shows words learned per day and practice days. No push/email reminders yet. The review schedule is fixed widening gaps, not a personal forgetting model. "
 "The AI names the actual mistake (e.g. masculine/feminine agreement) and the weak-spots review drills the mistakes you repeat. There is a prayer unit and a masjid scene.")
print("\n=== corrected facts: re-check the low 'true' lines")
recheck=[("v7 r06","And رَفِيق brings every word back for review, just before you'd forget it."),
 ("v7 n12","Have the conversation yourself, and get feedback on every reply."),
 ("v7 r15","Try رَفِيق free today."),
 ("v8 r01","رَفِيق. In Arabic, it means companion."),
 ("v8 n04","So everything here is built on what memory research says works."),
 ("v8 n07","Habit. A little every day. In one well-known study, a daily habit took about sixty-six days to feel automatic."),
 ("v8 n14","A few minutes a day, with a companion beside you.")]
with ThreadPoolExecutor(8) as ex: rr=list(ex.map(lambda x:ask({"facts":FACTS2,"line":x[1]},{"true":QL["true"]})["answers"]["true"]["noul"],recheck))
for (k,t),p in zip(recheck,rr): print(f"  {k}: {p:.2f}  {t}")

CAND={
 "v7 opening (hook)":("the first line of the 90-second 'everything inside' tutorial", [
   "Here's the easiest way to learn Arabic: open the app, and press Continue.",
   "Ninety seconds, and you'll know exactly how to learn Arabic with Rafiq.",
   "You open Rafiq. You press Continue. Here's everything that happens next.",
   "Want to understand the Arabic you hear every day, and speak it back? Here's how Rafiq works."]),
 "v7 line that shows what's different":("a line to add to the tutorial, after the conversation feature, to show what makes Rafiq different", [
   "Have the conversation yourself, and get feedback on every reply.",
   "Write real Arabic, and it tells you exactly what went wrong, the way a teacher would.",
   "Type your own replies, and Rafiq names the mistake, like mixing up masculine and feminine, then helps you fix it.",
   "Unlike a quiz app, you write real Arabic, and get told what to fix."]),
 "v7 closing line":("the closing line of the tutorial before the call to action", [
   "Your journey, or something specific. A few minutes a day.",
   "Press Continue each day, or practise what you need. A few minutes is enough.",
   "One path to follow, and practice whenever you want more. A few minutes a day.",
   "That's everything. Now press Continue."]),
 "call to action":("the final spoken call to action of both videos (the app has a 7-day free trial and is currently free during a beta)", [
   "Try رَفِيق free today.",
   "Try رَفِيق free at rafiq-arabic.com.",
   "Start your first lesson free at rafiq-arabic.com.",
   "Your first letter is waiting. rafiq-arabic.com."]),
 "v8 research line":("the line in 'the story' that introduces the memory research", [
   "So everything here is built on what memory research says works.",
   "So Rafiq is built on three things memory research agrees on.",
   "So we built Rafiq around three findings from memory research.",
   "Memory research has three simple answers. Rafiq is built on them."]),
 "v8 closing line":("the closing line of 'the story' before the call to action", [
   "A few minutes a day, with a companion beside you.",
   "From your first letter to your first conversation, a companion the whole way.",
   "A few minutes a day. Words that stay.",
   "Your companion for Arabic: a few minutes a day, and words that finally stay."]),
}
QC={"best":{"type":"score","instructions":"`facts` This is `slot` in a Rafiq video. Candidate line: `line`. Viewer: `viewer`. How good is it for this viewer: clear, memorable, persuasive, not cheesy?","criteria":["Weak","OK","Good","Excellent"]},
    "true":QL["true"]}
print("\n=== alternatives (avg over 4 viewers; true = claims supported)")
for slot,(desc,opts) in CAND.items():
    jobs=[(o,k) for o in opts for k in VIEWERS]
    with ThreadPoolExecutor(8) as ex: r=dict(ex.map(lambda j:(j,ask({"facts":FACTS2,"slot":desc,"line":j[0],"viewer":VIEWERS[j[1]]},QC)["answers"]),jobs))
    print(f"-- {slot}")
    for o in sorted(opts,key=lambda o:-sum(r[(o,k)]['best']['score'] for k in VIEWERS)):
        print(f"   {sum(r[(o,k)]['best']['score'] for k in VIEWERS)/4:.2f}  true {sum(r[(o,k)]['true']['noul'] for k in VIEWERS)/4:.2f}  {'(current) ' if o==opts[0] else ''}{o}")

# ---- round 3: accurate versions of the two overclaiming lines
CAND3={
 "spaced-review line":("the line explaining how reviews work", [
   "And رَفِيق brings every word back for review, just before you'd forget it.",
   "And رَفِيق brings every word back for review: after a day, then two, four, eight, so it sticks.",
   "And رَفِيق brings each word back again and again, a little further apart each time, until it sticks.",
   "And رَفِيق brings every word back at the moments it's starting to fade."]),
 "habit line":("the 'habit' point in the story, about memory research", [
   "Habit. A little every day. In one well-known study, a daily habit took about sixty-six days to feel automatic.",
   "Habit. A little every day. A daily goal and a streak keep you coming back, and in one study a new habit took about two months to feel automatic.",
   "Habit. A few minutes every day beats an hour once a week. Rafiq gives you a small daily goal and a streak to keep.",
   "Habit. A little, every day. In one study, a daily habit took about two months to feel automatic, so Rafiq keeps each day small."])}
print("\n=== round 3")
for slot,(desc,opts) in CAND3.items():
    jobs=[(o,k) for o in opts for k in VIEWERS]
    with ThreadPoolExecutor(8) as ex: r=dict(ex.map(lambda j:(j,ask({"facts":FACTS2,"slot":desc,"line":j[0],"viewer":VIEWERS[j[1]]},QC)["answers"]),jobs))
    print(f"-- {slot}")
    for o in sorted(opts,key=lambda o:-(sum(r[(o,k)]['best']['score'] for k in VIEWERS)/4+sum(r[(o,k)]['true']['noul'] for k in VIEWERS)/4)):
        print(f"   good {sum(r[(o,k)]['best']['score'] for k in VIEWERS)/4:.2f}  true {sum(r[(o,k)]['true']['noul'] for k in VIEWERS)/4:.2f}  {'(current) ' if o==opts[0] else ''}{o}")
