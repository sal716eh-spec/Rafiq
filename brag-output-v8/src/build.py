#!/usr/bin/env python3
"""v8 — the story. Run from the repo root:  python3 brag-output-v8/src/build.py
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
f.say('r01', V + 'r01.wav', '[Rafiq] رَفِيق. In Arabic, it means companion.', gap=0)
f.say('n02', V + 'n02.wav', "That's what this app was made to be: a companion for anyone studying Arabic.", 0.5)
f.say('n03', V + 'n03.wav', 'In a class, at a madrasa, or on your own, lessons give you new words. Keeping them is the hard part.', 0.7)
f.say('n04', V + 'n04.wav', 'So everything here is built on what memory research says works.', 0.6)
f.say('n05', V + 'n05.wav', "Spacing. Coming back to a word after a gap beats cramming. It's one of the most replicated findings in memory research.", 0.7)
f.say('n06', V + 'n06.wav', 'Testing. Pulling a word from memory strengthens it more than reading it again.', 0.7)
f.say('n07', V + 'n07.wav', 'Habit. A little every day. In one well-known study, a daily habit took about sixty-six days to feel automatic.', 0.7)
f.say('r08', V + 'r08.wav', "[Rafiq] So رَفِيق brings each word back just before you'd forget it, and asks you to recall it, not just reread it.", 0.7)
f.say('n09', V + 'n09.wav', 'Use it to revise alongside your course. Or start from nothing at all.', 0.8)
f.say('n10', V + 'n10.wav', "Can't read Arabic yet? Begin with the twenty-eight letters, in families that share a shape.", 0.7)
f.say('n11', V + 'n11.wav', 'Every letter comes with three words, the letter in red, and a native voice to copy.', 0.7)
f.say('ar_bayt', 'assets/ar/bayt.wav', 'بَيْت — house', 0.35)
f.say('n12', V + 'n12.wav', 'Then the vowel marks, and a listening test to train your ear.', 0.8)
f.say('ar_samak', 'assets/ar/samak.wav', 'سَمَك — fish', 0.4)
f.say('n13', V + 'n13.wav', 'From your first letter to your first conversation.', 2.2)
f.say('n14', V + 'n14.wav', 'A few minutes a day, with a companion beside you.', 1.2)
f.say('r15', V + 'r15.wav', '[Rafiq] Try رَفِيق free today.', 0.5)
TOTAL = round(f.cursor + 2.4, 2)
E = f.events

# scenes: in 0.45s before their first line, out 0.55s after the next one comes in (a crossfade)
order = [('a', 'r01'), ('c', 'n03'), ('d', 'n04'), ('e', 'n05'), ('fz', 'n06'), ('g', 'n07'), ('h', 'r08'),
         ('i', 'n09'), ('j', 'n10'), ('k', 'n11'), ('l', 'n12'), ('m', 'n13'), ('n', 'n14')]
starts = [0.0] + [E[ev]['s'] - 0.45 for _, ev in order[1:]]
for i, (sid, _) in enumerate(order):
    end = starts[i + 1] + 0.55 if i + 1 < len(order) else TOTAL
    f.scene(sid, starts[i], end)

# sound: the opener stroke, page turns between scenes, pen for writing, soft ✓, natural bed
f.sfx('opener', 'assets/sfx-gen/opener.wav', 0.0)
f.sfx('pen-word', 'assets/sfx-gen/pen-write.wav', 0.85, 1.0, 1.6,
      {'version': 1, 'lanes': [{'target': 'volume', 'points': [{'t': 0, 'v': 0.0}, {'t': 0.1, 'v': 0.5}, {'t': 1.3, 'v': 0.5}, {'t': 1.6, 'v': 0.0}]}]})
for i, s in enumerate(starts[1:]):
    f.sfx(f'page{i}', 'assets/sfx-gen/page-turn.wav', s, 0.4)
f.sfx('logo1', 'assets/sfx/impactSoft_medium_002.ogg', E['n02']['s'] + 0.2, 0.55)
for k, dt in enumerate([1.9, 2.6, 3.3, 4.0, 4.7]):
    f.sfx(f'tick{k}', 'assets/sfx-gen/pen-stroke.wav', E['n05']['s'] + dt, 0.35)
f.sfx('ok-test', 'assets/sfx/bong_001.ogg', E['n06']['s'] + 3.1, 0.5)
f.sfx('tap-quiz', 'assets/sfx-gen/tap.wav', E['r08']['s'] + 3.2, 0.5)
f.sfx('ok-quiz', 'assets/sfx/bong_001.ogg', E['r08']['s'] + 3.3, 0.5)
f.sfx('pen-abc', 'assets/sfx-gen/pen-write.wav', E['n10']['s'] + 1.4, 1.0, 3.4,
      {'version': 1, 'lanes': [{'target': 'volume', 'points': [{'t': 0, 'v': 0.0}, {'t': 0.2, 'v': 0.45}, {'t': 3.0, 'v': 0.45}, {'t': 3.4, 'v': 0.0}]}]})
f.sfx('tap-s', 'assets/sfx-gen/tap.wav', E['ar_samak']['e'] + 0.35, 0.5)
f.sfx('ok-s', 'assets/sfx/bong_001.ogg', E['ar_samak']['e'] + 0.45, 0.5)
f.sfx('ok-conv', 'assets/sfx/bong_001.ogg', E['n13']['s'] + 2.0, 0.45)
f.sfx('logo2', 'assets/sfx/impactSoft_medium_002.ogg', E['r15']['s'] - 0.3, 0.55)
f.bed('room', 'assets/amb/room.mp3', 0.5, TOTAL, 0.6)
f.bed('fountain', 'assets/sfx-gen/fountain.wav', 2.8, TOTAL - 0.3, 0.17)
f.bed('birds', 'assets/sfx-gen/birds.wav', 3.4, TOTAL - 0.8, 0.12)
f.sfx('swell', 'assets/sfx-gen/swell.wav', E['n14']['s'] - 0.6, 1.0, 8.0,
      {'version': 1, 'lanes': [{'target': 'volume', 'points': [{'t': 0, 'v': 0.0}, {'t': 2.0, 'v': 0.13}, {'t': 5.5, 'v': 0.13}, {'t': 8.0, 'v': 0.0}]}]})

f.build(os.path.join(HERE, 'index.tpl.html'), TOTAL)
f.vtt(os.path.join(HERE, '..', 'brag.en.vtt'))
print('duration', TOTAL, '· scenes', {k: v for k, v in f.scenes.items()})
