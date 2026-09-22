# بين يديك — Arabic

A study site for **Al-ʿArabiyyah Bayna Yadayk** (العربية بين يديك), Book 1. Modern Standard Arabic.

Two halves that work on the same problem from different ends: a **vocabulary** trainer for recall, and a **speaking drills** app for production. Static files — no build step, no server, no dependencies.

## Pages

| File | |
|---|---|
| `index.html` | Sign-in screen. Placeholder — any details take you through. |
| `dashboard.html` | Entry point; shows what's due in both halves |
| `vocab.html` | Daily spaced-repetition review + searchable word list |
| `vocab-data.js` | 622 words, units 1–16, from the book's own printed lists |
| `drills.html` | Thirteen drill modes across units 1–12 |
| `site.css` | Shared palette, nav and buttons |
| `judge.js` | Asks the answer-checking Worker whether a typed answer is right (see below) |

## Drills

Dialogue · Role-play · Dictation · Ladder · Substitution · Build-it · Transform · Gap-fill · Fix-it · Structures · Produce · Free speaking · Review.

672 tracked items with spaced repetition, answer checking that ignores vowel marks, and speech input where the browser supports it. Vocabulary comes from the word lists printed at the back of the books themselves, so every word drilled is one the book teaches.

## Answer checking

Typed answers are checked in two layers:

- **Exact match first**, in the browser — vowel marks ignored for Arabic, a leading "a/an/the" for English.
- **If that fails, a judgment on meaning** from [TypeSafe](https://docs.typesafe.ai), through a small Cloudflare Worker in `worker/` that holds the API key:
  - **Vocab** accepts synonyms, "go" for "to go", "you" for "you (m)" and small typos.
  - **Produce** accepts sentences without vowel marks, with synonyms or another valid word order, and names the main mistake ("a word has the wrong gender").
  - **Build-it** accepts another valid tile order ("That order works too ✓") instead of only the book's.
  - **Transform** and **Fix-it** take a typed answer and check the change was made — all of it, and nothing else broken.
  - **Free speaking** (new) gives open tasks from the book — introduce yourself, order a meal — and checks whether you did what was asked and, separately, your grammar. Without the judge it shows an example answer.

Dictation and verb forms stay exact-match: there the precise words are the point. If the Worker isn't configured, is offline or takes over 3 s, every page falls back to exact matching.

Measured on hand-labelled learner answers in `tools/typesafe-exp/`:

| Check | Cases | Judge | Before |
|---|---|---|---|
| Vocab | 43 | 95% | 53% (exact match) |
| Produce | 37 | 92–95% | 49–76% (word matching) |
| Build-it reorders | 15 | 15/15 | only the book's order |
| Transform / Fix-it | 33 | 31/33 | reveal only |
| Free speaking: task done | 17 | 17/17 | — |
| Free speaking: grammar | 17 | 17/17 | — |

The misses are subtle (a gender slip, a wrong plural, one verb of two left in the present), so when the judge is unsure the learner gets "Nearly — compare with the model answer" rather than a verdict. The small case counts mean these numbers are a sanity check, not a guarantee.

**When it's on, what the learner typed is sent to the Worker and on to TypeSafe** to be judged. Nothing else is: no account, no progress.

### Setting up the Worker

1. Cloudflare dashboard → **Workers & Pages → Create → Import a repository** → this repo, root directory `/worker`. Every push to `main` rebuilds and redeploys it.
2. Once deployed: **Settings → Variables and Secrets → Add** → type *Secret*, name `TYPESAFE_API_KEY`.
3. Copy the Worker's URL (`https://rafiq-judge.<you>.workers.dev`) into `ENDPOINT` at the top of `judge.js`.

The Worker only answers requests from `rafiq-arabic.com` and only asks the two fixed questions, so the key can't be borrowed for anything else.

## Progress

The two halves keep separate schedules, on purpose — single words and whole sentences are not forgotten at the same rate.

| | Store | Boxes |
|---|---|---|
| Vocab | `bay_vocab_progress_v1` | 1, 2, 4, 8, 16 days · 12 new words/day by default |
| Drills | `bay_drills_progress_v1` | 1, 3, 7, 21, 60 days |

Both use `localStorage`, so progress is per-device and per-browser. The dashboard reads both and reports them side by side.

## Running it

Open `index.html`, or publish with GitHub Pages: **Settings → Pages → Deploy from a branch → `main` → `/ (root)`**.

On a phone, open the published URL and **Add to Home Screen** — it runs full-screen with the manifest and icons here.

Audio needs an Arabic voice on the device; microphone input needs Chrome or another browser with the Web Speech API.

## Known gaps

- **The sign-in is cosmetic.** No accounts, no server, nothing checked — it sets a flag and moves on. Don't put anything private behind it.
- **English glosses and transliteration in `vocab-data.js` are editorial** — the book prints Arabic only. Worth spot-checking with a teacher.
- Units 13–16 are not in the drills yet.

## Caveats

Vowel marks, model answers and grammar notes are a study aid, not an authority — worth checking with a teacher, especially case endings. Built-in speech synthesis is fine for rhythm and shadowing but is not a pronunciation model.

## Licence

Code and original drill content: MIT (see `LICENSE`).

*Al-ʿArabiyyah Bayna Yadayk* is © Arabic For All (العربية للجميع). Unofficial personal study aid, not affiliated with or endorsed by the publisher, and not a substitute for the books.
