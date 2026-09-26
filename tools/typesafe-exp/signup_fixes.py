# Sign-up / onboarding fixes: which first? Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/signup_fixes.py
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

CTX=("Rafiq is a web app teaching Modern Standard Arabic to adult beginners (mostly UK Muslims), used mostly on phones, about to launch. "
 "Sign-up today: create account -> a small green line of text under the form says 'we've emailed you a link' -> the learner taps the link in their mail app, "
 "which often opens a different browser from the one they signed up in -> 4 quick questions -> (if they know some Arabic) a placement check where they "
 "type 6 English sentences in Arabic -> a one-time 79-second 'how it works' video -> Home. "
 "Found in testing: a tester confirmed in their everyday browser and landed straight on Home, skipping the questions and the video, because "
 "'already onboarded' and 'already saw the video' are remembered per browser, not per account. On the placement check the sentence "
 "'And peace be upon you - welcome! What's your name?' confused the tester: it reads as if the app is greeting them and asking their name.")
T={"A_onboard_per_account":"Remember 'finished the questions' per account, not per browser, so a new account always gets the questions.",
   "B_confirm_to_questions":"When the confirm link is opened, go straight to the questions (not Home first then a redirect).",
   "C_video_per_account":"Remember 'saw the how-it-works video' per account, so every new account is offered it once.",
   "D_check_email_screen":"Replace the small green line with a proper 'Check your email' screen: envelope, the address it went to, resend with a countdown, 'wrong email?', check spam.",
   "E_auto_continue":"If the learner comes back to the sign-up tab after confirming, carry on automatically (and an 'I've confirmed' button).",
   "F_placement_wording":"Placement: say 'Write this in Arabic', show the sentence in quotes as something to translate, and '1 of 6'.",
   "G_placement_keyboard":"Placement: give the answer box the app's own Arabic keyboard (phones may have no Arabic keyboard installed) and a placeholder.",
   "H_three_questions_copy":"The questions screen says 'Three quick questions' but there are four: fix the text.",
   "I_story_video_on_check_email":"Play the 88-second story video on the 'check your email' screen (the video file isn't ready yet)."}
Q={"harm":{"type":"score","instructions":"`ctx` Task: `t`. If this is NOT done before launch, how much does it hurt new learners (confusion, wrong experience, dropping out)?","criteria":["Not at all","A little","Quite a lot","A lot"]},
   "gain":{"type":"score","instructions":"`ctx` Task: `t`. Once done, how much does it improve the first 10 minutes for a new learner?","criteria":["Not at all","A little","Quite a lot","A lot"]},
   "effort":{"type":"score","instructions":"`ctx` Task: `t`. For a developer who knows this small static web app, how much work is it?","criteria":["Minutes","An hour or two","Half a day","Days"]}}
with ThreadPoolExecutor(9) as ex: r=dict(ex.map(lambda k:(k,ask({"ctx":CTX,"t":T[k]},Q)["answers"]),T))
rows=sorted(((k, r[k]['harm']['score'], r[k]['gain']['score'], r[k]['effort']['score']) for k in T), key=lambda x:-(x[1]+x[2]-0.5*x[3]))
print("task                           harm  gain  effort | priority")
for k,h,g,e in rows: print(f"{k:30} {h:.2f}  {g:.2f}  {e:.2f}   | {h+g-0.5*e:.2f}")
