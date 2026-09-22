"""Round 2b: focused extra questions for Build-it order and Transform / Fix-it,
after round2.py let a scrambled order and two half-right rewrites through.
Each run is repeated twice to see how stable the probabilities are."""
from concurrent.futures import ThreadPoolExecutor
from run import ask, produce_questions, report
from cases2 import BUILD, REWRITE
from round2 import REWRITE_Q

ORDER_Q = {"order": {"type": "noul", "instructions": {
    "task": "`learner_answer` is the pieces of `model_answer` put in a different order. Is the new order "
            "natural, grammatical Arabic that means the same as `english_prompt`?",
    "rules": ["an adjective must come straight after its noun (الدور الخامس, not الخامس في الدور)",
              "the order of events must not change", "a demonstrative must agree with the noun after it"]},
    "criteria": {"true": "Acceptable order", "false": "Unnatural, ungrammatical, or changes the meaning"}}}

CHANGES_Q = {"changes": {"type": "noul", "instructions": {
    "task": "Compare `original`, `model_answer` and `learner_answer`, ignoring vowel marks. Does `learner_answer` "
            "make every change that `model_answer` makes, or an equally correct alternative, with no new mistakes?",
    "check": ["every verb that should change has changed (e.g. both verbs to the past)",
              "after كم the noun is singular (كم حصة, never كم حصص)",
              "the person is right: asking someone a question uses 'you' (تـ), not 'I' (أ)"]},
    "criteria": {"true": "All required changes made correctly", "false": "A required change is missing or wrong"}}}

def run(cases, state, qs):
    with ThreadPoolExecutor(8) as ex: return list(ex.map(lambda c: ask(state(c), qs), cases))

bq = produce_questions(); bq.pop("a_ok"); bq.pop("err"); bq |= ORDER_Q
rq = {"ok": REWRITE_Q["ok"]} | CHANGES_Q
for rep in (1, 2):
    b = run(BUILD, lambda c: {"english_prompt": c[0], "model_answer": c[1], "learner_answer": c[2].lstrip("، ")}, bq)
    r = run(REWRITE, lambda c: {"task": c[0], "original": c[1], "model_answer": c[2], "learner_answer": c[3]}, rq)
    print(f"--- run {rep}")
    g = lambda res, q: [x["answers"][q]["noul"] for x in res]
    bg = [c[3] for c in BUILD]; rg = [c[4] for c in REWRITE]
    report("build: b_ok>=.8", bg, [n >= .8 for n in g(b, "b_ok")])
    report("build: order>=.5", bg, [n >= .5 for n in g(b, "order")])
    report("build: b_ok>=.8 AND order>=.5", bg, [a >= .8 and o >= .5 for a, o in zip(g(b, "b_ok"), g(b, "order"))])
    report("rewrite: ok>=.5", rg, [n >= .5 for n in g(r, "ok")])
    report("rewrite: changes>=.5", rg, [n >= .5 for n in g(r, "changes")])
    report("rewrite: ok>=.5 AND changes>=.5", rg, [a >= .5 and c >= .5 for a, c in zip(g(r, "ok"), g(r, "changes"))])
    if rep == 1:
        for c, x in zip(BUILD, b):
            a = x["answers"]; print(f"   {c[3]!s:<5} b_ok {a['b_ok']['noul']:.2f} order {a['order']['noul']:.2f}  {c[2]}")
        for c, x in zip(REWRITE, r):
            a = x["answers"]
            print(f"    {c[4]!s:<5} ok {a['ok']['noul']:.2f} changes {a['changes']['noul']:.2f}  {c[0][:20]:<20} {c[3]}")
