import json, os, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
KEY=os.environ.get("TYPESAFE_API_KEY") or os.environ["TYPE_SAFE_KEY"]; URL="https://api.typesafe.ai/v1/systemone"
def ask(state, qs):
    body=json.dumps({"state":state,"model":"jev-latest","questions":qs}).encode()
    for a in range(5):
        try:
            req=urllib.request.Request(URL,body,{"Authorization":f"Bearer {KEY}","Content-Type":"application/json"})
            with urllib.request.urlopen(req,timeout=60) as r: return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429,500,502,503,504,529) and a<4: time.sleep(2**a); continue
            raise
FACTS=["Rafiq is a web app for learning Modern Standard Arabic (fusha), at rafiq-arabic.com.",
 "Everything is fully vowelled (with harakat).",
 "Home shows one path with a single Continue button; units open in order; each step takes about 5-10 minutes.",
 "Each unit: meet 10 new words at a time (with audio and, for many words, a picture), hear a conversation, a short grammar explanation, practice, have the conversation yourself, then speak freely.",
 "Words you meet go into spaced repetition: they come back for review on a growing schedule (next day, then after longer gaps), and Home shows how many are due.",
 "A conversation partner: you reply in your own words and it tells you straight away whether your reply fits and whether the grammar is right; nothing is generated, it compares with checked model lines.",
 "It notices the kinds of mistakes you repeat (e.g. gender agreement, case endings) and offers a weak-spots review built from them.",
 "Six real-life scenes: airport, doctor, masjid, restaurant, taxi, visiting a family.",
 "A reading starter teaches the 28 letters and vowel marks; people who can read skip it.",
 "A short placement check at sign-up sets your starting unit.",
 "A Progress page shows words learned, sentences practised, streaks and streak goals based on memory research (spacing effect, testing effect, habit formation).",
 "12 units now (greetings, family, housing, daily life, food, prayer, study, work, shopping, weather, people and places, hobbies); more coming.",
 "Audio uses a native Arabic voice.",
 "There is a 7-day free trial; it is currently free during beta."]
VIEWERS={
 "quran":"An adult Muslim in the UK who wants to understand the Quran and prayers in Arabic, started twice before and gave up.",
 "heritage":"A second-generation Arab who understands some dialect at home but can't read well or speak formal Arabic.",
 "forgot":"A busy professional who did a few weeks on a language app, then forgot most of the words.",
 "beginner":"A complete beginner who finds the Arabic script intimidating.",
}
C={
 "hook":{
  "h1":"Learned an Arabic word last week? Can you still remember it?",
  "h2":"You've started learning Arabic before. Maybe more than once.",
  "h3":"Most people who start Arabic give up in the first month.",
  "h4":"You learn a word on Monday. By Friday, it's gone.",
  "h5":"Fluent Arabic in 30 days.",
  "h6":"You can recite it. But do you understand it?",
  "h7":"Struggling to learn Arabic? You're not alone.",
  "h8":"The Arabic alphabet looks impossible. It isn't."},
 "beat":{
  "path":"No guessing what to study: one path, one Continue button, steps of 5 to 10 minutes.",
  "vowels":"Every word fully vowelled, spoken by a native Arabic voice, with a picture.",
  "srs":"Words you've learned come back for review just as you're about to forget them, so they stick.",
  "chat":"Reply to a real conversation in your own words, and find out instantly if it makes sense.",
  "weak":"It notices the mistakes you keep making, and gives you practice on exactly those.",
  "scenes":"Practise real situations: the airport, the doctor, the masjid, a taxi.",
  "reading":"Can't read the script yet? Start with the 28 letters and the vowel marks.",
  "progress":"Watch your streak and your word count grow, with goals based on memory research.",
  "placement":"A two-minute check puts you in the right place from day one.",
  "units":"Twelve units, from greetings and family to prayer, work and travel."},
 "close":{
  "c1":"A few minutes a day. Arabic that stays.",
  "c2":"Rafiq: your companion in learning Arabic.",
  "c3":"Try it free for a week at rafiq-arabic.com.",
  "c4":"Stop forgetting. Start speaking.",
  "c5":"Become fluent with Rafiq."}}
Q={
 "appeal":{"type":"score","instructions":"This line is from a short promotional video for an Arabic learning app. The viewer: `viewer`. How much would this line make the viewer want to keep watching and try the app?",
   "criteria":["Not at all: irrelevant, off-putting or not believable to them","A little","Clearly: it speaks to their situation","Strongly: they'd feel it was made for them"]},
 "true":{"type":"noul","instructions":"Facts about the app: `facts`. Is everything this line claims or implies about the app or about learners supported by these facts, with no exaggeration, invented statistics or promise of fluency? Line: `line`"},
 "clear":{"type":"noul","instructions":"For someone who has never heard of this app, does the line `line` make clear something concrete the app does or why it helps?"}}
jobs=[(k,cid,v) for k in C for cid in C[k] for v in VIEWERS]
def run(j):
    k,cid,v=j; qs={"appeal":Q["appeal"]}
    if v=="quran": qs["true"]=Q["true"]; qs["clear"]=Q["clear"]
    return j, ask({"line":C[k][cid],"viewer":VIEWERS[v],"facts":FACTS}, qs)
with ThreadPoolExecutor(8) as ex: res=dict(ex.map(run,jobs))
json.dump({f"{a}|{b}|{c}":r for (a,b,c),r in res.items()},open("story-out.json","w"),indent=1)
for k in C:
    print(f"\n== {k}: appeal 0-3 per viewer ({', '.join(VIEWERS)}) | mean | true | clear")
    rows=[]
    for cid,line in C[k].items():
        ap=[res[(k,cid,v)]["answers"]["appeal"]["score"] for v in VIEWERS]
        tr=res[(k,cid,"quran")]["answers"]["true"]["noul"]; cl=res[(k,cid,"quran")]["answers"]["clear"]["noul"]
        rows.append((sum(ap)/len(ap),cid,ap,tr,cl,line))
    for m,cid,ap,tr,cl,line in sorted(rows,reverse=True):
        print(f"{cid:9} {' '.join(f'{a:.1f}' for a in ap)} | {m:.2f} | {tr:.2f} | {cl:.2f} | {line}")
