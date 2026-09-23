import json
exec(open('story.py').read().split('C={')[0])
LINES=[
 "You've tried to learn Arabic before.",
 "The script. The vowels. The words that never stick.",
 "You can recite it. But do you understand it?",
 "Meet Rafiq, your companion in learning Arabic.",
 "Can't read the script yet? Start with the letters.",
 "Then one path, one Continue button, five to ten minutes a day.",
 "Every word fully vowelled, and spoken by a native Arabic voice.",
 "Rafiq remembers what you've learned, and brings each word back just before you'd forget it.",
 "Then use it. Reply in your own words, and find out instantly if it makes sense.",
 "It notices the mistakes you keep making, and helps you fix them.",
 "A few minutes a day. Arabic that stays.",
 "Try Rafiq free at rafiq-arabic.com."]
Qt={"true":{"type":"noul","instructions":"Facts about the app: `facts`. Is everything this voiceover line claims or implies about the app supported by these facts, with no exaggeration, invented statistics or promise of fluency? A line that describes the viewer's own experience makes no claim about the app. Line: `line`"},
    "tone":{"type":"choice","instructions":"How does this voiceover line from an app promo come across to a thoughtful adult learner?","criteria":{"warm":"Warm and credible","neutral":"Neutral, informative","salesy":"Pushy or salesy","cringe":"Cheesy or cringeworthy"}}}
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(6) as ex:
    out=list(ex.map(lambda l: (l, ask({"line":l,"facts":FACTS},Qt)), LINES))
for l,r in out:
    a=r["answers"]; print(f'{a["true"]["noul"]:.2f}  {a["tone"]["choice"]:7} ({a["tone"]["probabilities"][a["tone"]["choice"]]:.2f})  {l}')
