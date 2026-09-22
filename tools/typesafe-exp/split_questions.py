"""Follow-up: do separate grammar and meaning questions beat one combined one?
Runs twice to measure run-to-run drift. (Result: no - one question is enough.)"""
import json, os
from concurrent.futures import ThreadPoolExecutor
from run import ask, produce_questions, report
from cases import PRODUCE

Q = produce_questions()
Q.pop("a_ok"); Q.pop("err")
Q["grammatical"] = {"type": "noul", "instructions": {
    "task": "Ignoring missing vowel marks, is every word in `learner_answer` correctly spelled standard Arabic, "
            "and is the sentence grammatical?",
    "check": ["adjectives and predicates agree in gender with their noun (e.g. a feminine noun needs a feminine adjective)",
              "after كم the counted noun is singular",
              "each word is a real, correctly spelled Arabic word (e.g. مصر not مسر)"]},
    "criteria": {"true": "Grammatical and correctly spelled", "false": "Has a spelling or grammar error"}}
Q["same_meaning"] = {"type": "noul",
    "instructions": "Setting aside grammar and spelling, does `learner_answer` say the same thing as `english_prompt` "
                    "(same people, facts, numbers, tense and order of events)?"}

def one(c):
    return ask({"english_prompt": c[1], "model_answer": c[0], "learner_answer": c[2]}, Q)

runs = []
for r in range(2):
    with ThreadPoolExecutor(8) as ex: runs.append(list(ex.map(one, PRODUCE)))
json.dump(runs, open(os.path.join(os.path.dirname(__file__), "results2.json"), "w"), ensure_ascii=False, indent=1)
gold = [c[3] for c in PRODUCE]
for i, res in enumerate(runs):
    g = lambda q: [x["answers"][q]["noul"] for x in res]
    print(f"run {i+1}")
    report("b_ok >= .5", gold, [x >= .5 for x in g("b_ok")])
    report("grammatical >= .5 AND same_meaning >= .5", gold,
           [a >= .5 and b >= .5 for a, b in zip(g("grammatical"), g("same_meaning"))])
    report("b_ok AND grammatical AND same_meaning", gold,
           [a >= .5 and b >= .5 and m >= .5 for a, b, m in zip(g("b_ok"), g("grammatical"), g("same_meaning"))])
drift = max(abs(a["answers"][q]["noul"] - b["answers"][q]["noul"])
            for a, b in zip(*runs) for q in ("b_ok", "grammatical", "same_meaning"))
print(f"max run-to-run difference in any probability: {drift:.3f}")
print("\nper case (run 1): gold | b_ok gram same | answer")
for c, x in zip(PRODUCE, runs[0]):
    a = x["answers"]; print(f"  {c[3]!s:<5} | {a['b_ok']['noul']:.2f} {a['grammatical']['noul']:.2f} {a['same_meaning']['noul']:.2f} | {c[2]}")
