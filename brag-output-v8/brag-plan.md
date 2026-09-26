# Brag Plan v8: Rafiq (رَفِيق) — why it exists

## What is this app?
Rafiq teaches Modern Standard Arabic in short, fully vowelled daily steps, brings every word back for review on widening gaps (1, 2, 4, 8, 16 days), and can start a complete beginner from the 28 letters.

## The angle
The name is the story. رَفِيق means *companion*: something that sits beside you while you study Arabic, in a class, at a madrasa or on your own. Lessons give you words; keeping them is the hard part, so Rafiq is built on three findings from memory research that the app already cites in its own streak goals (spacing, testing, habit). Then the second door: if you can't read Arabic yet, Rafiq starts you from the first letter.

No invented history: no founding dates, people or user numbers. Every research claim is the app's own (path.js `STREAK_GOALS`, with sources).

## Hook (first 2-3 seconds)
A red ink stroke drawn right to left (the v5/v6 opener), then رَفِيق written right to left in large type, and Rafiq's own native Arabic voice: "رَفِيق. In Arabic, it means companion."

## Key moments (the middle)
- Three contexts (in a class · at a madrasa · on your own); vowelled word cards that blur away: "Keeping them is the hard part."
- The research, one card each, with its source on screen:
  - Spacing: cramming (every review on day 1) vs spacing (days 1, 2, 4, 8, 16, each ✓). Cepeda et al., 2006, a review of 317 experiments.
  - Testing: reading بَيْت again vs recalling it (the answer is hidden, then revealed ✓). Roediger & Karpicke, 2006.
  - Habit: Home's daily goal filling (2 of 2 steps) and the 🔥 streak ticking from 11 to 12. Lally et al., 2010 on screen: about two months.
- Rafiq doing it: a review card, "What does this mean? بَيْت", the right answer picked; the next reviews in 2, 4, 8 and 16 days.
- Two doors: "Revise alongside your course" / "Start from nothing".
- The reading starter from the app: the whole alphabet (right to left) turning green family by family; the ب card with three words, ب in red in each; the native voice says بَيْت; the fatha in red; the listening test (س ص ث) answered.

## Outro / punchline
"From your first letter to your first conversation." → "A few minutes a day, with a companion beside you." → the tile, Rafiq, rafiq-arabic.com, and Rafiq: "Start your first lesson free at rafiq-arabic.com."

## User flow worth showing
Reading starter: alphabet chart → letter card with examples → listening test. Review: a due word recalled and rescheduled.

## Tone
- Preset: polished
- Creative direction: the same quiet manuscript film as the website's v6 video, told as the story behind the name
- Interpretation: calm pacing, one idea per scene, generous holds for reading, soft crossfades, sources shown quietly

## Format: landscape — 1920x1080
## Duration: about 88s (voice-led; the brief asks for the same format as the site's 62s v6 video rather than a 15-25s brag)

## Revision (TypeSafe review, tools/typesafe-exp/videos_v7_v8.py)
- Reviews are on fixed, widening gaps (1, 2, 4, 8, 16 days): r08b and the review heading say so; no "just before you'd forget it".
- No permanent free tier: the close is "Start your first lesson free at rafiq-arabic.com." (r16, Rafiq's voice, shared with v7).
- n04b: "So we built رَفِيق around three findings from memory research."
- Habit is now n07b + r07 over Home's real streak and daily goal (dashboard.html); the Lally et al. (2010) line stays on screen as "about two months".
- Cepeda et al. (2006) reviewed 317 experiments (from 184 articles): the source line says so.
- Transitions: a 0.4s handoff (the old scene is gone 0.1s after the new one starts), so no scene is drawn over another.

## Visual identity (from the project)
- Background: #f1ece0 (paper), cards #f7f3ea
- Accent: #b4322a (rubric red), #2e7263 (verdigris), #a8842c (gold)
- Text: #17262b (ink), #4f6163 (ink soft)
- Display font: Karla 700 · Arabic: IBM Plex Sans Arabic · Labels: JetBrains Mono
- Strongest visual element: fully vowelled Arabic on cards, the red letter in the reading starter, the ر tile logo

## Share copy (draft)
رَفِيق means companion. A few minutes of Arabic a day, built on what memory research says works, from your first letter to your first conversation.

## Audio direction
- Role: warm bed of natural sound under two voices (no music), as in v6
- Music: none (v4-v6 decision: natural sounds tested better than music for this audience)
- Voices: narrator (ElevenLabs "Sarah"; v6's local Kokoro voice can't be downloaded here) and Rafiq, the app's native Arabic voice, only on the lines where he says his name
- Native clips from the app: بَيْت (letter card), سَمَك (listening test)
- SFX posture: sparse, physical: reed pen for writing, page turn between scenes, a soft bong on ✓, a tap on the answer
- Audio-reactive: subtle, the warm background glow breathes with the voices
- Restraint rule: nothing competes with the voices; background about 18 dB under them

## Voiceover script (brag-output-v8/vo-script.txt; recordings from tools/v8-lines.json)
| id | voice | line |
|---|---|---|
| r01 | Rafiq | رَفِيق. In Arabic, it means companion. |
| n02 | narrator | That's what this app was made to be: a companion for anyone studying Arabic. |
| n03 | narrator | In a class, at a madrasa, or on your own, lessons give you new words. Keeping them is the hard part. |
| n04b | narrator | So we built رَفِيق around three findings from memory research. |
| n05 | narrator | Spacing. Coming back to a word after a gap beats cramming. It's one of the most replicated findings in memory research. |
| n06 | narrator | Testing. Pulling a word from memory strengthens it more than reading it again. |
| n07b | narrator | Habit. A few minutes every day beats an hour once a week. |
| r07 | Rafiq | رَفِيق gives you a small daily goal, and a streak to keep. |
| r08b | Rafiq | So رَفِيق brings each word back after a day, then two, four, eight, and asks you to recall it, not just reread it. |
| n09 | narrator | Use it to revise alongside your course. Or start from nothing at all. |
| n10 | narrator | Can't read Arabic yet? Begin with the twenty-eight letters, in families that share a shape. |
| n11 | narrator | Every letter comes with three words, the letter in red, and a native voice to copy. |
| ar_bayt | app voice | بَيْت — house |
| n12 | narrator | Then the vowel marks, and a listening test to train your ear. |
| ar_samak | app voice | سَمَك — fish |
| n13 | narrator | From your first letter to your first conversation. |
| n14 | narrator | A few minutes a day, with a companion beside you. |
| r16 | Rafiq | Start your first lesson free at rafiq-arabic.com. |

## Storyboard
Timings follow the voice (build.py computes them from the recorded line lengths).
1. **Companion** (r01, n02): ink stroke; رَفِيق written right to left; "rafīq · companion"; then the ر tile + Rafiq + "a companion for anyone studying Arabic". Pen sound under the writing.
2. **The hard part** (n03): three context chips arrive one by one (held); three word cards كِتاب مَدِينَة صَدِيق rise, then blur away under "Keeping them is the hard part."
3. **The research** (n04): three numbered cards (Spacing, Testing, Habit) arrive one by one.
4. **Spacing** (n05): cramming row (five dots on day 1, then faded) vs spaced row (days 1, 2, 4, 8, 16 ✓ one by one, pen ticks); source line.
5. **Testing** (n06): "Reading it again" card (dim) vs "Recalling it" (hidden answer → "house ✓", bong); source line.
6. **Habit** (n07b, r07): Home's streak and daily-goal cards; the goal fills, the streak goes 11 → 12; "A few minutes every day / beats an hour once a week"; source line.
7. **Rafiq does it** (r08): review quiz بَيْت → "house" tapped ✓; next reviews in 2 · 4 · 8 · 16 days.
8. **Two doors** (n09): "Revise alongside your course" and "Start from nothing" cards.
9. **The alphabet** (n10): the app's 28-letter chart, right to left, turning green one shape family at a time (pen writing).
10. **A letter** (n11 + بَيْت): the ب card with بَيْت / طالِبَة / كِتاب, ب in red; the بَيْت row lights while the native voice says it.
11. **Vowels and the ear** (n12 + سَمَك): بَ with the fatha in red; the listening test plays سَمَك, س is tapped ✓ and the word is revealed.
12. **First conversation** (n13): ا → بَيْت → a reply bubble with "✓ Good reply."
13. **Close** (n14, r16): "A few minutes a day," / "with a companion beside you."; tile, Rafiq, rafiq-arabic.com, "Start your first lesson free".

**Audio summary:** a pen stroke opens; fountain and birdsong settle in under the voices from the first scene; quiet physical sounds mark writing, answers and page turns; a soft swell carries the close.
