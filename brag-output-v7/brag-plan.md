# Brag Plan v7: Rafiq (رَفِيق) — everything inside

## What is this app?
Rafiq teaches Modern Standard Arabic in short, fully vowelled daily steps on one path, brings every word back for review on widening gaps (1, 2, 4, 8, 16 days), and has a Practise area (verbs, joining words, spelling bee) and Complete extras (real-life scenes, a conversation partner, a weak-spots review).

## The angle
Two ways to use Rafiq, shown as a tour of the real app. The easy way: open it and press Continue; the path does the rest (reading starter, 12 units, five kinds of step, word tiles that grow into typing, review). The specific way: step off the path into Practise, or go further with Complete. Every scene is a recreated screen from the app with its real content.

## Hook (first 2-3 seconds)
The red ink stroke (v6's opener), then Home's Today card with the big green Continue button, pressed on "press Continue".

## Key moments (the middle)
- The path: Reading Arabic ✓, then the 12 units arriving one by one (Greetings … Hobbies).
- A day's step: Meet · Listen · Understand · Practise · Speak lighting up in turn, with the بَيْت word card.
- Word tiles (new): "I go to school by bus every day." — tiles glide into order, turn green, and the app's native voice reads the sentence; "From unit 7: type it".
- Review: بَيْت coming back on day 2, 4, 8, 16; "12 to review".
- Practise menu (as in the app: Weak-spots review, Spelling bee, Beyond the lessons, Real-life scenes, Redo a unit) → verbs: ذَهَبَ in past, present and future → joining words: أُصَلِّي، ___ أَتَناوَلُ الْفَطُورَ with ثُمَّ chosen and read aloud → spelling bee: كِتاب heard, typed, "✓ Correct · fully vowelled".
- Complete: the six real-life scenes (airport, doctor, masjid, restaurant, taxi, a family visit); the conversation partner (the neighbour's line in the native voice, a typed reply, "✓ Good reply."); the weak-spots card.

## Outro / punchline
"One path to follow, and practice whenever you want more. A few minutes a day." → tile, Rafiq, rafiq-arabic.com → Rafiq: "Start your first lesson free at rafiq-arabic.com."

## User flow worth showing
Home → Continue → a step; Practise → a practice area; a tile answer checked; a spelling answered.

## Tone
- Preset: polished (app-store clarity inside v6's manuscript look)
- Creative direction: a guided tour of the real app, one feature per scene, same palette and sound as the website's v6 film
- Interpretation: steady pace, each screen held long enough to read, sequential reveals held, soft crossfades

## Format: landscape — 1920x1080
## Duration: about 79s (voice-led, to cover every feature; the site's v6 film is 62s)
## Revision (TypeSafe review, tools/typesafe-exp/videos_v7_v8.py)
- Reviews are on fixed, widening gaps (1, 2, 4, 8, 16 days), so every "just before you'd forget it" is gone (r06b, the review heading).
- No permanent free tier: the close is "Start your first lesson free at rafiq-arabic.com." (r16, Rafiq's voice).
- New hook (n01b + r02b), new closer (n14b); n08 and n09 merged into n08b; r13 added with the mistake-naming feedback on screen (a gender slip, the note naming it, the fix).
- Trimmed from 90s to about 79s: n04's first sentence cut (the step card already says 5-10 minutes), n03 and n11 re-recorded shorter, r02/n12 folded into the new lines, the two sentence clips (school, usalli) dropped, gaps tightened.
- Transitions: a 0.4s handoff (the old scene is gone 0.1s after the new one starts), and each scene's main content is on screen as it arrives.


## Visual identity (from the project)
Same as v6/v8: paper #f1ece0, card #f7f3ea, ink #17262b, red #b4322a, verdigris #2e7263, gold #a8842c; Karla, IBM Plex Sans Arabic, JetBrains Mono.

## Share copy (draft)
Open Rafiq and press Continue, or go straight to what you need: verbs, joining words, a spelling bee, real-life scenes and a conversation partner. A few minutes of Arabic a day.

## Audio direction
- Role: natural-sound bed (fountain, birdsong) under two voices; no music (as v6)
- Voices: narrator (ElevenLabs "Sarah"), Rafiq's native Arabic voice only on his own-name lines; native app clips for the tile sentence, the joining-words sentence, كِتاب and the neighbour's greeting
- SFX: taps on Continue, tiles, options and Send; pen for typing; soft bong on ✓; page turn between scenes
- Audio-reactive: the background glow follows the voices
- Restraint: nothing over the voices; background about 18 dB under

## Voiceover script (brag-output-v7/vo-script.txt; recordings from tools/v7-lines.json)
| id | voice | line |
|---|---|---|
| n01b | narrator | Want to understand the Arabic you hear every day, and speak it back? |
| r02b | Rafiq | Here's how رَفِيق works. |
| n03s | narrator | One path: a reading starter, then twelve units, from greetings to hobbies. |
| n04t | narrator | Meet new words, hear a conversation, learn one grammar idea, practise, then speak. |
| n05 | narrator | In the early units, you build sentences from word tiles. Later on, you type them yourself. |
| r06b | Rafiq | And رَفِيق brings every word back for review: after a day, then two, four, eight, so it sticks. |
| n07 | narrator | Want something specific? Step off the path, into Practise. |
| n08b | narrator | Drill twenty-one common verbs in three tenses, and the joining words that link your ideas. |
| n10 | narrator | Or play the spelling bee: hear a word, then spell it in Arabic. |
| ar_kitab | app voice | كِتاب — book |
| n11s | narrator | Go further with Complete: real-life scenes, from the airport to the masjid. |
| ar_neighbour | app voice | السَّلامُ عَلَيْكُمْ. أَنا جارُكَ الْجَدِيدُ. — Peace be upon you. I'm your new neighbour. |
| r13 | Rafiq | Type your own replies, and رَفِيق names the mistake, like mixing up masculine and feminine, then helps you fix it. |
| n13 | narrator | And get a review built from the mistakes you keep making. |
| n14b | narrator | One path to follow, and practice whenever you want more. A few minutes a day. |
| r16 | Rafiq | Start your first lesson free at rafiq-arabic.com. |

## Storyboard (voice-timed by src/build.py)
1. **Hook** (n01b): Today card (Unit 1 · step 3 of 9 · Continue), pressed with a tap.
2. **Here's how Rafiq works** (r02b): tile + Rafiq + رَفِيق.
3. **The path** (n03s): Reading Arabic ✓ + the 12 units, lighting up in order.
4. **A step** (n04t): five step cards lighting up in turn.
5. **Word tiles** (n05): tiles glide into the answer line, green ✓; "From unit 7: type it" typed beside it.
6. **Review** (r06b): بَيْت returning on day 2, 4, 8, 16, each gap (+1, +2, +4, +8 days) named as it's said; "12 to review".
7. **Practise** (n07): the app's Practise menu; Beyond the lessons pressed.
8. **Verbs** (n08b, first half): ذَهَبَ table (أَنا / أَنْتَ / هُوَ × past / present / future), cells filling.
9. **Joining words** (n08b, second half): the cloze, ثُمَّ picked, the gap fills, the translation.
10. **Spelling bee** (n10 + كِتاب): 🔊 plays, كتاب typed, green "✓ Correct · fully vowelled", progress bar segment fills.
11. **Complete: scenes** (n11s): COMPLETE badge with all six scene cards at once; airport and masjid marked as they're named.
12. **Conversation** (greeting + r13): neighbour bubble (native voice); a reply with a gender slip (بَيْتُكَ جَمِيلَةٌ) typed and sent; "✓ Good reply — but check this: بَيْت is masculine, so the adjective is too: جَمِيلٌ" with a MASCULINE / FEMININE tag; the slip turns red, then becomes جَمِيلٌ.
13. **Weak spots** (n13): "Masculine and feminine must match" card.
14. **Close** (n14b, r16): the closer as a line; brand, url, Start your first lesson free.
