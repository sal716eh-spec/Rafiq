"""Round 3b: the reply check with the conversation's situation. round3.py's
question judged only against the previous line, and rejected natural moves
such as a thank-you, giving the total, or asking the fare on arrival (7 of the
90 suggested replies scored < 0.7). Here the situation is part of the state.

Pass criteria: the 47 labelled replies (cases3.py), and every one of the 90
suggested replies from the unit dialogues and scenes must itself be judged a fit."""
import json, subprocess
from concurrent.futures import ThreadPoolExecutor
from run import ask, report
from cases3 import REPLY
from round3 import REPLY_Q as OLD

FITS = {"type": "noul", "instructions": {
    "task": "In a beginner's Arabic conversation (`situation`), the other person said `previous_line`. The learner "
            "replied `learner_reply`. Could this naturally be said next in this conversation?",
    "counts": ["an answer to a question, with the learner's own details (it need not match `suggested_reply`)",
               "a thank-you, an acknowledgement or a polite response to what was said",
               "a question or remark that naturally belongs to this situation at this point, as `suggested_reply` does"],
    "does_not_count": ["a remark about something unrelated to the situation or to what was just said",
                       "an answer to a different question from the one asked",
                       "a personal question out of the blue that ignores what was just said"],
    "note": "Ignore grammar and spelling here."},
    "criteria": {"true": "A natural next line", "false": "Doesn't follow on"}}
Q = {"fits": FITS, "grammar": OLD["grammar"]}

rows = json.loads(subprocess.check_output(["node", "-e", r'''
const fs=require("fs");let s=fs.readFileSync("drills-data.js","utf8").replace(/const\s+(DATA|EXTRA)\s*=/g,"globalThis.$1=");eval(s);
eval(fs.readFileSync("scenes-data.js","utf8").replace("const SCENES","globalThis.SCENES"));
const out=[];
DATA.forEach(u=>{const L=u.dialogue,sit=u.en+": "+u.convos[0].sub;for(let i=0;i+1<L.length;i+=2)out.push([sit,L[i][1],L[i][2],L[i+1][1]]);});
SCENES.forEach(x=>{const L=x.lines,sit=x.en+" ("+x.d+")";for(let i=0;i+1<L.length;i+=2)out.push([sit,L[i][1],L[i][2],L[i+1][1]]);});
console.log(JSON.stringify(out));'''], cwd="../.."))
# situations for the labelled cases, by their previous line
SIT = {r[1]: r[0] for r in rows}

def one(state): return ask(state, Q)["answers"]
with ThreadPoolExecutor(8) as ex:
    lab = list(ex.map(lambda c: one({"situation": SIT.get(c[0], "a friendly conversation"), "previous_line": c[0],
        "previous_line_english": c[1], "suggested_reply": c[2], "learner_reply": c[3]}), REPLY))
    sug = list(ex.map(lambda r: one({"situation": r[0], "previous_line": r[1], "previous_line_english": r[2],
        "suggested_reply": r[3], "learner_reply": r[3]}), rows))
f = [a["fits"]["noul"] for a in lab]
report("labelled: fits >= 0.5", [c[4] for c in REPLY], [x >= .5 for x in f])
for c, x in zip(REPLY, f):
    if (x >= .5) != c[4]: print(f"   MISS fits {c[4]!s:<5} {x:.2f} | {c[0][:30]} → {c[3]}")
s = [a["fits"]["noul"] for a in sug]
print(f"suggested replies judged a fit (>= 0.5): {sum(x >= .5 for x in s)}/{len(s)}; lowest {min(s):.2f}")
for r, x in zip(rows, s):
    if x < .5: print(f"   {x:.2f} {r[0][:24]} | {r[1]} → {r[3]}")
