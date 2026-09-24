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
from concurrent.futures import ThreadPoolExecutor
U1="Greetings & introductions: meeting a new neighbour"
C=[ # situation, earlier learner lines, previous line (en), learner reply, next line (en), follows?
 (U1,[],"Peace be upon you. I'm your new neighbour.","وعليكم السلام، أهلا وسهلا! ما اسمك؟","اسْمِي يُوسُفُ. وَأَنْتَ، ما اسْمُكَ؟","My name is Yusuf. And you, what's your name?",True),
 (U1,[],"Peace be upon you. I'm your new neighbour.","وعليكم السلام، أهلا وسهلا","اسْمِي يُوسُفُ. وَأَنْتَ، ما اسْمُكَ؟","My name is Yusuf. And you, what's your name?",True),
 (U1,[],"Peace be upon you. I'm your new neighbour.","وعليكم السلام. أنا سامر","اسْمِي يُوسُفُ. وَأَنْتَ، ما اسْمُكَ؟","My name is Yusuf. And you, what's your name?",False),
 (U1,["وعليكم السلام، ما اسمك؟"],"My name is Yusuf. And you, what's your name?","اسمي حمزة. من أين أنت يا يوسف؟","أَنا مِنَ الْمَغْرِبِ. وَأَنْتَ؟","I'm from Morocco. And you?",True),
 (U1,["وعليكم السلام، ما اسمك؟"],"My name is Yusuf. And you, what's your name?","اسمي سامر. من أين أنت؟","أَنا مِنَ الْمَغْرِبِ. وَأَنْتَ؟","I'm from Morocco. And you?",True),
 (U1,["وعليكم السلام، ما اسمك؟"],"My name is Yusuf. And you, what's your name?","اسمي سامر","أَنا مِنَ الْمَغْرِبِ. وَأَنْتَ؟","I'm from Morocco. And you?",False),
 (U1,["ما اسمك؟","اسمي حمزة. من أين أنت؟"],"I'm from Morocco. And you?","أنا سوداني. هل أنت طالب؟","لا، أَنا مُدَرِّسٌ. وَهَذا ابْنِي، هُوَ طالِبٌ.","No, I'm a teacher. And this is my son — he's a student.",True),
 (U1,["ما اسمك؟","اسمي حمزة. من أين أنت؟"],"I'm from Morocco. And you?","أنا من مصر. هل أنت طالب؟","لا، أَنا مُدَرِّسٌ. وَهَذا ابْنِي، هُوَ طالِبٌ.","No, I'm a teacher. And this is my son — he's a student.",True),
 (U1,["ما اسمك؟","اسمي حمزة. من أين أنت؟"],"I'm from Morocco. And you?","أنا من مصر","لا، أَنا مُدَرِّسٌ. وَهَذا ابْنِي، هُوَ طالِبٌ.","No, I'm a teacher. And this is my son — he's a student.",False),
 (U1,["ما اسمك؟","اسمي حمزة. من أين أنت؟"],"I'm from Morocco. And you?","أنا من بريطانيا. ما عملك؟","لا، أَنا مُدَرِّسٌ. وَهَذا ابْنِي، هُوَ طالِبٌ.","No, I'm a teacher. And this is my son — he's a student.",False),
 (U1,["ما اسمك؟","اسمي حمزة. من أين أنت؟","أنا سوداني. هل أنت طالب؟"],"No, I'm a teacher. And this is my son — he's a student.","ما شاء الله. أنا طبيب، وبيتي هنا.","تَشَرَّفْنا يا حَمْزَةُ.","Pleased to meet you, Hamza.",True),
 (U1,["ما اسمك؟","اسمي حمزة. من أين أنت؟","أنا سوداني. هل أنت طالب؟"],"No, I'm a teacher. And this is my son — he's a student.","ما شاء الله أين تسكن","تَشَرَّفْنا يا حَمْزَةُ.","Pleased to meet you, Hamza.",False),
 (U1,["ما اسمك؟","اسمي سامر. من أين أنت؟","أنا من مصر. هل أنت طالب؟"],"No, I'm a teacher. And this is my son — he's a student.","ما شاء الله","تَشَرَّفْنا يا حَمْزَةُ.","Pleased to meet you, Hamza.",False),
 (U1,["ما اسمك؟","اسمي حمزة. من أين أنت؟","أنا سوداني. هل أنت طالب؟"],"No, I'm a teacher. And this is my son — he's a student.","ما شاء الله","تَشَرَّفْنا يا حَمْزَةُ.","Pleased to meet you, Hamza.",True),
 ("Family: an Eid visit",[],"Mashallah! Who's this man?","هذا أبي","وَمَنْ هَذا الْوَلَدُ الصَّغِيرُ؟","And who's this little boy?",True),
 ("Family: an Eid visit",[],"Mashallah! Who's this man?","هذا عمي","وَمَنْ هَذا الْوَلَدُ الصَّغِيرُ؟","And who's this little boy?",True),
 ("Family: an Eid visit",[],"How many brothers do you have?","عندي ثلاثة إخوة وأختان","أُسْرَتُكَ كَبِيرَةٌ! وَأَيْنَ جَدُّكَ؟","Your family is big! And where's your grandfather?",True),
 ("Family: an Eid visit",[],"How many brothers do you have?","عندي أخ واحد","أُسْرَتُكَ كَبِيرَةٌ! وَأَيْنَ جَدُّكَ؟","Your family is big! And where's your grandfather?",False),
 ("At the masjid",[],"Over there, on the left.","ومتى صلاة العصر؟","بَعْدَ عَشْرِ دَقائِقَ.","In ten minutes.",True),
 ("At the masjid",[],"Over there, on the left.","متى صلاة المغرب؟","بَعْدَ عَشْرِ دَقائِقَ.","In ten minutes.",True),
 ("At the masjid",[],"Over there, on the left.","شكرا جزيلا","بَعْدَ عَشْرِ دَقائِقَ.","In ten minutes.",False),
 ("Ordering a meal",[],"Welcome. What would you like to eat?","أريد دجاجا من فضلك","وَماذا تَشْرَبُ؟","And what will you drink?",True),
 ("Ordering a meal",[],"Welcome. What would you like to eat?","أريد سمكا مع أرز","وَماذا تَشْرَبُ؟","And what will you drink?",True),
 ("Ordering a meal",[],"Welcome. What would you like to eat?","لا أريد شيئا، شكرا","وَماذا تَشْرَبُ؟","And what will you drink?",False),
]
Q={"follows":{"type":"noul","instructions":{
  "task":"In a beginner's Arabic conversation (`situation`), the other person said `previous_line`, and the learner replied `learner_reply`. Earlier in this conversation the learner said: `learner_earlier`. The other person's next line is already written: `next_line` (`next_line_en`). Does it make sense for them to say this right after the learner's reply?",
  "makes_sense":["it responds to what the learner said or asked","it moves the conversation on naturally, and the learner didn't just ask something it ignores"],
  "does_not":["it answers a question the learner did not ask","it reacts to information the learner did not give (e.g. 'your family is big' after one brother)","it uses a name or detail that contradicts what the learner said earlier (e.g. calls them Hamza when they said their name is Samer)","it ignores a question the learner just asked","it asks for something the learner already told them"]},
  "criteria":{"true":"Makes sense next","false":"Doesn't follow"}}}
def run(c):
    sit,ear,prev,rep,nxt,nen,lab=c
    r=ask({"situation":sit,"learner_earlier":ear or ["(nothing yet)"],"previous_line":prev,"learner_reply":rep,"next_line":nxt,"next_line_en":nen},Q)
    return r["answers"]["follows"]["noul"],lab,rep,nen
with ThreadPoolExecutor(8) as ex: out=list(ex.map(run,C))
for th in (0.4,0.5,0.6):
    acc=sum((p>=th)==lab for p,lab,_,_ in out); fa=sum(p>=th and not lab for p,lab,_,_ in out); fr=sum(p<th and lab for p,lab,_,_ in out)
    print(f"threshold {th}: {acc}/{len(out)} right · lets through {fa} that don't follow · blocks {fr} that do")
for p,lab,rep,nen in out:
    if (p>=0.5)!=lab: print(f"  miss {p:.2f} label={lab}  {rep}  →  {nen}")
