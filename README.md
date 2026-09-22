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
| `drills.html` | Twelve drill modes across units 1–12 |
| `site.css` | Shared palette, nav and buttons |
| `judge.js` | Asks the answer-checking Worker whether a typed answer is right (see below) |

## Drills

Dialogue · Role-play · Dictation · Ladder · Substitution · Build-it · Transform · Gap-fill · Fix-it · Structures · Produce · Review.

672 tracked items with spaced repetition, answer checking that ignores vowel marks, and speech input where the browser supports it. Vocabulary comes from the word lists printed at the back of the books themselves, so every word drilled is one the book teaches.

## Answer checking

Typed answers are checked in two layers:

- **Exact match first**, in the browser — vowel marks ignored for Arabic, a leading "a/an/the" for English.
- **If that fails, a judgment on meaning** from [TypeSafe](https://docs.typesafe.ai), through a small Cloudflare Worker in `worker/` that holds the API key. Vocab accepts synonyms, "go" for "to go", "you" for "you (m)" and small typos; Produce accepts sentences without vowel marks, with synonyms or another valid word order, and names the main mistake when there is one ("a word has the wrong gender").

Dictation and verb forms stay exact-match: there the precise words are the point. If the Worker isn't configured, is offline or takes over 3 s, every page falls back to exact matching.

On 80 hand-labelled learner answers (`tools/typesafe-exp/`), the judge was right 95% of the time on vocab (exact match: 53%) and 92–95% on Produce (word matching: 49–76%). Its misses were subtle (a gender slip, a misspelling, a wrong plural), so when it is unsure the learner gets "Nearly — compare with the model answer" rather than a verdict.

**When it's on, what the learner typed is sent to the Worker and on to TypeSafe** to be judged. Nothing else is: no account, no progress.

### Setting up the Worker

1. Cloudflare dashboard → **Workers & Pages → Create → Import a repository** → this repo. Leave the root directory as `/`; `wrangler.toml` at the top level points at `worker/src/index.js`.
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
