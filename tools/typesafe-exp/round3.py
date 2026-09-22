"""Round 3: the conversation partner. Does the learner's reply make sense after
what was just said (it need not match the book's reply), and is it grammatical?

    TYPESAFE_API_KEY=... python3 tools/typesafe-exp/round3.py

REPLY_Q is what worker/src/index.js sends for kind 'reply'."""
from concurrent.futures import ThreadPoolExecutor
from run import ask, report, best_threshold
from cases3 import REPLY

REPLY_Q = {
    "fits": {"type": "noul", "instructions": {
        "task": "In a beginner's Arabic conversation, the other person said `previous_line`. The learner replied "
                "`learner_reply`. Is it a sensible, relevant reply to what was just said?",
        "notes": ["It does not have to match `suggested_reply` — any natural answer counts, with the learner's own details",
                  "Ignore grammar and spelling here; judge only whether it answers or responds to `previous_line`"]},
        "criteria": {"true": "A sensible reply", "false": "Doesn't respond to what was said"}},
    "grammar": {"type": "noul", "instructions": {
        "task": "Ignoring missing vowel marks, is `learner_reply` grammatical, correctly spelled Arabic?",
        "check": ["gender agreement, and addressing a man as أنتَ", "the right person and tense on verbs",
                  "numbers with the right gender (ثلاثة إخوة, not ثلاث إخوة)"]},
        "criteria": {"true": "No errors", "false": "At least one error"}},
    "err": {"type": "choice", "instructions": "What is the main grammar or spelling problem in `learner_reply`?",
            "criteria": {"none": "No grammar or spelling problem (missing vowel marks are fine)",
                         "gender_agreement": "A word has the wrong gender (masculine/feminine) for what it refers to",
                         "wrong_person_or_tense": "A verb or pronoun is in the wrong person, number or tense",
                         "spelling": "A word is misspelled so it is a different or non-existent word",
                         "grammar_other": "Some other grammatical error"}},
}

def main():
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda c: ask({"previous_line": c[0], "previous_line_english": c[1], "suggested_reply": c[2],
                                          "learner_reply": c[3]}, REPLY_Q), REPLY))
    f = [x["answers"]["fits"]["noul"] for x in res]; g = [x["answers"]["grammar"]["noul"] for x in res]
    print(f"REPLY ({len(REPLY)})")
    report("fits >= 0.5", [c[4] for c in REPLY], [x >= .5 for x in f])
    print("  best fits threshold %.2f -> %.0f%%" % (best_threshold(f, [c[4] for c in REPLY])[1], 100*best_threshold(f, [c[4] for c in REPLY])[0]))
    for th in (.5, .7):
        report(f"grammar >= {th}", [c[5] for c in REPLY], [x >= th for x in g])
    for c, a, b, x in zip(REPLY, f, g, res):
        if (a >= .5) != c[4] or (b >= .7) != c[5]:
            print(f"   fits {c[4]!s:<5} {a:.2f} | gram {c[5]!s:<5} {b:.2f} {x['answers']['err']['choice']:<22} | {c[3]}")
    ms = sorted(x["_ms"] for x in res); print(f"latency p50 {ms[len(ms)//2]} ms")

if __name__ == "__main__":
    main()
