"""Compare Rafiq's current answer checkers with TypeSafe judgments.

    TYPESAFE_API_KEY=... python3 tools/typesafe-exp/run.py

Without a key it reports the current checkers only. The question wording
here is what worker/src/index.js sends; change both together.
"""
import json, os, re, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from cases import VOCAB, PRODUCE

KEY = os.environ.get("TYPESAFE_API_KEY") or os.environ.get("TYPE_SAFE_KEY")
URL = "https://api.typesafe.ai/v1/systemone"
OUT = os.path.join(os.path.dirname(__file__), "results.json")

# ---------- current app logic, ported 1:1 ----------
def norm_en(s):
    s = (s or "").lower().strip()
    s = re.sub(r"^(a|an|the)\s+", "", s)
    s = re.sub(r"[.,!?;:()\"']", "", s)
    return re.sub(r"\s+", " ", s).strip()

def vocab_baseline(gloss, typed):
    t = norm_en(typed)
    return bool(t) and t in [norm_en(g) for g in gloss.split("/") if norm_en(g)]

def norm_ar(s):
    s = re.sub("[ً-ْٰـٓ-ٖ]", "", s or "")
    for a, b in (("[أإآٱ]", "ا"), ("ى", "ي"), ("ؤ", "و"), ("ئ", "ي"), ("ة", "ه")):
        s = re.sub(a, b, s)
    s = re.sub("[^ء-ي\\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def lcs_score(target, said):
    t = [w for w in (norm_ar(x) for x in target.split()) if w]
    s = norm_ar(said).split()
    dp = [[0] * (len(s) + 1) for _ in range(len(t) + 1)]
    for i in range(1, len(t) + 1):
        for j in range(1, len(s) + 1):
            dp[i][j] = dp[i-1][j-1] + 1 if t[i-1] == s[j-1] else max(dp[i-1][j], dp[i][j-1])
    return round(100 * dp[-1][-1] / len(t)) if t else 0

# ---------- TypeSafe ----------
def ask(state, questions):
    body = json.dumps({"state": state, "model": "jev-latest", "questions": questions}).encode()
    req = urllib.request.Request(URL, body, {"Authorization": f"Bearer {KEY}",
                                             "Content-Type": "application/json"})
    for attempt in range(4):
        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                res = json.load(r)
            res["_ms"] = round(1000 * (time.time() - t0))
            return res
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < 3:
                time.sleep(2 ** attempt); continue
            raise RuntimeError(f"HTTP {e.code}: {e.read()[:300]!r}")

def vocab_questions():
    return {
        # A: bare question
        "a_ok": {"type": "noul",
                 "instructions": "Is `answer` an acceptable English translation of `arabic`?"},
        # B: spells out what a teacher would accept and reject
        "b_ok": {"type": "noul",
                 "instructions": {
                     "task": "A beginner learning Arabic was shown `arabic` and typed its English meaning as `answer`. "
                             "The textbook glosses are in `glosses`. Should a fair teacher mark it correct?",
                     "accept": ["a synonym or near-synonym with the same meaning",
                                "the same word without 'to', 'a' or 'the', or in another form (plural, past tense)",
                                "a small spelling slip where the intended English word is obvious",
                                "leaving out a gender note such as (m) or (f)"],
                     "reject": ["a different word, even a related one (bedroom for room)",
                                "an opposite or a word from the same topic with another meaning"]},
                 "criteria": {"true": "Mark correct", "false": "Mark wrong"}},
    }

ERRS = {
    "none": "Correct: same meaning as the model answer and grammatical. Missing vowel marks, "
            "hamza spelling, ة/ه and attached و are fine; so are synonyms and word orders Arabic allows.",
    "gender_agreement": "A word has the wrong gender (masculine/feminine) for what it refers to",
    "wrong_person_or_tense": "A verb or pronoun is in the wrong person, number or tense",
    "wrong_word": "One word or detail is replaced by a different one, changing a fact",
    "different_meaning": "The words are rearranged or changed so the sentence says something else",
    "missing_word": "Needed words are left out, so the sentence is incomplete",
    "spelling": "A word is misspelled so it is a different or non-existent word",
    "grammar_other": "Some other grammatical error",
}

def produce_questions():
    return {
        "a_ok": {"type": "noul",
                 "instructions": "Does `learner_answer` correctly express `english_prompt` in Arabic, "
                                 "like `model_answer` does?"},
        "b_ok": {"type": "noul",
                 "instructions": {
                     "task": "A beginner was asked to say `english_prompt` in Modern Standard Arabic and wrote "
                             "`learner_answer`. `model_answer` is one correct answer. Is the learner's answer correct?",
                     "ignore": ["missing vowel marks (harakat) and case endings that are not written",
                                "hamza forms, ة written as ه, ى as ي, spacing, punctuation",
                                "synonyms and any word order Arabic allows"],
                     "not_ignore": ["wrong gender, person, number or tense",
                                    "a changed fact, word or meaning", "missing words", "misspelled words"]},
                 "criteria": {"true": "Correct answer", "false": "Contains an error"}},
        "err": {"type": "choice",
                "instructions": "What is the main problem with `learner_answer` as an Arabic rendering of "
                                "`english_prompt`, compared with `model_answer`?",
                "criteria": ERRS},
    }

# ---------- evaluation ----------
def best_threshold(scores, gold):
    best = (0, 0.5)
    for th in [i / 20 for i in range(1, 20)]:
        acc = sum((s >= th) == g for s, g in zip(scores, gold)) / len(gold)
        best = max(best, (acc, th))
    return best

def report(name, gold, preds):
    acc = sum(p == g for p, g in zip(preds, gold)) / len(gold)
    fa = sum(p and not g for p, g in zip(preds, gold))   # wrong answer accepted
    fr = sum(g and not p for p, g in zip(preds, gold))   # right answer rejected
    print(f"  {name:<34} acc {acc:5.0%}   wrongly accepted {fa:2}   wrongly rejected {fr:2}")
    return acc

def main():
    vg = [c[3] for c in VOCAB]; pg = [c[3] for c in PRODUCE]
    print(f"VOCAB ({len(VOCAB)} cases)")
    report("current exact match", vg, [vocab_baseline(c[1], c[2]) for c in VOCAB])
    lcs = [lcs_score(c[0], c[2]) for c in PRODUCE]
    print(f"PRODUCE ({len(PRODUCE)} cases)")
    for th in (60, 80, 100):
        report(f"current word match >= {th}%", pg, [s >= th for s in lcs])
    if not KEY:
        print("\nTYPESAFE_API_KEY not set - baseline only."); return

    vq, pq = vocab_questions(), produce_questions()
    with ThreadPoolExecutor(8) as ex:
        vres = list(ex.map(lambda c: ask({"arabic": c[0], "glosses": c[1].split("/"), "answer": c[2]}, vq), VOCAB))
        pres = list(ex.map(lambda c: ask({"english_prompt": c[1], "model_answer": c[0],
                                          "learner_answer": c[2]}, pq), PRODUCE))
    json.dump({"vocab": vres, "produce": pres}, open(OUT, "w"), ensure_ascii=False, indent=1)

    for label, cases, res, gold, qs in (("VOCAB", VOCAB, vres, vg, ("a_ok", "b_ok")),
                                        ("PRODUCE", PRODUCE, pres, pg, ("a_ok", "b_ok"))):
        print(f"\n{label} - TypeSafe")
        for q in qs:
            p = [r["answers"][q]["noul"] for r in res]
            report(f"{q} noul >= 0.5", gold, [x >= .5 for x in p])
            acc, th = best_threshold(p, gold)
            print(f"  {'':<34} (best threshold {th:.2f} -> {acc:.0%}; in-sample, optimistic)")
        if label == "VOCAB":
            combo = [vocab_baseline(c[1], c[2]) or r["answers"]["b_ok"]["noul"] >= .5 for c, r in zip(cases, res)]
            report("exact match, else b_ok", gold, combo)
        ms = sorted(r["_ms"] for r in res); tok = [r["usage"]["input_tokens"] for r in res]
        print(f"  latency p50 {ms[len(ms)//2]} ms, p90 {ms[int(len(ms)*.9)]} ms; ~{sum(tok)//len(tok)} input tokens/call")

    errs = [(c[4], r["answers"]["err"]["choice"]) for c, r in zip(PRODUCE, pres)]
    print(f"\nPRODUCE error type: {sum(a == b for a, b in errs)}/{len(errs)} exact;"
          f" ok-vs-error agreement {sum((a == 'none') == (b == 'none') for a, b in errs)}/{len(errs)}")

    print("\nMisses (b_ok):")
    for c, r in zip(VOCAB, vres):
        n = r["answers"]["b_ok"]["noul"]
        if (n >= .5) != c[3]: print(f"  vocab  {c[1]!r:<12} typed {c[2]!r:<14} gold {c[3]!s:<5} noul {n:.2f}")
    for c, r in zip(PRODUCE, pres):
        n = r["answers"]["b_ok"]["noul"]; e = r["answers"]["err"]["choice"]
        if (n >= .5) != c[3] or e != c[4]:
            print(f"  produce {c[2]:<40} gold {c[3]!s:<5}/{c[4]:<22} noul {n:.2f} err {e}")

if __name__ == "__main__":
    main()
