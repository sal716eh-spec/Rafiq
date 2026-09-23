import json
exec(open('story.py').read().split('FACTS=')[0])
from concurrent.futures import ThreadPoolExecutor
VIDEO=("A 60-second promo for Rafiq (رَفِيق, 'companion'), an app for learning Modern Standard Arabic aimed at Muslims in the UK. "
 "Paper-and-ink visuals, no music (natural sounds only), a warm female English narrator, and short native Arabic clips. "
 "The name Rafiq is spoken three times: 'Meet Rafiq, your companion in learning Arabic', 'Rafiq remembers what you've learned…', 'Try Rafiq free…'. "
 "The current narrator pronounces Rafiq in an English way ('RAH-fick') instead of the Arabic رَفِيق (ra-FEEQ, with a deep q).")
def run(qs, opts, extra=None):
    with ThreadPoolExecutor(6) as ex:
        return dict(ex.map(lambda k:(k,ask({"video":VIDEO,"option":opts[k],**(extra or {})},qs)),opts))
# 1) the voice question
VO={
 "one_fixed":"Keep one female narrator for everything, and fix only the pronunciation of Rafiq.",
 "duet":"Two voices take turns: the female narrator tells the learner's story (the problem), and a warm male native Arabic speaker speaks the lines about Rafiq, so the name is always said the Arabic way. The switch happens at 'Meet Rafiq', like the companion introducing himself.",
 "duet_alt":"Two voices alternate sentence by sentence throughout the whole video, female then male.",
 "male_only":"Replace the narrator with one male native Arabic speaker for the whole video.",
 "male_name_only":"Keep the female narrator but splice in a male voice saying only the word 'Rafiq' each time."}
QV={"natural":{"type":"score","instructions":"`video` Proposed voice approach: `option`. How natural and polished would this sound to viewers?","criteria":["Odd or jarring","Acceptable","Natural","Very natural and polished"]},
    "engage":{"type":"score","instructions":"`video` Proposed voice approach: `option`. How much would it make the video more engaging and memorable?","criteria":["Less engaging","No change","More engaging","Much more engaging"]},
    "auth":{"type":"noul","instructions":"`video` Proposed voice approach: `option`. Would Arabic-speaking and Muslim viewers feel the brand name and Arabic are treated authentically?"}}
r=run(QV,VO)
print("VOICE        natural engage authentic")
for k in VO: a=r[k]["answers"]; print(f"{k:14} {a['natural']['score']:.2f}   {a['engage']['score']:.2f}   {a['auth']['noul']:.2f}")
# 2) the opening sound
OP={"ping":"A single bright notification ping.",
    "chime":"A single soft, clear bell-like chime that rings out.",
    "qalam":"A sharp, close reed-pen stroke on paper, like the first stroke of calligraphy, slightly loud and crisp.",
    "knock":"Two crisp wooden knocks, like knocking on a door.",
    "whoosh":"A quick airy whoosh as the first word card flies in.",
    "pageslam":"A book closing firmly with a soft thud.",
    "word":"No effect: the native Arabic voice saying the first word, as now."}
QO={"attn":{"type":"score","instructions":"`video` It opens with: `option` right at 0 seconds, before the Arabic voice says the first word. How well does this grab attention in the first second on social media?","criteria":["Not at all","A little","Clearly","Strongly"]},
    "fit":{"type":"score","instructions":"`video` It opens with: `option`. How well does it fit the calm, paper-and-ink, Islamic-friendly brand?","criteria":["Poor","Acceptable","Good","Perfect"]},
    "halal":{"type":"noul","instructions":"`video` It opens with: `option`. Would practising Muslims who avoid music consider this acceptable?"}}
r=run(QO,OP)
print("\nOPENER      attention fit  halal")
for k in OP: a=r[k]["answers"]; print(f"{k:10}  {a['attn']['score']:.2f}   {a['fit']['score']:.2f}  {a['halal']['noul']:.2f}")
# 3) answer sounds in the app
APP=("In the Rafiq learning app, after a learner answers a question (multiple choice, typed answer, or a quiz), a short sound plays. "
     "It is used many times per session, on phones, often in public.")
AN={"soft_chime":"Correct: a soft two-note rising chime. Wrong: a soft low single 'bonk'.",
    "bright_ping":"Correct: a bright high ping. Wrong: a buzzer.",
    "wood":"Correct: a warm wooden 'tock' followed by a light higher 'tick' (natural wood blocks). Wrong: a soft muted low wooden thud.",
    "pen":"Correct: a crisp pen tick like a teacher's check mark on paper. Wrong: a soft paper rustle.",
    "pop":"Correct: a gentle bubbly pop. Wrong: a soft descending 'whomp'."}
QA={"clear":{"type":"score","instructions":"`app` Sounds: `option`. How clearly does a learner instantly tell correct from wrong by ear?","criteria":["Unclear","Somewhat","Clear","Unmistakable"]},
    "pleasant":{"type":"score","instructions":"`app` Sounds: `option`. How pleasant is it to hear dozens of times, without being annoying or discouraging on a wrong answer?","criteria":["Annoying or discouraging","Tolerable","Pleasant","Very pleasant"]},
    "halal":{"type":"noul","instructions":"`app` Sounds: `option`. Would practising Muslims who avoid music consider these sounds acceptable (not music)?"}}
with ThreadPoolExecutor(6) as ex: r=dict(ex.map(lambda k:(k,ask({"app":APP,"option":AN[k]},QA)),AN))
print("\nANSWERS     clear pleasant halal")
for k in AN: a=r[k]["answers"]; print(f"{k:11} {a['clear']['score']:.2f}  {a['pleasant']['score']:.2f}   {a['halal']['noul']:.2f}")
