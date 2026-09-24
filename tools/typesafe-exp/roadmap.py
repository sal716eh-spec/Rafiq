# Weigh what's left to build (Sept 2026). Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/roadmap.py
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
CTX=("Rafiq is a web app (rafiq-arabic.com) teaching Modern Standard Arabic, mostly to Muslim adults in the UK: one daily path of short steps, "
 "spaced-repetition review, a conversation partner and AI answer checks, native audio. It is in free beta: everyone gets the top plan, no payments yet. "
 "Plans planned: Essentials £6.99/mo, Complete £11.99/mo, 7-day trial. Accounts use Supabase email+password sign-up; there is no password reset, "
 "no privacy policy page, no welcome email, no admin view. Built and run by one founder with an AI coding assistant.")
O={
 "admin":"Admin account: a dashboard listing every user and their progress (steps done, words learned, streak, last active), with everything unlocked for the admin.",
 "teacher":"Teacher/class accounts: a teacher creates a class, students join with a code, the teacher sets homework (units, steps, word sets) and sees each student's progress; sold to schools, madrasas and mosques.",
 "email":"Working sign-up: email verification, a branded welcome email from rafiq-arabic.com (custom SMTP), and a 'forgot password' reset.",
 "stripe":"Stripe payments: checkout for both plans with the 7-day trial, a webhook that sets each user's plan, a 'manage subscription' link, then switch off the free beta.",
 "legal":"Privacy policy, terms, cookie notice and a 'delete my account / export my data' option (UK GDPR).",
 "reminders":"Daily reminders: an opt-in email or push notification at the learner's chosen time to protect their streak, plus installable app (PWA) polish.",
 "analytics":"Product analytics and a feedback button: see where people drop off (sign-up, first lesson, day 2, day 7) and let learners report a wrong answer or bug in one tap.",
 "quran":"A Quran & prayer track: the words and phrases of Al-Fatiha, the short surahs and the daily prayers, taught with the same path and review.",
 "speaking":"Speech recognition: the learner speaks their reply aloud and gets feedback on pronunciation and meaning, not just typed replies.",
 "mobile":"Native iOS/Android apps in the app stores.",
 "referral":"Referral and gift subscriptions: invite a friend for a free month; gift a year (e.g. for Ramadan).",
}
Q={"success":{"type":"score","instructions":"`ctx` Candidate next piece of work: `option`. How much would it raise the product's chance of commercial success in the next 6 months?","criteria":["Barely","Somewhat","A lot","Crucial"]},
   "friendly":{"type":"score","instructions":"`ctx` Candidate: `option`. How much would it make the product easier or more pleasant for learners (or teachers)?","criteria":["Barely","Somewhat","A lot","Hugely"]},
   "blocker":{"type":"score","instructions":"`ctx` Candidate: `option`. Must this be done before the product can responsibly charge real customers and grow publicly?","criteria":["Not needed","Nice first","Should do first","Must do first"]},
   "effort":{"type":"score","instructions":"`ctx` Candidate: `option`. How big a job is it for one founder with an AI coding assistant?","criteria":["Months","Weeks","Days","Hours"]}}
with ThreadPoolExecutor(6) as ex: r=dict(ex.map(lambda k:(k,ask({"ctx":CTX,"option":O[k]},Q)),O))
rows=[(k,*(r[k]["answers"][q]["score"] for q in Q)) for k in O]
rows.sort(key=lambda x:-(x[1]+x[2]+1.5*x[3]+0.5*x[4]))
print("item       success friendly blocker ease   total")
for k,s,f,b,e in rows: print(f"{k:10} {s:.2f}    {f:.2f}     {b:.2f}    {e:.2f}   {s+f+1.5*b+0.5*e:.2f}")
