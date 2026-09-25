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
f.cursor = 0.9
f.say('n01', V + 'n01.wav', "Here's the easiest way to learn Arabic: open the app, and press Continue.", gap=0)
f.say('r02', V + 'r02.wav', '[Rafiq] This is رَفِيق. Let me show you everything inside.', 0.7)
f.say('n03', V + 'n03.wav', 'First, your journey. One path: a reading starter, then twelve units, from greetings to hobbies.', 0.7)
f.say('n04', V + 'n04.wav', 'Each step takes five to ten minutes. Meet new words, hear a conversation, learn one grammar idea, practise, then speak.', 0.6)
f.say('n05', V + 'n05.wav', 'In the early units, you build sentences from word tiles. Later on, you type them yourself.', 0.7)
f.say('ar_school', 'assets/ar/school.wav', 'أَذْهَبُ إِلى الْمَدْرَسَةِ بِالْحافِلَةِ كُلَّ يَوْمٍ — I go to school by bus every day.', 0.4)
f.say('r06', V + 'r06.wav', "[Rafiq] And رَفِيق brings every word back for review, just before you'd forget it.", 0.8)
f.say('n07', V + 'n07.wav', 'Want something specific? Step off the path, into Practise.', 0.8)
f.say('n08', V + 'n08.wav', 'Drill twenty-one common verbs in the past, present and future.', 0.7)
f.say('n09', V + 'n09.wav', 'Learn the joining words that link your ideas together.', 0.7)
f.say('ar_usalli', 'assets/ar/usalli.wav', 'أُصَلِّي، ثُمَّ أَتَناوَلُ الْفَطُورَ. — I pray, then I have breakfast.', 1.0)
f.say('n10', V + 'n10.wav', 'Or play the spelling bee: hear a word, then spell it in Arabic.', 0.8)
f.say('ar_kitab', 'assets/ar/kitab.wav', 'كِتاب — book', 0.4)
f.wait(2.2)                                   # the learner spells it
f.say('n11', V + 'n11.wav', 'Go further with Complete. Practise real-life scenes, from the airport to the masjid.', 0.6)
f.say('ar_neighbour', 'assets/ar/neighbour.wav', "السَّلامُ عَلَيْكُمْ. أَنا جارُكَ الْجَدِيدُ. — Peace be upon you. I'm your new neighbour.", 0.8)
f.say('n12', V + 'n12.wav', 'Have the conversation yourself, and get feedback on every reply.', 0.4)
f.say('n13', V + 'n13.wav', 'And get a review built from the mistakes you keep making.', 1.3)
f.say('n14', V + 'n14.wav', 'Your journey, or something specific. A few minutes a day.', 1.0)
f.say('r15', V + 'r15.wav', '[Rafiq] Try رَفِيق free today.', 0.5)
TOTAL = round(f.cursor + 2.4, 2)
E = f.events

order = [('a', 'n01'), ('b', 'r02'), ('c', 'n03'), ('d', 'n04'), ('e', 'n05'), ('fz', 'r06'), ('g', 'n07'), ('h', 'n08'),
         ('i', 'n09'), ('j', 'n10'), ('k', 'n11'), ('l', 'ar_neighbour'), ('m', 'n13'), ('n', 'n14')]
starts = [0.0] + [E[ev]['s'] - 0.45 for _, ev in order[1:]]
for i, (sid, _) in enumerate(order):
    end = starts[i + 1] + 0.55 if i + 1 < len(order) else TOTAL
    f.scene(sid, starts[i], end)

f.sfx('opener', 'assets/sfx-gen/opener.wav', 0.0)
for i, s in enumerate(starts[1:]):
    f.sfx(f'page{i}', 'assets/sfx-gen/page-turn.wav', s, 0.4)
f.sfx('tap-cont', 'assets/sfx-gen/tap.wav', E['n01']['e'] - 0.5, 0.55)
f.sfx('logo1', 'assets/sfx/impactSoft_medium_002.ogg', E['r02']['s'] - 0.1, 0.55)
for k in range(4):
    f.sfx(f'tile{k}', 'assets/sfx/click_003.ogg', E['n05']['s'] + 0.9 + k * 0.45, 0.6, 0.05)
f.sfx('ok-tiles', 'assets/sfx/bong_001.ogg', E['n05']['s'] + 2.9, 0.5)
f.sfx('pen-type', 'assets/sfx-gen/pen-write.wav', E['n05']['s'] + 3.6, 1.0, 1.5,
      {'version': 1, 'lanes': [{'target': 'volume', 'points': [{'t': 0, 'v': 0.0}, {'t': 0.1, 'v': 0.4}, {'t': 1.2, 'v': 0.4}, {'t': 1.5, 'v': 0.0}]}]})
for k, dt in enumerate([0.6, 1.2, 1.8, 2.4]):
    f.sfx(f'rev{k}', 'assets/sfx-gen/pen-stroke.wav', E['r06']['s'] + dt, 0.35)
f.sfx('tap-beyond', 'assets/sfx-gen/tap.wav', E['n07']['e'] - 0.3, 0.5)
f.sfx('tap-then', 'assets/sfx-gen/tap.wav', E['n09']['e'] + 0.2, 0.5)
f.sfx('ok-then', 'assets/sfx/bong_001.ogg', E['n09']['e'] + 0.3, 0.45)
f.sfx('pen-spell', 'assets/sfx-gen/pen-write.wav', E['ar_kitab']['e'] + 0.2, 1.0, 1.4,
      {'version': 1, 'lanes': [{'target': 'volume', 'points': [{'t': 0, 'v': 0.0}, {'t': 0.1, 'v': 0.45}, {'t': 1.1, 'v': 0.45}, {'t': 1.4, 'v': 0.0}]}]})
f.sfx('tap-check', 'assets/sfx-gen/tap.wav', E['ar_kitab']['e'] + 1.6, 0.5)
f.sfx('ok-spell', 'assets/sfx/bong_001.ogg', E['ar_kitab']['e'] + 1.7, 0.5)
f.sfx('tap-send', 'assets/sfx-gen/tap.wav', E['n12']['s'] + 2.2, 0.55)
f.sfx('ok-reply', 'assets/sfx/bong_001.ogg', E['n12']['s'] + 2.9, 0.5)
f.sfx('logo2', 'assets/sfx/impactSoft_medium_002.ogg', E['r15']['s'] - 0.3, 0.55)
f.bed('room', 'assets/amb/room.mp3', 0.5, TOTAL, 0.6)
f.bed('fountain', 'assets/sfx-gen/fountain.wav', E['r02']['s'] - 0.4, TOTAL - 0.3, 0.17)
f.bed('birds', 'assets/sfx-gen/birds.wav', E['r02']['s'], TOTAL - 0.8, 0.12)
f.sfx('swell', 'assets/sfx-gen/swell.wav', E['n14']['s'] - 0.6, 1.0, 8.0,
      {'version': 1, 'lanes': [{'target': 'volume', 'points': [{'t': 0, 'v': 0.0}, {'t': 2.0, 'v': 0.13}, {'t': 5.5, 'v': 0.13}, {'t': 8.0, 'v': 0.0}]}]})

f.build(os.path.join(HERE, 'index.tpl.html'), TOTAL)
f.vtt(os.path.join(HERE, '..', 'brag.en.vtt'))
print('duration', TOTAL, '· scenes', f.scenes)
