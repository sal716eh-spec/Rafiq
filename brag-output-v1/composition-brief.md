# Hyperframes Composition Brief: Rafiq

## Objective
Create a short launch-style brag video for Rafiq, a Modern Standard Arabic learning app.

## Output
- Composition directory: `brag-output/composition/`
- Rendered video: `brag-output/brag.mp4`
- Format: landscape — 1920x1080
- Duration: 20.5 seconds

## Source Material
- Project root: the Rafiq repository
- Primary files read: index.html, site.css, learn.html (words step, chat step), drills-data.js (unit 1 dialogue), vocab-data.js, README.md
- Product name: Rafiq (رَفِيق)
- Tagline / strongest claim: "Learn to read, understand and speak Arabic"
- Key UI to recreate: the New words card and its "What does this mean?" check; the conversation partner with "✓ Good reply."
- Copy that must appear verbatim:
  - رَفِيقُكَ فِي تَعَلُّمِ الْعَرَبِيَّةِ
  - Learn to read, understand and speak Arabic
  - What does this mean?
  - ✓ Good reply.

## Creative Direction
- Tone preset: polished
- Creative direction: quiet premium product film — manuscript paper, ink and one red accent
- Interpretation: four scenes, long settled holds, 0.7s crossfades, mixed-case type, no lists.
- Angle: the Arabic script is the hero; the product is shown doing its two defining moves (meet-and-check a word; reply in your own words and be understood).
- Hook: رَفِيق written at full scale, then the headline.
- Outro: the Arabic hero line, logo tile + "Rafiq", rafiq-arabic.com.
- Avoid: generic SaaS language, abstract filler, redesigning the brand.

## Visual Identity
- Background: #F1ECE0; card #F7F3EA; deep paper #E4DCC9
- Text: #17262B; secondary #5C6E70
- Accent: #B4322A; success #2E7263; decorative gold #A8842C
- Display font: IBM Plex Sans Arabic (local woff2); Latin: Karla; labels: JetBrains Mono
- Visual references: fully vowelled Arabic in ink on paper; rubric-red accent word; logo tile (ر on ink, red dot)

## Storyboard
Creative contract: `brag-output/brag-plan.md`.
1. The word — 0–4.4s — رَفِيق, label, headline
2. Meet a word — 4.0–9.6s — صَدِيق card, four answers, "friend" ✓
3. Have the conversation — 9.2–15.4s — neighbour line, typed reply, "✓ Good reply."
4. Rafiq — 15.0–20.5s — Arabic hero line, logo, URL

## Audio
- Audio role: warm bed with sparse accents
- Music: assets/music/rafiq-bed.mp3 (vol-12 trimmed to 21s), ~0.3, fade in 0–1s, fade out 18.6–20.5s
- Cue source: bundled preset (vol-12, 109.96 BPM). Beat-locks: 8.74, 13.11, 17.47. Beat grid for answers: 6.00/6.56/7.09/7.64.
- Audio-reactive: subtle — RMS swells the background glow and logo shadow (assets/audio-data.js, pre-extracted).
- SFX: interface/bong_001 (✓ moments), interface/click_003 (send), impact/impactSoft_medium_002 (logo), soft volumes 0.5–0.6.

## Hyperframes Instructions
Single standalone index.html, one paused GSAP timeline registered as window.__timelines["main"]; local GSAP, fonts and audio; run `hyperframes check` before render.
