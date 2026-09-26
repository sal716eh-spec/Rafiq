#!/usr/bin/env python3
"""v7 — everything inside. Run from the repo root:  python3 brag-output-v7/src/build.py
Lays the voice out line by line (each recording's own length sets the pace),
then writes composition/index.html from src/index.tpl.html, the captions and
the glow data (tools/vidbuild.py)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'tools'))
from vidbuild import Film

COMP = os.path.join(HERE, '..', 'composition')
f = Film(COMP)
V = 'assets/vo/'
f.cursor = 0.5
f.say('n01b', V + 'n01b.wav', 'Want to understand the Arabic you hear every day, and speak it back?', gap=0)
f.say('r02b', V + 'r02b.wav', "[Rafiq] Here's how رَفِيق works.", 0.35)
f.say('n03s', V + 'n03s.wav', 'One path: a reading starter, then twelve units, from greetings to hobbies.', 0.45)
f.say('n04t', V + 'n04t.wav', 'Meet new words, hear a conversation, learn one grammar idea, practise, then speak.', 0.45)   # the normalised n04 from 2.40s: its first sentence ("Each step takes five to ten minutes.") is on the card
f.say('n05', V + 'n05.wav', 'In the early units, you build sentences from word tiles. Later on, you type them yourself.', 0.45)
f.say('r06b', V + 'r06b.wav', '[Rafiq] And رَفِيق brings every word back for review: after a day, then two, four, eight, so it sticks.', 0.6)
f.say('n07', V + 'n07.wav', 'Want something specific? Step off the path, into Practise.', 0.45)
f.say('n08b', V + 'n08b.wav', 'Drill twenty-one common verbs in three tenses, and the joining words that link your ideas.', 0.45)
f.say('n10', V + 'n10.wav', 'Or play the spelling bee: hear a word, then spell it in Arabic.', 0.9)
f.say('ar_kitab', 'assets/ar/kitab.wav', 'كِتاب — book', 0.35)
f.wait(1.8)                                   # the learner spells it
f.say('n11s', V + 'n11s.wav', 'Go further with Complete: real-life scenes, from the airport to the masjid.', 0.8)
f.say('ar_neighbour', 'assets/ar/neighbour.wav', "السَّلامُ عَلَيْكُمْ. أَنا جارُكَ الْجَدِيدُ. — Peace be upon you. I'm your new neighbour.", 0.5)
f.say('r13', V + 'r13.wav', '[Rafiq] Type your own replies, and رَفِيق names the mistake, like mixing up masculine and feminine, then helps you fix it.', 0.4)
f.say('n13', V + 'n13.wav', 'And get a review built from the mistakes you keep making.', 0.6)
f.say('n14b', V + 'n14b.wav', 'One path to follow, and practice whenever you want more. A few minutes a day.', 0.6)
f.say('r16', V + 'r16.wav', '[Rafiq] Start your first lesson free at rafiq-arabic.com.', 0.4)
TOTAL = round(f.cursor + 1.6, 2)
E = f.events

# scenes: each comes in 0.45s before its first line; the one before fades out over
# 0.4s, ending 0.1s after the new one starts (a short handoff, never an empty frame).
# Verbs and joining words share n08b: the cut is on its comma.
order = [('a', 'n01b'), ('b', 'r02b'), ('c', 'n03s'), ('d', 'n04t'), ('e', 'n05'), ('fz', 'r06b'), ('g', 'n07'), ('h', 'n08b'),
         ('i', None), ('j', 'n10'), ('k', 'n11s'), ('l', 'ar_neighbour'), ('m', 'n13'), ('n', 'n14b')]
IJ = E['n08b']['s'] + 2.45
starts = [0.0] + [E[ev]['s'] - 0.45 if ev else IJ for _, ev in order[1:]]
for i, (sid, _) in enumerate(order):
    end = starts[i + 1] + 0.1 if i + 1 < len(order) else TOTAL
    f.scene(sid, starts[i], end)

f.sfx('opener', 'assets/sfx-gen/opener.wav', 0.0)
for i, s in enumerate(starts[1:]):
    f.sfx(f'page{i}', 'assets/sfx-gen/page-turn.wav', s, 0.4)
f.sfx('tap-cont', 'assets/sfx-gen/tap.wav', E['n01b']['e'] - 0.3, 0.55)
f.sfx('logo1', 'assets/sfx/impactSoft_medium_002.ogg', E['r02b']['s'] - 0.1, 0.55)
for k in range(4):
    f.sfx(f'tile{k}', 'assets/sfx/click_003.ogg', E['n05']['s'] + 0.9 + k * 0.45, 0.6, 0.05)
f.sfx('ok-tiles', 'assets/sfx/bong_001.ogg', E['n05']['s'] + 2.9, 0.5)
f.sfx('pen-type', 'assets/sfx-gen/pen-write.wav', E['n05']['s'] + 3.6, 1.0, 1.5,
      {'version': 1, 'lanes': [{'target': 'volume', 'points': [{'t': 0, 'v': 0.0}, {'t': 0.1, 'v': 0.4}, {'t': 1.2, 'v': 0.4}, {'t': 1.5, 'v': 0.0}]}]})
for k, dt in enumerate([3.0, 4.1, 4.6, 5.1]):          # r06b: "after a day, then two, four, eight"
    f.sfx(f'rev{k}', 'assets/sfx-gen/pen-stroke.wav', E['r06b']['s'] + dt, 0.35)
f.sfx('tap-beyond', 'assets/sfx-gen/tap.wav', E['n07']['e'] - 0.3, 0.5)
f.sfx('tap-then', 'assets/sfx-gen/tap.wav', E['n08b']['e'] - 0.9, 0.5)
f.sfx('ok-then', 'assets/sfx/bong_001.ogg', E['n08b']['e'] - 0.8, 0.45)
f.sfx('pen-spell', 'assets/sfx-gen/pen-write.wav', E['ar_kitab']['e'] + 0.15, 1.0, 1.1,
      {'version': 1, 'lanes': [{'target': 'volume', 'points': [{'t': 0, 'v': 0.0}, {'t': 0.1, 'v': 0.45}, {'t': 0.8, 'v': 0.45}, {'t': 1.1, 'v': 0.0}]}]})
f.sfx('tap-check', 'assets/sfx-gen/tap.wav', E['ar_kitab']['e'] + 1.1, 0.5)
f.sfx('ok-spell', 'assets/sfx/bong_001.ogg', E['ar_kitab']['e'] + 1.2, 0.5)
f.sfx('pen-reply', 'assets/sfx-gen/pen-write.wav', E['r13']['s'] + 0.1, 1.0, 1.6,
      {'version': 1, 'lanes': [{'target': 'volume', 'points': [{'t': 0, 'v': 0.0}, {'t': 0.1, 'v': 0.35}, {'t': 1.3, 'v': 0.35}, {'t': 1.6, 'v': 0.0}]}]})
f.sfx('tap-send', 'assets/sfx-gen/tap.wav', E['r13']['s'] + 1.8, 0.55)
f.sfx('pen-fix', 'assets/sfx-gen/pen-stroke.wav', E['r13']['s'] + 5.75, 0.4)
f.sfx('ok-fix', 'assets/sfx/bong_001.ogg', E['r13']['s'] + 6.0, 0.45)
f.sfx('logo2', 'assets/sfx/impactSoft_medium_002.ogg', E['r16']['s'] - 0.3, 0.55)
f.bed('room', 'assets/amb/room.mp3', 0.5, TOTAL, 0.6)
f.bed('fountain', 'assets/sfx-gen/fountain.wav', E['r02b']['s'] - 0.4, TOTAL - 0.3, 0.17)
f.bed('birds', 'assets/sfx-gen/birds.wav', E['r02b']['s'], TOTAL - 0.8, 0.12)
f.sfx('swell', 'assets/sfx-gen/swell.wav', E['n14b']['s'] - 0.6, 1.0, 8.0,
      {'version': 1, 'lanes': [{'target': 'volume', 'points': [{'t': 0, 'v': 0.0}, {'t': 2.0, 'v': 0.13}, {'t': 5.5, 'v': 0.13}, {'t': 8.0, 'v': 0.0}]}]})

f.build(os.path.join(HERE, 'index.tpl.html'), TOTAL)
f.vtt(os.path.join(HERE, '..', 'brag.en.vtt'))
print('duration', TOTAL, '· scenes', f.scenes)
