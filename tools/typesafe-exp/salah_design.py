# How should the salah feature appear in Rafiq? Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/salah_design.py
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



APP=("Rafiq: web app teaching Modern Standard Arabic to adult beginners, mostly UK Muslims. One daily path of 12 units (incl. a Prayer unit), 779 fully vowelled words, "
 "native audio, spaced repetition, AI-checked writing and conversation. Planned: help learners understand the words they say in salah (Al-Fatiha, takbir, ruku/sujud "
 "phrases, tashahhud, salawat, short surahs), since everyday MSA shares many roots with them (rabb, hamd, rahma, 'ilm, kataba, sami'a...).")
L={"muslim":"a UK Muslim adult who prays daily in Arabic but understands little of it, and is doing the everyday Arabic course",
   "revert":"a new Muslim who learned the prayer by sound and cannot yet read Arabic"}
O={"bridge":"Bridge cards inside the existing lessons: after a 'New words' step, if a word shares a root with something said in salah, show 'You'll hear this in your salah', the phrase with the word highlighted, and its meaning.",
   "track":"A separate 'Understand your salah' track: walks through the prayer in order (takbir, Al-Fatiha, ruku, sujud, tashahhud, salawat, taslim, then short surahs), word by word with meaning, root, audio, and spaced-repetition review.",
   "both":"Both: the 'Understand your salah' track, plus bridge cards in everyday lessons pointing to it, plus a 'Your salah' progress map showing which words of the prayer you now understand (known words lit up).",
   "map":"Only a 'Your salah' map: the full prayer text where words you already know from lessons are lit up, tap any word for its meaning; no separate lessons."}
Q={"value":{"type":"score","instructions":"`app` Learner: `learner`. Design: `option`. How much would it help this learner understand their salah?","criteria":["Barely","Somewhat","A lot","Transformative"]},
   "motiv":{"type":"score","instructions":"`app` Learner: `learner`. Design: `option`. How much would it motivate them to keep going with the everyday Arabic course too?","criteria":["Not at all","A little","A lot","Hugely"]},
   "effort":{"type":"score","instructions":"`app` Design: `option`. How big a job, given the content needs checking by a qualified teacher?","criteria":["Months","Weeks","A couple of weeks","Days"]}}
with ThreadPoolExecutor(8) as ex: r=dict(ex.map(lambda j:(j,ask({"app":APP,"learner":L[j[1]],"option":O[j[0]]},Q)["answers"]),[(o,l) for o in O for l in L]))
print("design   value  motivate  ease")
for o in O:
    a=lambda q:sum(r[(o,l)][q]["score"] for l in L)/len(L)
    print(f"{o:7}  {a('value'):.2f}   {a('motiv'):.2f}      {a('effort'):.2f}")
