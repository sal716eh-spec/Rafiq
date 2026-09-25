# Brag Plan v7: Rafiq (رَفِيق) — everything inside

## What is this app?
Rafiq teaches Modern Standard Arabic in short, fully vowelled daily steps on one path, brings every word back for review before you'd forget it, and has a Practise area (verbs, joining words, spelling bee) and Complete extras (real-life scenes, a conversation partner, a weak-spots review).

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
"Your journey, or something specific. A few minutes a day." → tile, Rafiq, rafiq-arabic.com → Rafiq: "Try رَفِيق free today."

## User flow worth showing
Home → Continue → a step; Practise → a practice area; a tile answer checked; a spelling answered.

## Tone
- Preset: polished (app-store clarity inside v6's manuscript look)
- Creative direction: a guided tour of the real app, one feature per scene, same palette and sound as the website's v6 film
- Interpretation: steady pace, each screen held long enough to read, sequential reveals held, soft crossfades

## Format: landscape — 1920x1080
## Duration: about 85s (voice-led, to cover every feature; the site's v6 film is 62s)

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

## Voiceover script (tools/v7-lines.json)
| id | voice | line |
|---|---|---|
| n01 | narrator | Here's the easiest way to learn Arabic: open the app, and press Continue. |
| r02 | Rafiq | This is رَفِيق. Let me show you everything inside. |
| n03 | narrator | First, your journey. One path: a reading starter, then twelve units, from greetings to hobbies. |
| n04 | narrator | Each step takes five to ten minutes. Meet new words, hear a conversation, learn one grammar idea, practise, then speak. |
| n05 | narrator | In the early units, you build sentences from word tiles. Later on, you type them yourself. |
| — | app voice | أَذْهَبُ إِلى الْمَدْرَسَةِ بِالْحافِلَةِ كُلَّ يَوْمٍ |
| r06 | Rafiq | And رَفِيق brings every word back for review, just before you'd forget it. |
| n07 | narrator | Want something specific? Step off the path, into Practise. |
| n08 | narrator | Drill twenty-one common verbs in the past, present and future. |
| n09 | narrator | Learn the joining words that link your ideas together. |
| — | app voice | أُصَلِّي، ثُمَّ أَتَناوَلُ الْفَطُورَ. |
| n10 | narrator | Or play the spelling bee: hear a word, then spell it in Arabic. |
| — | app voice | كِتاب |
| n11 | narrator | Go further with Complete. Practise real-life scenes, from the airport to the masjid. |
| — | app voice | السَّلامُ عَلَيْكُمْ. أَنا جارُكَ الْجَدِيدُ. |
| n12 | narrator | Have the conversation yourself, and get feedback on every reply. |
| n13 | narrator | And get a review built from the mistakes you keep making. |
| n14 | narrator | Your journey, or something specific. A few minutes a day. |
| r15 | Rafiq | Try رَفِيق free today. (v6's recording) |

## Storyboard (voice-timed by src/build.py)
1. **Continue** (n01): Today card (Unit 1 · step 3 of 9 · Continue), pressed with a tap.
2. **Meet Rafiq** (r02): tile + Rafiq + رَفِيق.
3. **The path** (n03): Reading Arabic ✓ + 12 unit chips arriving in order.
4. **A step** (n04): five step cards lighting up in turn; the بَيْت card beside Meet.
5. **Word tiles** (n05 + sentence): tiles glide into the answer line, green ✓, the native voice reads it; "From unit 7 you type it" typed below.
6. **Review** (r06): بَيْت returning on day 2, 4, 8, 16; "12 to review".
7. **Practise** (n07): the app's Practise menu; Beyond the lessons pressed.
8. **Verbs** (n08): ذَهَبَ table (أَنا / أَنْتَ / هُوَ × past / present / future), cells filling.
9. **Joining words** (n09 + sentence): the cloze, ثُمَّ picked, the gap fills, the native voice reads it.
10. **Spelling bee** (n10 + كِتاب): 🔊 plays, كتاب typed, green "✓ Correct · fully vowelled", progress bar segment fills.
11. **Complete: scenes** (n11): COMPLETE badge; six scene cards one by one.
12. **Conversation** (greeting + n12): neighbour bubble (native voice), reply typed, Send, "✓ Good reply."
13. **Weak spots** (n13): "Masculine and feminine must match" card.
14. **Close** (n14, r15): the two ways as a line; brand, url, Try it free.
