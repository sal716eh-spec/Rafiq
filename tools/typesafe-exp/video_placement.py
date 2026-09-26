# Where should the three Rafiq videos go? Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/video_placement.py
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


CTX=("Rafiq is a web app teaching Modern Standard Arabic to adult beginners (mostly UK Muslims), used mostly on phones. "
 "Landing page (rafiq-arabic.com) order: hero with a sign-up button, a one-minute intro film, 'How a day works', 'What's inside', pricing, FAQ. "
 "Sign-up: create account, confirm email, then 4 quick questions (can you read Arabic, level, minutes a day, reason), then Home with one Continue button. "
 "Three videos exist: "
 "V6 'intro film' (62s): the learner's problem (words slip away), meet Rafiq, reading starter, native voice, spaced review, conversation reply, promise. Currently the landing page film. "
 "V7 'how it works' tutorial (79s): press Continue, the path and its steps, word tiles then typing, spaced review, Practise area (verbs, joining words, spelling bee), real-life scenes, AI naming your mistake, weak-spots review. "
 "V8 'the story' (88s): the name means companion, keeping words is the hard part, three findings from memory research (spacing, testing, habit) and how Rafiq uses them, then the reading starter; for anyone studying Arabic in a class, madrasa or alone.")
P={"land_v6_hero":"Landing page: keep V6 as the main film (it needs one line fixed).",
   "land_v8_hero":"Landing page: replace V6 with V8 'the story' as the main film.",
   "land_v7_hero":"Landing page: replace V6 with V7 'how it works' as the main film.",
   "land_v7_section":"Landing page: keep V6 as the main film, and put V7 in the 'What's inside' section as 'See how it works (79s)'.",
   "land_v8_section":"Landing page: keep V6 as the main film, and add V8 lower down as 'Why we built Rafiq (88s)' near the FAQ.",
   "onboard_v7_optional":"After sign-up, at the end of the 4 questions: 'Watch how Rafiq works (79s)' with a clear 'Skip, start my first lesson' button.",
   "onboard_v7_forced":"After sign-up, V7 plays before the first lesson and must be watched.",
   "home_v7_card":"On Home for the first week: a small dismissible card 'New here? See how Rafiq works (79s)' under the Continue button.",
   "settings_help":"In Settings: a 'How Rafiq works' video (V7) and 'Our story' (V8), always available.",
   "confirm_email_v8":"On the 'check your email to confirm' screen right after creating an account: V8 'the story' plays while they wait.",
   "social_only":"Use V7 and V8 only on social media (Instagram, TikTok, YouTube), not inside the site or app."}
PEOPLE={"visitor":"a first-time visitor on a phone deciding whether to sign up, who found Rafiq through a friend's WhatsApp",
        "new_user":"someone who has just signed up and wants to start learning",
        "week1":"a learner in their first week who hasn't explored beyond the Continue button"}
Q={"help":{"type":"score","instructions":"`ctx` Placement: `p`. Person: `who`. How helpful is this placement for this person at this moment?","criteria":["Not at all","A little","Helpful","Very helpful"]},
   "annoy":{"type":"score","instructions":"`ctx` Placement: `p`. Person: `who`. How much friction or annoyance does it add for them?","criteria":["None","A little","Some","A lot"]},
   "biz":{"type":"score","instructions":"`ctx` Placement: `p`. How much would it raise sign-ups and people sticking with Rafiq overall?","criteria":["Not at all","A little","A fair amount","A lot"]}}
jobs=[(k,w) for k in P for w in PEOPLE]
with ThreadPoolExecutor(10) as ex: r=dict(ex.map(lambda j:(j,ask({"ctx":CTX,"p":P[j[0]],"who":PEOPLE[j[1]]},Q)["answers"]),jobs))
rows=[]
for k in P:
    h={w:r[(k,w)]['help']['score'] for w in PEOPLE}; a=sum(r[(k,w)]['annoy']['score'] for w in PEOPLE)/3; b=sum(r[(k,w)]['biz']['score'] for w in PEOPLE)/3
    rows.append((k,h,a,b, sum(h.values())/3 + b - a))
print("placement             help: visitor new_user week1 | annoy  business | total")
for k,h,a,b,t in sorted(rows,key=lambda x:-x[4]):
    print(f"{k:20}        {h['visitor']:.2f}    {h['new_user']:.2f}    {h['week1']:.2f} |  {a:.2f}   {b:.2f}    | {t:.2f}")
