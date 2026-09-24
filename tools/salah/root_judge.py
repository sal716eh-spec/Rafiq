"""Asks TypeSafe whether a course word really comes from a root used in salah.
Letter matching alone links شَرْق (east) to شَرّ (evil); this filters that out.
Measured on 69 hand-labelled candidate pairs (29 real, 40 coincidental):
  asking "is the entry derived from root R?"           -> 56/69 at 0.5 (10 false links)
  asking "same root as this salah word?" (below)        -> 64/69 at 0.5 (2 false links, 3 missed)
                                                          63/69 at 0.6 (1 false link, 5 missed)
Every accepted link is still checked by hand and then by the teacher."""
THRESHOLD = 0.5
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
Q = {"same": {"type": "noul", "instructions": "Arabic roots. Salah word: `sw` (meaning `swm`), root `root`. Course entry: `entry` (meaning `meaning`). "
 "Does the course entry contain a word that an Arabic dictionary lists under the same root `root` as the salah word? "
 "Think about the actual root of each word in the entry. Shared letters are not enough: e.g. شَرْق (east, root ش-ر-ق) is NOT from شَرّ (evil, root ش-ر-ر); "
 "مَسْجِد (root س-ج-د) is NOT from مَجِيد (root م-ج-د). Particles such as عَلى and نَعَمْ have no root."}}
def judge(entry, meaning, root, salah_word, salah_meaning):
    return ask({"sw": salah_word, "swm": salah_meaning, "root": "-".join(root), "entry": entry, "meaning": meaning}, Q)["answers"]["same"]["noul"]
