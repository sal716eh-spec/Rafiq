# Which Arabic keyboard opens on phones, and how learners switch. Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/keyboard_choice.py
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


APP=("Rafiq is a web app teaching Modern Standard Arabic to adult beginners, used mostly on phones. Learners type Arabic answers. The app has its own on-screen "
 "Arabic keyboard (letters plus the vowel marks fatha, damma, kasra, sukun, shadda, which are hard to reach on phone keyboards). Today on phones BOTH the phone's "
 "own keyboard and the app keyboard open at once, covering the screen. Some learners have an Arabic keyboard installed on their phone; many beginners don't.")
L={"beginner":"a beginner with no Arabic keyboard installed on their phone",
   "native_kb":"a learner who already has an Arabic keyboard on their phone and types Arabic daily",
   "vowels":"a learner with an Arabic phone keyboard who sometimes wants to add vowel marks for the spelling bee bonus"}
O={"app_default":"Only one keyboard ever opens. By default the app keyboard (the phone keyboard is suppressed). A key on the app keyboard, 'Use my phone keyboard', switches to the phone's own keyboard and the choice is remembered; a small ⌨ button beside the answer box switches back. Also changeable in Settings.",
   "phone_default":"Only one keyboard ever opens. By default the phone's own keyboard. A small ⌨ 'Rafiq keyboard' button beside the answer box switches to the app keyboard and the choice is remembered; the app keyboard has a key to go back. Also in Settings.",
   "ask_once":"Only one keyboard ever opens. The first time a learner taps an Arabic answer box, a small prompt asks: 'Which keyboard? Rafiq keyboard (with vowel marks) / My phone's Arabic keyboard'. The choice is remembered, with a ⌨ button beside the box and a Settings option to change it.",
   "settings_only":"Only one keyboard ever opens: the app keyboard by default; learners can change it only in Settings."}
Q={"ease":{"type":"score","instructions":"`app` Learner: `learner`. Design: `option`. How easy and comfortable is typing answers for this learner?","criteria":["Frustrating","OK","Easy","Effortless"]},
   "find":{"type":"score","instructions":"`app` Learner: `learner`. Design: `option`. How likely is this learner to end up with the keyboard they prefer, without help?","criteria":["Unlikely","Maybe","Likely","Certain"]},
   "annoy":{"type":"score","instructions":"`app` Learner: `learner`. Design: `option`. How much friction or interruption does it add?","criteria":["None","A little","Some","A lot"]}}
with ThreadPoolExecutor(8) as ex: r=dict(ex.map(lambda j:(j,ask({"app":APP,"learner":L[j[1]],"option":O[j[0]]},Q)["answers"]),[(o,l) for o in O for l in L]))
print("design          ease  finds-pref  friction  total(ease+find-friction)")
for o in O:
    a=lambda q:sum(r[(o,l)][q]["score"] for l in L)/len(L)
    print(f"{o:14}  {a('ease'):.2f}  {a('find'):.2f}        {a('annoy'):.2f}      {a('ease')+a('find')-a('annoy'):.2f}")
    print("   by learner (ease):", {l: round(r[(o,l)]['ease']['score'],2) for l in L})
