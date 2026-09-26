# Days, months, numbers, colours, time: own section or in the journey? Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/essentials.py
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


APP=("Rafiq teaches Modern Standard Arabic to adult beginners (mostly UK Muslims). Home = one path: a reading starter, then 12 themed units (greetings, family, housing, daily life, "
 "food, prayer, study, work, shopping, weather, people & places, hobbies), each a run of 5-10 minute steps (new words, conversation, grammar, practise, speak), with spaced review. "
 "A Practise area has extra sections (weak-spots review, spelling bee, 21 verbs in 3 tenses, joining words, real-life scenes, redo a unit). "
 "Today the 'everyday essentials' are patchy and scattered: 4 of 7 days (unit 3); no months on the path (9 Islamic months only in the word list; Ramadan, Sha'ban, Safar missing; "
 "no Western months); numbers 1-10 scattered over units 1-3 with 'six' missing; 11-19 not taught; 6 basic colours in unit 9 (shopping); no telling the time (half past, quarter past).")
L={"beginner":"a complete beginner three weeks in",
   "muslim":"a UK Muslim adult who wants to talk about prayer times, Ramadan and the Islamic calendar",
   "returning":"a learner at unit 8 who keeps forgetting numbers and days"}
O={"weave":"Weave them into the journey: fill the gaps inside the existing units where they fit (all 7 days and time-telling in daily life, numbers 1-20 early, the Islamic months in the prayer unit, colours in shopping).",
   "new_unit":"Add one new unit to the path, 'Numbers, days & time' (numbers 1-100, days, Islamic and Western months, telling the time, colours), placed early, after unit 3.",
   "practise_section":"Add an 'Everyday essentials' section in Practise (numbers, days, months, colours, time), each a short drill plus a quick-reference table, open any time; the path stays as it is.",
   "both":"Both: fill the gaps inside the journey where they fit, AND add an 'Everyday essentials' section in Practise for quick reference and extra drilling of the same sets.",
   "leave":"Leave it as it is."}
Q={"learn":{"type":"score","instructions":"`app` Learner: `learner`. Proposal: `option`. How well would this learner come to know numbers, days, months, colours and time?","criteria":["Poorly","OK","Well","Very well"]},
   "find":{"type":"score","instructions":"`app` Learner: `learner`. Proposal: `option`. How easily can they find or look up, say, the days or a number when they need it?","criteria":["Hard","OK","Easy","Very easy"]},
   "simple":{"type":"score","instructions":"`app` Proposal: `option`. How well does it keep the app simple and consistent with how it works now?","criteria":["Cluttered","OK","Clean","Very clean"]},
   "effort":{"type":"score","instructions":"`app` Proposal: `option`. How big a job (writing content, native audio, teacher checks)?","criteria":["Months","Weeks","A week","Days"]}}
with ThreadPoolExecutor(8) as ex: r=dict(ex.map(lambda j:(j,ask({"app":APP,"learner":L[j[1]],"option":O[j[0]]},Q)["answers"]),[(o,l) for o in O for l in L]))
print("option             learn  find  simple  ease  | total (learn+find+simple+0.5ease)")
rows=[]
for o in O:
    a=lambda q:sum(r[(o,l)][q]["score"] for l in L)/len(L)
    rows.append((o,a('learn'),a('find'),a('simple'),a('effort')))
for o,le,fi,si,ef in sorted(rows,key=lambda x:-(x[1]+x[2]+x[3]+.5*x[4])):
    print(f"{o:17}  {le:.2f}   {fi:.2f}  {si:.2f}    {ef:.2f}  | {le+fi+si+.5*ef:.2f}")

# refined: the Practise section, plus only the obvious holes in sets the units already teach
O2={"section_plus_holes":"Add an 'Everyday essentials' section in Practise (numbers, days, months incl. Islamic months, colours, time), each a short drill plus a quick-reference table, open any time; "
     "and in the journey only fill the obvious holes in sets already taught there (add Sunday, Monday, Wednesday to unit 3 next to the other days; add 'six' and 'two' next to the other numbers). No new unit."}
with ThreadPoolExecutor(8) as ex: r2=dict(ex.map(lambda j:(j,ask({"app":APP,"learner":L[j[1]],"option":O2[j[0]]},Q)["answers"]),[(o,l) for o in O2 for l in L]))
for o in O2:
    a=lambda q:sum(r2[(o,l)][q]["score"] for l in L)/len(L)
    print(f"{o:17}  {a('learn'):.2f}   {a('find'):.2f}  {a('simple'):.2f}    {a('effort'):.2f}  | {a('learn')+a('find')+a('simple')+.5*a('effort'):.2f}")
