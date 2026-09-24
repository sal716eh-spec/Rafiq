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
CTX=("A beginner Arabic app has a 'have the conversation' step: a partner's lines are fixed and pre-recorded (no text generation), "
 "the learner replies in their own words, and a judge checks each reply. Problem: the partner's next line was written expecting one particular reply, "
 "so if the learner says something sensible but different (e.g. says where they're from instead of asking 'are you a student?', or gives their own name), "
 "the partner's next line doesn't follow and the conversation stops making sense.")
O={
 "goal":"Before each reply, show the learner what to get across (e.g. 'Say where you're from and ask if he's a student'); they word it themselves, and the judge checks they covered it. The partner's next line then always follows.",
 "gate":"Let the learner reply freely. Before playing the partner's next line, the judge checks whether that line would make sense after what the learner actually said. If not, the app says 'Good Arabic! To keep this conversation going, also…' with the missing part, and the learner tries again or uses the suggested reply.",
 "both":"Combine both: a short goal shown before each reply, and the check that the partner's next line still follows, with a friendly nudge when it doesn't.",
 "branches":"Write several vetted partner lines for each turn in advance and have the judge pick the one that best follows the learner's reply.",
 "note":"Keep it as is, and tell the learner the partner follows a script."}
Q={"coherent":{"type":"score","instructions":"`ctx` Proposed fix: `option`. How reliably would the conversation make sense afterwards?","criteria":["Often broken","Sometimes broken","Rarely broken","Always makes sense"]},
   "freedom":{"type":"score","instructions":"`ctx` Proposed fix: `option`. How much real freedom and speaking practice does the learner keep?","criteria":["Little","Some","Good","A lot"]},
   "effort":{"type":"score","instructions":"`ctx` Proposed fix: `option`. How much new content has to be written and checked by a teacher for 12 conversations plus 6 scenes?","criteria":["A lot","A fair amount","A little","Almost none"]},
   "feel":{"type":"score","instructions":"`ctx` Proposed fix: `option`. How encouraging and natural does it feel for a beginner?","criteria":["Frustrating","OK","Good","Great"]}}
with ThreadPoolExecutor(5) as ex: r=dict(ex.map(lambda k:(k,ask({"ctx":CTX,"option":O[k]},Q)),O))
print("option    coherent freedom low-effort feel")
for k in O: a=r[k]["answers"]; print(f"{k:9} {a['coherent']['score']:.2f}     {a['freedom']['score']:.2f}    {a['effort']['score']:.2f}      {a['feel']['score']:.2f}")
