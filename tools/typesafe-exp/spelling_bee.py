# Should Practise get a Spelling bee? Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/spelling_bee.py
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

APP=("Rafiq is a web app teaching Modern Standard Arabic to adult beginners (mostly UK Muslims). One daily path of short steps. "
 "Existing practice: word reviews are flashcards (see the Arabic, reveal the meaning, rate yourself); a daily vocab test where you type the ENGLISH meaning "
 "or pick from multiple choice; sentence drills where you type whole Arabic sentences (checked by AI); a conversation partner; weak-spots review; real-life scenes; "
 "redo a unit. An on-screen Arabic keyboard exists. Nothing currently asks the learner to spell a single Arabic word from memory.")
LEARNERS={
 "beginner":"a complete beginner, three weeks in, still slow at reading the script",
 "quran":"a Muslim learner whose main goal is to understand the Quran and prayers; reads Arabic script already but knows little vocabulary",
 "busy":"a busy professional doing 10 minutes a day on their phone",
 "heritage":"a heritage speaker who understands spoken Arabic but can barely write it",
}
O={
 "bee_en":"Spelling bee: see the English word (and emoji), type the Arabic word from memory; letters are checked one by one and wrong letters are highlighted. Unlimited rounds on words already learned.",
 "bee_audio":"Spelling bee (listening): hear the native voice say a word already learned, type it in Arabic; then see the English. Letters checked one by one, wrong letters highlighted. Unlimited rounds.",
 "bee_mix":"Spelling bee with both: alternates hearing the word and seeing the English; type the Arabic word; letter-by-letter feedback; vowel marks optional; mistakes come back in the same round; results also feed spaced repetition. Unlimited rounds on words already learned.",
 "none":"Add nothing new to Practise; learners keep using the existing flashcards, English-meaning test and sentence drills.",
}
Q={"useful":{"type":"score","instructions":"`app` The learner: `learner`. Proposed addition to the Practise section: `option`. How useful would this be for this learner's progress?","criteria":["Not useful","A little","Useful","Very useful"]},
   "use":{"type":"score","instructions":"`app` The learner: `learner`. Proposed: `option`. How likely is this learner to come back and use it regularly of their own accord?","criteria":["Unlikely","Maybe","Likely","Very likely"]},
   "new":{"type":"score","instructions":"`app` Proposed: `option`. How much does it add that the existing practice does not already cover?","criteria":["Nothing","A little","A fair amount","A lot"]},
   "frustr":{"type":"score","instructions":"`app` The learner: `learner`. Proposed: `option`. How frustrating would it feel (hard typing, fussy about tiny marks)?","criteria":["Not at all","A little","Quite","Very"]}}
jobs=[(o,l) for o in O for l in LEARNERS]
with ThreadPoolExecutor(8) as ex: res=dict(ex.map(lambda j:(j,ask({"app":APP,"learner":LEARNERS[j[1]],"option":O[j[0]]},Q)["answers"]),jobs))
print("option      "+"  ".join(f"{l[:8]:>8}" for l in LEARNERS)+"   | useful  use   new  frustr (avg)")
for o in O:
    rs=[res[(o,l)] for l in LEARNERS]; avg=lambda q:sum(r[q]["score"] for r in rs)/len(rs)
    print(f"{o:10}  "+"  ".join(f"{res[(o,l)]['useful']['score']:8.2f}" for l in LEARNERS)+f"   | {avg('useful'):.2f}   {avg('use'):.2f}  {avg('new'):.2f}  {avg('frustr'):.2f}")

# How strict about vowel marks?
V={"required":"The learner must type every vowel mark (fatha, damma, kasra, sukun, shadda) exactly for the word to count as right.",
   "optional":"Only the letters must be right; vowel marks are optional and ignored when checking; the fully vowelled word is shown after each answer.",
   "bonus":"Letters must be right to pass; vowel marks are optional, but typing them correctly earns a 'fully vowelled ✓' bonus; the vowelled word is always shown after."}
QV={"learn":{"type":"score","instructions":"`app` Planned: a spelling bee where the learner types learned Arabic words. Rule for vowel marks: `rule`. The learner: `learner`. How well does this rule help them learn?","criteria":["Poorly","OK","Well","Very well"]},
    "frustr":Q["frustr"]}
QV["frustr"]={**Q["frustr"],"instructions":"`app` Planned spelling bee. Vowel-mark rule: `rule`. The learner: `learner`. How frustrating would it feel?"}
jobs=[(v,l) for v in V for l in LEARNERS]
with ThreadPoolExecutor(8) as ex: rv=dict(ex.map(lambda j:(j,ask({"app":APP,"learner":LEARNERS[j[1]],"rule":V[j[0]]},QV)["answers"]),jobs))
print("\nvowel rule   learn  frustr")
for v in V: print(f"{v:10}  {sum(rv[(v,l)]['learn']['score'] for l in LEARNERS)/4:.2f}   {sum(rv[(v,l)]['frustr']['score'] for l in LEARNERS)/4:.2f}")
