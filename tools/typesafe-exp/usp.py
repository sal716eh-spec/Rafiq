# What is Rafiq's real USP, is it commercially valuable, what would strengthen it, how to market it.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/usp.py
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


BUILT=("WHAT RAFIQ IS (from its code, Sept 2026): a web app (no native app yet) teaching Modern Standard Arabic to adult beginners, roughly A1-A2: "
 "a reading starter (letters, vowel marks), then 12 units (greetings, family, housing, daily life, food, PRAYER, study, work, shopping, weather, people & places, hobbies), "
 "779 words, all fully vowelled, 2,357 native-voice audio clips. One path with one Continue button, 5-10 minute steps. Spaced repetition of words and sentences met in lessons. "
 "AI checking of free-typed Arabic: translate-into-Arabic answers, rewrites, and conversation replies are judged for meaning and grammar, naming the error type "
 "(gender agreement, wrong person/tense, missing word...). A conversation partner: pre-written dialogues where the learner replies in their own words and the AI checks the reply fits "
 "and that the partner's next line still follows. A mistake profile that notices repeat error types and a weak-spots review built from them. Six real-life scenes "
 "(airport, doctor, MASJID, restaurant, taxi, visiting a family). Islamic greetings and a prayer unit; no music (halal-conscious). Progress page, streaks. "
 "Planned price £6.99 / £11.99 a month, 7-day trial. Tiny team, no users or brand yet.")
COMP=("COMPETITORS (2026): Duolingo Arabic (free, MSA, fully vowelled, gamified, tops out at beginner; its AI roleplay/video call is NOT offered for Arabic); "
 "Busuu (CEFR MSA, native-speaker community corrections, thin content); Pimsleur (audio-only, MSA/Levantine); ArabicPod101; Mondly/Memrise/Drops; "
 "AI chat apps: Yallah Speak, Talkpal, Promova, Parallel Arabic, Fusha Connect (open-ended AI conversation with corrections, many dialects incl. Fusha); "
 "Quran-focused: Quranic (gamified Quranic vocabulary, big among Muslims), Quranle, Quranlingo, Kalaam, Bayyinah TV ($11/mo video courses by Nouman Ali Khan); "
 "Madinah Arabic (free classical grammar), NaTakallam, Kaleela; human tutors on italki/Preply (~£10-25/hour); local madrasas and evening classes.")
CTX=BUILT+" "+COMP
BUYERS={"muslim":"a UK Muslim adult (25-40) who prays in Arabic, wants to understand it and to be able to speak/read basic Arabic, has tried apps before and quit",
 "revert":"a recent convert to Islam who cannot read Arabic script yet",
 "parent":"a Muslim parent choosing something for themself and their 12-year-old who attends weekend madrasa",
 "general":"a non-Muslim professional or traveller who wants to learn Arabic for work or travel in the Gulf",
 "teacher":"an Arabic teacher at a UK weekend madrasa or Islamic school looking for something to set as homework"}
USP={"vowelled":"Clear, fully vowelled MSA with a native voice for every word, on one simple daily path.",
 "ai_check":"Write real Arabic from day one and get instant feedback that names your actual mistake (e.g. gender agreement), then practise exactly the mistakes you keep making.",
 "guided_convo":"Conversations that stay at your level: you reply in your own words to a real dialogue and the app checks you, instead of an open-ended chatbot that drifts beyond you.",
 "muslim_msa":"The everyday-Arabic course made for Muslims: fully vowelled MSA with prayer, masjid and Islamic greetings woven in, no music, bridging 'I can recite' and 'I can understand and speak'.",
 "srs":"Words come back just before you'd forget them, so they finally stick.",
 "combo":"The only Arabic course for Muslims that makes you produce Arabic, not just recognise it: a structured, fully vowelled MSA path with prayer and masjid life built in, where AI checks every sentence you write and every reply you give, and drills the mistakes you personally keep making."}
QU={"distinct":{"type":"score","instructions":"`ctx` Candidate selling point for Rafiq: `usp`. How clearly does this set Rafiq apart from the competitors listed (would a buyer see it as different, not 'yet another app')?","criteria":["Not at all","Slightly","Clearly","Strongly"]},
    "true":{"type":"score","instructions":"`ctx` Candidate selling point: `usp`. How fully does what is actually built back up this claim today?","criteria":["Not backed","Partly","Mostly","Fully"]},
    "defend":{"type":"score","instructions":"`ctx` Candidate selling point: `usp`. How hard would it be for Duolingo, Quranic or an AI chat app to copy within a year?","criteria":["Trivial","Easy","Hard","Very hard"]}}
QB={"want":{"type":"score","instructions":"`ctx` Buyer: `buyer`. Selling point: `usp`. How much does this buyer care about it?","criteria":["Not at all","A little","A lot","It's exactly what they want"]},
    "pay":{"type":"score","instructions":"`ctx` Buyer: `buyer`. If Rafiq delivered on this selling point, how likely would this buyer pay £7-12 a month after the free trial?","criteria":["Very unlikely","Unlikely","Likely","Very likely"]}}
def run(jobs,fn):
    with ThreadPoolExecutor(8) as ex: return dict(ex.map(lambda j:(j,fn(j)),jobs))
S=lambda r,q:r[q]["score"]
print("== 1. Which selling point is real?  (0-3)")
u=run(list(USP),lambda k:ask({"ctx":CTX,"usp":USP[k]},QU)["answers"])
b=run([(k,x) for k in USP for x in BUYERS],lambda j:ask({"ctx":CTX,"usp":USP[j[0]],"buyer":BUYERS[j[1]]},QB)["answers"])
print("usp           distinct true  defend | want: "+" ".join(f"{x[:7]:>7}" for x in BUYERS)+" | pay avg")
for k in USP:
    print(f"{k:12}  {S(u[k],'distinct'):.2f}     {S(u[k],'true'):.2f}  {S(u[k],'defend'):.2f}   |       "+" ".join(f"{S(b[(k,x)],'want'):7.2f}" for x in BUYERS)+f" | {sum(S(b[(k,x)],'pay') for x in BUYERS)/len(BUYERS):.2f}")
print("   pay by buyer (combo): "+", ".join(f"{x} {S(b[('combo',x)],'pay'):.2f}" for x in BUYERS))

print("\n== 2. Commercial value of Rafiq as built today")
QC={"viable":{"type":"noul","instructions":"`ctx` As built today and positioned as: `usp`. Is there a real, reachable paying market for this (enough to support a small business of a few thousand subscribers)?"},
    "vsfree":{"type":"noul","instructions":"`ctx` Positioned as: `usp`. Would most target buyers see enough reason to pay rather than use free Duolingo Arabic plus free Quranic?"},
    "special":{"type":"noul","instructions":"`ctx` Positioned as: `usp`. Is Rafiq, as built today, special rather than 'another Duolingo'?"}}
c=ask({"ctx":CTX,"usp":USP["combo"]},QC)["answers"]
for q in QC: print(f"  {q:8} p(yes)={c[q]['probability'] if 'probability' in c[q] else c[q]}")

print("\n== 3. What would make it more special and more commercially successful?")
IMP={"quran_bridge":"A 'from salah to speaking' bridge: every unit links everyday words to the same roots in the prayers and short surahs you already recite (e.g. رَبّ, عِلْم, كَتَبَ), so each lesson also unlocks meaning in your salah.",
 "salah_track":"A dedicated track to understand every word of the daily prayers and the last 10 surahs, reviewed with spaced repetition.",
 "speaking_ai":"Speak your replies aloud and get AI feedback on meaning, grammar and pronunciation of hard letters (ع ح ق ض).",
 "madrasa_b2b":"Madrasa & Islamic-school edition: teacher dashboard, classes, homework, per-student mistake reports; sold per school.",
 "gcse":"Align content with UK GCSE Arabic (MSA) and market to parents of teens taking it.",
 "family":"Family plan: parent and children learn together, with a kids mode and shared family streak.",
 "outcome":"A measurable promise: a placement test and a monthly 'can-do' check (e.g. 'understand Al-Fatiha word by word', 'introduce yourself'), with a certificate.",
 "tutor_hybrid":"Human tutor add-on: weekly 20-minute sessions with a vetted teacher who sees your mistake profile.",
 "dialects":"Add Egyptian and Levantine dialect courses.",
 "native_app":"Native iOS/Android apps."}
QI={"special":{"type":"score","instructions":"`ctx` Proposed addition: `imp`. How much more special and hard to copy would it make Rafiq versus the competitors?","criteria":["No change","A bit","A lot","Transformative"]},
    "money":{"type":"score","instructions":"`ctx` Proposed addition: `imp`. How much would it raise revenue potential within 12 months?","criteria":["Barely","Somewhat","A lot","Hugely"]},
    "effort":{"type":"score","instructions":"`ctx` Proposed addition: `imp`. How big a job for one founder with an AI coding assistant (plus hiring a teacher for content review if needed)?","criteria":["Many months","A few months","Weeks","Days"]}}
im=run(list(IMP),lambda k:ask({"ctx":CTX,"imp":IMP[k]},QI)["answers"])
print("addition       special money  ease   score(special+money+0.5ease)")
for k in sorted(IMP,key=lambda k:-(S(im[k],'special')+S(im[k],'money')+.5*S(im[k],'effort'))):
    print(f"{k:13}  {S(im[k],'special'):.2f}    {S(im[k],'money'):.2f}   {S(im[k],'effort'):.2f}   {S(im[k],'special')+S(im[k],'money')+.5*S(im[k],'effort'):.2f}")

print("\n== 4. How to market it")
MK={"masjid":"Partner with UK masjids and Islamic societies: a talk or stall after Jumu'ah, posters with a QR code, a free month for the congregation.",
 "isoc":"University Islamic societies (ISOCs): ambassador program, society-wide free access, Ramadan challenges.",
 "madrasa_pilot":"Pilot free with 3-5 weekend madrasas / Islamic schools, then sell class licences and let pupils bring parents in.",
 "influencers":"Paid and gifted partnerships with Muslim content creators and Islamic YouTubers/TikTokers (UK and US).",
 "own_content":"Own short-form content: daily 30-second videos on TikTok/Instagram/YouTube Shorts (e.g. 'what you're saying in salah, word by word', a word a day).",
 "ramadan":"A Ramadan campaign: '30 days to understand your salah', gift subscriptions, launched two weeks before Ramadan.",
 "seo":"SEO content: guides and free tools (e.g. 'meaning of every word in Al-Fatiha', an Arabic keyboard, vowel-mark guide) ranking on Google.",
 "paid_ads":"Paid Meta/TikTok/Google ads targeting UK Muslims interested in learning Arabic.",
 "referral":"Referral program: a free month for you and a friend; family and gift plans.",
 "product_hunt":"Launch on Product Hunt, Hacker News, and general tech press.",
 "app_store":"Get into the App Store / Google Play (ASO) as a native app."}
QM={"reach":{"type":"score","instructions":"`ctx` Marketing channel for Rafiq at launch: `mk`. How well does it reach people likely to pay for Rafiq?","criteria":["Poorly","Somewhat","Well","Very well"]},
    "cheap":{"type":"score","instructions":"`ctx` Channel: `mk`. How affordable is it for a bootstrapped founder with little money?","criteria":["Very costly","Costly","Affordable","Almost free"]},
    "convert":{"type":"score","instructions":"`ctx` Channel: `mk`. How well do people reached this way turn into loyal, paying subscribers?","criteria":["Poorly","Somewhat","Well","Very well"]},
    "trust":{"type":"score","instructions":"`ctx` Channel: `mk`. How much trust and word of mouth does it build in the Muslim community?","criteria":["None","A little","A lot","A great deal"]}}
mk=run(list(MK),lambda k:ask({"ctx":CTX+" Chosen positioning: "+USP["combo"],"mk":MK[k]},QM)["answers"])
print("channel        reach  cheap  convert trust  total")
for k in sorted(MK,key=lambda k:-sum(S(mk[k],q) for q in QM)):
    print(f"{k:13}  {S(mk[k],'reach'):.2f}   {S(mk[k],'cheap'):.2f}   {S(mk[k],'convert'):.2f}    {S(mk[k],'trust'):.2f}   {sum(S(mk[k],q) for q in QM):.2f}")

print("\n== 5. Commercial value again, with the top additions built")
for name,extra in [("+quran_bridge",IMP["quran_bridge"]),("+bridge+salah",IMP["quran_bridge"]+" "+IMP["salah_track"]),("+bridge+salah+madrasa",IMP["quran_bridge"]+" "+IMP["salah_track"]+" "+IMP["madrasa_b2b"])]:
    c2=ask({"ctx":CTX+" ALSO BUILT: "+extra,"usp":USP["combo"]+" Every lesson also opens up the meaning of your salah."},QC)["answers"]
    print(f"  {name:22} "+"  ".join(f"{q}={c2[q]['noul']:.2f}" for q in QC))
