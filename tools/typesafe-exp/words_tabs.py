# Are Words → Daily practise / Daily test redundant with Home's Review? Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/words_tabs.py
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


APP=("Rafiq teaches Modern Standard Arabic to adult beginners on one daily path. Home has a 'Review' button: a spaced-repetition session mixing "
 "due WORDS (flashcards: see the Arabic, say it aloud, reveal the meaning, rate yourself) and due SENTENCE exercises, from lessons done so far. It can be started any time, as often as the learner likes: when nothing is due it tops up with other learned words and sentences. "
 "Practise has: Weak-spots, Beyond the lessons, Real-life scenes, Redo a unit, and a Words page with three tabs: "
 "(1) 'Daily practise' — flashcards of the same due words, same schedule, same self-rating as Home's Review, then 'next 5' top-ups; "
 "(2) 'Daily test' — once a day, a quiz on due words: multiple choice in both directions (Arabic→English, English→Arabic) and, for well-known words, typing the English meaning; "
 "the app marks the answer (no self-rating), shows a score, and feeds the same spaced repetition; "
 "(3) 'Full list' of words met. A Spelling bee (type learned words in Arabic) is planned for Practise.")
LEARNERS={"beginner":"a complete beginner, three weeks in","busy":"a busy professional doing 10 minutes a day on their phone",
          "keen":"a keen learner who wants to practise words far more than the daily review offers"}
O={"keep":"Keep Words as it is: Daily practise, Daily test and Full list.",
   "drop_prac":"Remove the 'Daily practise' tab (Home's Review already covers it). Keep 'Daily test' and 'Full list'.",
   "merge":"Remove 'Daily practise'. Turn 'Daily test' into a 'Word quiz' in Practise that can be played any time (not once a day), marked by the app; keep 'Full list'.",
   "into_review":"Remove both tabs. Put the quiz question types (multiple choice, typed English) inside Home's Review instead of self-rated flashcards; keep only 'Full list'.",
   "drop_both":"Remove both 'Daily practise' and 'Daily test'; keep only 'Full list'. Home's Review is the one place to review words."}
Q={"learn":{"type":"score","instructions":"`app` The learner: `learner`. Proposal: `option`. How well would the learner's words be learned and retained afterwards?","criteria":["Worse than now","Same","A bit better","Much better"]},
   "clear":{"type":"score","instructions":"`app` The learner: `learner`. Proposal: `option`. How clear is it to this learner what to do each day and where to go?","criteria":["Confusing","OK","Clear","Very clear"]},
   "loss":{"type":"score","instructions":"`app` The learner: `learner`. Proposal: `option`. How much would this learner miss something valuable that the app used to offer?","criteria":["Nothing lost","A little","Quite a lot","A lot"]},
   "redund":{"type":"score","instructions":"`app` Proposal: `option`. After this change, how much duplication is left between the Words page and Home's Review?","criteria":["None","A little","Quite a lot","A lot"]}}
jobs=[(o,l) for o in O for l in LEARNERS]
with ThreadPoolExecutor(8) as ex: res=dict(ex.map(lambda j:(j,ask({"app":APP,"learner":LEARNERS[j[1]],"option":O[j[0]]},Q)["answers"]),jobs))
for o in O: print(o, {l: round(res[(o,l)]["loss"]["score"],2) for l in LEARNERS}, "learn", {l: round(res[(o,l)]["learn"]["score"],2) for l in LEARNERS})
print("option        learn  clear  loss   dupl   total (learn+clear-loss-dupl)")
for o in O:
    a=lambda q:sum(res[(o,l)][q]["score"] for l in LEARNERS)/len(LEARNERS)
    print(f"{o:12}  {a('learn'):.2f}   {a('clear'):.2f}   {a('loss'):.2f}   {a('redund'):.2f}   {a('learn')+a('clear')-a('loss')-a('redund'):.2f}")

# Once the Spelling bee (unlimited word-only practice, issue #36) exists:
O2={"keep+bee":"Add the Spelling bee to Practise and keep Words as it is (Daily practise, Daily test, Full list).",
    "bee_replaces":"Add the Spelling bee to Practise (unlimited rounds of learned words: hear it or see the English, type the Arabic, marked by the app, feeds spaced repetition) and remove the 'Daily practise' tab; keep 'Daily test' and 'Full list'."}
jobs=[(o,l) for o in O2 for l in LEARNERS]
with ThreadPoolExecutor(8) as ex: r2=dict(ex.map(lambda j:(j,ask({"app":APP,"learner":LEARNERS[j[1]],"option":O2[j[0]]},Q)["answers"]),jobs))
for o in O2:
    a=lambda q:sum(r2[(o,l)][q]["score"] for l in LEARNERS)/len(LEARNERS)
    print(f"{o:12}  {a('learn'):.2f}   {a('clear'):.2f}   {a('loss'):.2f}   {a('redund'):.2f}   {a('learn')+a('clear')-a('loss')-a('redund'):.2f}")
