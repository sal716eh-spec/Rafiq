"""QA for tools/new-dialogues.json: every line is checked for grammar, vowelling
and whether the English matches. Lines flagged here need a human look."""
import json, os
from concurrent.futures import ThreadPoolExecutor
from run import ask

Q = {
  "grammar": {"type": "noul", "instructions": {
      "task": "Is `arabic` a grammatical, natural Modern Standard Arabic sentence for a beginners' textbook dialogue?",
      "check": ["agreement in gender and number", "correct case endings in the vowel marks",
                "correct numbers and counted nouns", "natural word choice"]},
    "criteria": {"true": "Correct and natural", "false": "Has an error or sounds unnatural"}},
  "vowels": {"type": "noul", "instructions": "Are the vowel marks (harakat) on `arabic` correct throughout?"},
  "english": {"type": "noul", "instructions": "Is `english` an accurate translation of `arabic`?"},
}
D = json.load(open(os.path.join(os.path.dirname(__file__), "..", "new-dialogues.json")))
rows = [(u, i, l) for u, d in D.items() for i, l in enumerate(d["lines"])]
with ThreadPoolExecutor(8) as ex:
    res = list(ex.map(lambda r: ask({"arabic": r[2][1], "english": r[2][2], "context": D[r[0]]["sub"]}, Q), rows))
flag = 0
for (u, i, l), x in zip(rows, res):
    a = {k: v["noul"] for k, v in x["answers"].items()}
    if min(a.values()) < 0.6:
        flag += 1
        print(f"{u}:{i+1:<2} gram {a['grammar']:.2f} vowels {a['vowels']:.2f} eng {a['english']:.2f} | {l[1]} | {l[2]}")
print(f"\n{flag} of {len(rows)} lines flagged")
