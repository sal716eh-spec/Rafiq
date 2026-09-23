# Brag Plan v2: Rafiq (رَفِيق) — the story

## What is this app?
Rafiq teaches Modern Standard Arabic in short, fully vowelled daily steps on one path, brings back every word you've learned on a spaced-repetition schedule so it sticks, lets you reply to real conversations in your own words with instant feedback, and notices the mistakes you repeat.

## The angle
v1 showed the product; v2 tells the story. It starts with the learner's problem (you've tried before, and the words slipped away), asks the question many Muslim learners feel ("You can recite it. But do you understand it?"), then introduces Rafiq and walks through how it solves that problem — ending on the promise TypeSafe rated most credible: "A few minutes a day. Words that come back until they stay."

## How TypeSafe shaped it
Candidate hooks, feature lines and closers were scored by TypeSafe (System One, jev-latest) for four viewers — a Muslim learner who wants to understand the Quran and prayers, a heritage speaker, a busy professional who forgot what an app taught them, a complete beginner — plus two checks against a list of true facts about the app: "is every claim supported?" and "is it concrete?". Scripts: `typesafe/`.
- Hook chosen: "You've tried to learn Arabic before…" (highest appeal across all four viewers, 2.52/3). "Fluent Arabic in 30 days" (supported 0.05) and an invented "most people give up" statistic (0.14) were rejected.
- Spaced repetition line chosen: "Rafiq remembers what you've learned, and brings each word back just before you'd forget it." (2.32/3; 2.9 for the viewer who forgot; supported 0.83).
- Feature beats kept (top-rated): reading starter, fully vowelled words with a native voice, one path, conversation feedback, weak spots. Dropped for time: real-life scenes, placement, unit list, streak goals.
- Line rewritten: "The script. The vowels. The words that never stick." was judged cheesy (0.53) → "A new script, tiny vowel marks, and words that slip away a week later."
- Closer: "A few minutes a day. Words that come back until they stay." (supported 0.78, warm 0.93) beat "Arabic that stays" (0.54) and "Become fluent with Rafiq" (0.20).

## Voiceover (vo-script.txt)
1. You've tried to learn Arabic before.
2. A new script, tiny vowel marks, and words that slip away a week later.
3. You can recite it. But do you understand it?
4. Meet Rafiq, your companion in learning Arabic.
5. Can't read the script yet? Start with the letters.
6. Then one path, one Continue button, five to ten minutes a day.
7. Every word fully vowelled, and spoken by a native Arabic voice. → then the app's own native-voice clip: بَيْت
8. Rafiq remembers what you've learned, and brings each word back just before you'd forget it.
— the app's native-voice neighbour line: السَّلامُ عَلَيْكُمْ. أَنا جارُكَ الْجَدِيدُ.
9. Then use it. Reply in your own words, and find out instantly if it makes sense.
10. It notices the mistakes you keep making, and helps you fix them.
11. A few minutes a day. Words that come back until they stay.
12. Try Rafiq free at rafiq-arabic.com.

Draft voice: Kokoro af_heart (local, free). To swap for ElevenLabs, render the same 12 lines to `composition/assets/vo/vo-NN.wav` (or .mp3) and re-run render; scene timing follows the line lengths in index.html.

## Tone
- Preset: polished, with a story arc (problem → question → answer → how → promise)
- Format: landscape 1920x1080 · Duration: 61.9s

## Storyboard (seconds)
| # | Scene | Window | VO |
|---|---|---|---|
| A | The problem: three vowelled word cards blur away — "one week later" | 0–7.8 | 1, 2 |
| B | سُبْحانَ رَبِّيَ الْعَظِيمِ with an empty "meaning?" line | 7.4–11.0 | 3 |
| C | Meet Rafiq: logo tile, Rafiq, رَفِيق | 10.6–14.8 | 4 |
| D1 | Reading starter: ا ب ت ث with names | 14.4–17.9 | 5 |
| D2 | Home: Today card, Continue pressed, the path | 17.5–22.1 | 6 |
| E | Word card 🏠 بَيْت · bayt · house, native voice plays | 21.7–28.5 | 7 + clip |
| F | Spaced review: بَيْت returns on day 2, 4, 8, 16; memory curve; "12 to review" | 28.1–35.8 | 8 |
| G | Conversation: neighbour line (native audio), typed reply, ✓ Good reply. | 35.4–45.2 | clip + 9 |
| H | Weak spots: "Masculine and feminine must match" card | 44.8–50.6 | 10 |
| I | "A few minutes a day." / "Words that come back until they stay." → logo, rafiq-arabic.com, Try it free | 50.2–59.5 | 11, 12 |

Review days follow the app's real word schedule (gaps of 1, 2, 4, 8 days). No personal data: learner and neighbour are fictional; lines are the app's own content.

## Audio (no music)
No music, by choice for an Islamic learning platform. Instead:
- Cold open (0–3s): the app's native Arabic voice says كِتاب, مَدِينَة, صَدِيق as each card appears; the narrator starts after.
- Soft room tone throughout (filtered brown noise, about -40 dB): non-musical, just enough that pauses aren't dead silence.
- Quiet paper sounds as cards slide in; soft clicks on Continue and Send; a soft chime on ✓ and a soft thud under the logo.
- The background glow breathes with the voices (RMS of the narration and Arabic clips) instead of music.
Everything after the cold open is 2.4s later than the storyboard table above; total 61.9s.
