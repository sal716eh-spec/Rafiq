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

# Where should the salah track live?
NAV=(" Current navigation: four tabs (Home, Practise, Progress, Settings). Home = the one daily path with a Continue button, plus a Review button. "
 "Practise = a menu of four buttons: Weak-spots, Beyond the lessons, Real-life scenes (six role-play conversations: airport, doctor, masjid, restaurant, taxi, family visit), Redo a unit; "
 "a Spelling bee is planned there too.")
P={"in_scenes":"Put the salah lessons inside 'Real-life scenes' as a seventh scene.",
   "practise_btn":"A new button in Practise called 'Your salah' (or 'Understand your salah'), opening its own step-by-step track.",
   "home_track":"On Home, a second track under the daily path: a 'Your salah' card with its own Continue button and progress ('Al-Fatiha: 18 of 29 words'), also reachable from Practise.",
   "own_tab":"A fifth tab in the bottom navigation called 'Salah'."}
QP={"find":{"type":"score","instructions":"`app``nav` Learner: `learner`. Placement: `option`. How easily would this learner find it and come back to it?","criteria":["Hard","OK","Easy","Very easy"]},
    "fit":{"type":"score","instructions":"`app``nav` Placement: `option`. How well does it fit what that part of the app is for, keeping the app simple and uncluttered?","criteria":["Poor fit","OK","Good fit","Perfect fit"]},
    "signal":{"type":"score","instructions":"`app``nav` Placement: `option`. How clearly does it show new visitors that understanding salah is a core part of Rafiq (its selling point)?","criteria":["Hidden","Somewhat","Clearly","Front and centre"]}}
with ThreadPoolExecutor(8) as ex: rp=dict(ex.map(lambda j:(j,ask({"app":APP,"nav":NAV,"learner":L[j[1]],"option":P[j[0]]},QP)["answers"]),[(o,l) for o in P for l in L]))
print("\nplacement      find  fit   signal  total")
for o in P:
    a=lambda q:sum(rp[(o,l)][q]["score"] for l in L)/len(L)
    print(f"{o:13}  {a('find'):.2f}  {a('fit'):.2f}  {a('signal'):.2f}    {a('find')+a('fit')+a('signal'):.2f}")

# How does the Home card work, and what is inside a salah lesson?
PATHDESC=(" The main course works like this: Home shows one Continue button; each unit is a run of 5-10 minute steps (meet 10 words, hear the conversation, "
 "how it works, practise, have the conversation...) opened in order; finished steps can be revisited; review of learned items is a separate Review button. "
 "The salah track would cover the prayer in order in about 10 parts: takbir, opening supplication, Al-Fatiha (2-3 parts), ruku, rising, sujud, tashahhud, "
 "salawat, taslim; then the short surahs.")
E={"straight":"Tapping the Home card's Continue goes straight into the next salah step, exactly like the main path. Nothing else.",
   "hub":"Tapping the card opens a Salah page with four sections the learner chooses between: Learn (explanations), Practise (exercises), Test (graded quiz), and Your salah map.",
   "hybrid":"The card has a Continue button that goes straight into the next salah step (like the main path). Tapping the card itself opens a Salah overview: the prayer in order, each part marked done / next / locked, a 'Your salah' map with understood words lit up, and a Review button; any finished part can be reopened."}
QE={"simple":{"type":"score","instructions":"`app``path` Learner: `learner`. How the salah track is entered: `option`. How simple is it to know what to do next?","criteria":["Confusing","OK","Simple","Effortless"]},
    "learn":{"type":"score","instructions":"`app``path` Learner: `learner`. Entry design: `option`. How well does it lead to real understanding of the prayer (not just skipping around)?","criteria":["Poorly","OK","Well","Very well"]},
    "return":{"type":"score","instructions":"`app``path` Learner: `learner`. Entry design: `option`. How likely are they to come back to it day after day?","criteria":["Unlikely","Maybe","Likely","Very likely"]},
    "consistent":{"type":"score","instructions":"`app``path` Entry design: `option`. How consistent is it with how the rest of the app works (so nothing new to learn)?","criteria":["Inconsistent","Somewhat","Consistent","Identical pattern"]}}
S={"words_first":"Each part: (1) Listen: hear the phrase recited, see it with its meaning; (2) Word by word: each word with meaning, root and a word you know from the course with the same root; (3) Check: match words to meanings; (4) Put it together: rebuild the phrase's meaning / order the words; (5) Follow along: hear it again with each word lit up as it is said. Review later with spaced repetition.",
   "explain_first":"Each part: (1) Explanation: a short paragraph on what this part of the prayer is and why it is said; (2) Word by word with meanings; (3) A graded quiz at the end.",
   "cards_only":"Each part: a set of flashcards of the words (Arabic on the front, meaning on the back), rated by the learner, then reviewed with spaced repetition."}
QS={"understand":{"type":"score","instructions":"`app` Learner: `learner`. Lesson design for one part of the prayer: `option`. How well will they understand what they say in that part of salah afterwards, and still know it a month later?","criteria":["Poorly","OK","Well","Very well"]},
    "feel":{"type":"score","instructions":"`app` Learner: `learner`. Lesson design: `option`. How engaging and meaningful does it feel?","criteria":["Dull","OK","Good","Moving"]}}
with ThreadPoolExecutor(8) as ex:
    re_=dict(ex.map(lambda j:(j,ask({"app":APP,"path":PATHDESC,"learner":L[j[1]],"option":E[j[0]]},QE)["answers"]),[(o,l) for o in E for l in L]))
    rs=dict(ex.map(lambda j:(j,ask({"app":APP,"learner":L[j[1]],"option":S[j[0]]},QS)["answers"]),[(o,l) for o in S for l in L]))
print("\nentry     simple learn return consistent total")
for o in E:
    a=lambda q:sum(re_[(o,l)][q]["score"] for l in L)/len(L)
    print(f"{o:9} {a('simple'):.2f}   {a('learn'):.2f}  {a('return'):.2f}   {a('consistent'):.2f}       {sum(a(q) for q in QE):.2f}")
print("\nlesson         understand feel")
for o in S:
    a=lambda q:sum(rs[(o,l)][q]["score"] for l in L)/len(L)
    print(f"{o:13}  {a('understand'):.2f}       {a('feel'):.2f}")
