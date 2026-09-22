"""Round 2: Build-it reorderings, Transform / Fix-it answers, open prompts.

    TYPESAFE_API_KEY=... python3 tools/typesafe-exp/round2.py

Build-it reuses the Produce question unchanged. REWRITE_Q and PROMPT_Q are
what worker/src/index.js sends for kinds 'rewrite' and 'prompt'; change
both together.
"""
from concurrent.futures import ThreadPoolExecutor
from run import ask, produce_questions, report, ERRS
from cases2 import BUILD, REWRITE, PROMPT

REWRITE_Q = {
    "ok": {"type": "noul",
           "instructions": {
               "task": "A beginner was given `original` and asked to do `task`. They wrote `learner_answer`. "
                       "`model_answer` is one correct answer. Did they do the task correctly?",
               "ignore": ["missing vowel marks (harakat) and case endings that are not written",
                          "hamza forms, ة written as ه, ى as ي, spacing, punctuation",
                          "a different but equally correct way of doing the task"],
               "not_ignore": ["the change asked for was not made, or only partly made",
                              "other words changed that should have stayed the same",
                              "wrong gender, person, number or tense", "misspelled words"]},
           "criteria": {"true": "Task done correctly", "false": "Not done correctly"}},
    "err": {"type": "choice",
            "instructions": "What is the main problem with `learner_answer` as an answer to `task` applied to `original`?",
            "criteria": {**ERRS,
                         "none": "Correct: the task is done and the sentence is grammatical. Missing vowel marks, "
                                 "hamza spelling and ة/ه are fine, and so is another correct way of doing it.",
                         "not_done": "The change asked for in `task` was not made, or the sentence was copied unchanged"}},
}

PROMPT_Q = {
    "done": {"type": "score",
             "instructions": "A beginner was asked `task` and answered in Arabic with `learner_answer`. "
                             "`model_answer` is one example answer; theirs may say different things. "
                             "How completely does their answer do what `task` asks? Ignore grammar here.",
             "criteria": ["Does not answer the task: off-topic or nothing relevant",
                          "Partly answers: on topic, but noticeably less than the task asks for "
                          "(fewer sentences, questions or items than requested)",
                          "Fully answers the task, even if the details differ from the model answer"]},
    "grammar": {"type": "noul",
                "instructions": {
                    "task": "Ignoring missing vowel marks, is `learner_answer` grammatical, correctly spelled Arabic?",
                    "check": ["gender agreement between nouns, adjectives, pronouns and verbs",
                              "the right person on verbs", "indefinite accusative nouns written with their alif (دجاجا)"]},
                "criteria": {"true": "No errors", "false": "At least one error"}},
    "err": {"type": "choice",
            "instructions": "What is the main grammar or spelling problem in `learner_answer`?",
            "criteria": {k: v for k, v in ERRS.items() if k not in ("different_meaning", "wrong_word", "missing_word")}
                        | {"none": "No grammar or spelling problem (missing vowel marks are fine)"}},
}

def main():
    pq = produce_questions(); pq.pop("a_ok")
    with ThreadPoolExecutor(8) as ex:
        b = list(ex.map(lambda c: ask({"english_prompt": c[0], "model_answer": c[1], "learner_answer": c[2]}, pq), BUILD))
        r = list(ex.map(lambda c: ask({"task": c[0], "original": c[1], "model_answer": c[2], "learner_answer": c[3]}, REWRITE_Q), REWRITE))
        p = list(ex.map(lambda c: ask({"task": c[0], "model_answer": c[1], "learner_answer": c[2]}, PROMPT_Q), PROMPT))

    print(f"BUILD reorderings ({len(BUILD)}; {sum(c[3] for c in BUILD)} valid)")
    nb = [x["answers"]["b_ok"]["noul"] for x in b]
    for th in (.5, .8):
        report(f"b_ok >= {th}", [c[3] for c in BUILD], [n >= th for n in nb])
    for c, n in zip(BUILD, nb):
        print(f"   {c[3]!s:<5} {n:.2f}  {c[2]}")

    print(f"\nREWRITE: Transform + Fix-it ({len(REWRITE)})")
    nr = [x["answers"]["ok"]["noul"] for x in r]
    for th in (.5, .8):
        report(f"ok >= {th}", [c[4] for c in REWRITE], [n >= th for n in nr])
    for c, n, x in zip(REWRITE, nr, r):
        if (n >= .5) != c[4] or .5 <= n < .8:
            print(f"   {c[4]!s:<5} {n:.2f} {x['answers']['err']['choice']:<22} {c[0][:22]:<22} {c[3]}")

    print(f"\nPROMPT ({len(PROMPT)})")
    sc = [x["answers"]["done"]["score"] for x in p]
    band = lambda s: 0 if s < .67 else 1 if s < 1.34 else 2
    print(f"  task done: {sum(band(s) == c[3] for s, c in zip(sc, PROMPT))}/{len(PROMPT)} in the right band")
    report("grammar >= 0.5", [c[4] for c in PROMPT], [x["answers"]["grammar"]["noul"] >= .5 for x in p])
    for c, s, x in zip(PROMPT, sc, p):
        a = x["answers"]
        print(f"   done {c[3]} got {s:.2f} | gram {c[4]!s:<5} got {a['grammar']['noul']:.2f} {a['err']['choice']:<22} | {c[2]}")
    ms = sorted(x["_ms"] for x in b + r + p)
    print(f"\nlatency p50 {ms[len(ms)//2]} ms, p90 {ms[int(len(ms)*.9)]} ms")

if __name__ == "__main__":
    main()
