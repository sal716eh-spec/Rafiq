"""Shared builder for Rafiq's voice-led videos (brag-output-v7, -v8).

A video's src/build.py lays out voice lines and native Arabic clips in order
(each line's real length decides when the next one starts), names the scene
windows and sound cues, and this module writes:
  composition/index.html        the template with every time filled in
  composition/assets/audio-data.js   per-frame loudness of the voices (glow)
  ../brag.en.vtt                captions
Template placeholders: {{TIMES}} (JSON of every event's start/end),
{{SCENE:id}} (data-start/data-duration), {{AUDIO}}, {{DURATION}}.
"""
import json, os, re, subprocess, array, math

def length(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                          '-of', 'csv=p=0', path], capture_output=True, text=True).stdout
    return float(out.strip())

class Film:
    def __init__(self, comp):
        self.comp = comp
        self.cursor = 0.0
        self.events = {}      # id -> {s, e}
        self.voice = []       # (id, file, start, dur, caption) — voices and clips, for mix + captions
        self.audio = []       # extra <audio>: (id, file, start, dur, vol, automation)
        self.scenes = {}
        self.track = 20

    def mark(self, id, s, e):
        self.events[id] = {'s': round(s, 3), 'e': round(e, 3)}

    def say(self, id, file, caption, gap=0.5):
        """A voice line or native clip, gap seconds after the last one ends."""
        s = self.cursor + gap
        d = length(os.path.join(self.comp, file))
        self.voice.append((id, file, round(s, 3), round(d, 3), caption))
        self.mark(id, s, s + d)
        self.cursor = s + d
        return self.events[id]

    def wait(self, sec):
        self.cursor += sec

    def scene(self, id, start, end):
        self.scenes[id] = (round(start, 3), round(end - start, 3))

    def sfx(self, id, file, start, vol=1.0, dur=None, auto=None):
        d = dur if dur is not None else length(os.path.join(self.comp, file))
        self.audio.append((id, file, round(start, 3), round(d, 3), vol, auto))

    def bed(self, id, file, start, end, level, seg=None, fade=1.2):
        """A looping ambience: overlapping segments of one file, each faded in and out."""
        full = length(os.path.join(self.comp, file))
        seg = min(seg or full, full)
        t, k = start, 0
        while t < end - 0.5:
            d = min(seg, end - t)
            fi = 1.5 if k == 0 else 0.5
            pts = [{'t': 0, 'v': 0.0}, {'t': round(fi, 2), 'v': level},
                   {'t': round(max(fi, d - fade), 2), 'v': level}, {'t': round(d, 2), 'v': 0.0}]
            self.sfx(f'{id}{k}', file, t, 1.0, d, {'version': 1, 'lanes': [{'target': 'volume', 'points': pts}]})
            t += d - 0.5; k += 1

    def _audio_html(self):
        rows = []
        for id, file, s, d, cap in self.voice:
            rows.append(f'<audio id="{id}" src="{file}" data-start="{s}" data-duration="{d}" data-track-index="{self._t()}"></audio>')
        for id, file, s, d, vol, auto in self.audio:
            a = f" data-automation='{json.dumps(auto)}'" if auto else ''
            rows.append(f'<audio id="{id}" src="{file}" data-start="{s}" data-duration="{d}" data-track-index="{self._t()}" data-volume="{vol}"{a}></audio>')
        return '\n      '.join(rows)

    def _t(self):
        self.track += 1
        return self.track

    def rms(self, total, fps=30):
        """Per-frame loudness of the voice track (0..1), for the glow."""
        mixed = os.path.join(self.comp, 'assets', '.voices.raw')
        inputs, filt = [], []
        for i, (id, file, s, d, cap) in enumerate(self.voice):
            inputs += ['-i', os.path.join(self.comp, file)]
            ms = int(s * 1000)
            filt.append(f'[{i}:a]aformat=channel_layouts=mono,adelay={ms}|{ms}[a{i}]')
        filt.append(''.join(f'[a{i}]' for i in range(len(self.voice))) + f'amix=inputs={len(self.voice)}:normalize=0,apad[m]')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *inputs, '-filter_complex', ';'.join(filt),
                        '-map', '[m]', '-t', str(total), '-ac', '1', '-ar', '8000', '-f', 's16le', mixed], check=True)
        pcm = array.array('h'); pcm.frombytes(open(mixed, 'rb').read()); os.remove(mixed)
        step = 8000 // fps
        vals = [math.sqrt(sum(x * x for x in pcm[i:i + step]) / max(1, len(pcm[i:i + step]))) for i in range(0, len(pcm), step)]
        peak = max(vals) or 1
        vals = [round(min(1, v / (peak * 0.8)), 3) for v in vals]
        with open(os.path.join(self.comp, 'assets', 'audio-data.js'), 'w') as f:
            f.write('window.AUDIO_DATA=' + json.dumps({'fps': fps, 'rms': vals}, separators=(',', ':')) + ';\n')

    def vtt(self, path):
        def ts(t):
            h, r = divmod(t, 3600); m, s = divmod(r, 60)
            return f'{int(h):02d}:{int(m):02d}:{s:06.3f}'
        cues = ['WEBVTT', '']
        for n, (id, file, s, d, cap) in enumerate(self.voice, 1):
            cues += [str(n), f'{ts(s)} --> {ts(s + d)}', cap, '']
        open(path, 'w', encoding='utf-8').write('\n'.join(cues))

    def build(self, tpl, total):
        html = open(tpl, encoding='utf-8').read()
        html = html.replace('{{TIMES}}', json.dumps(self.events))
        html = html.replace('{{DURATION}}', str(round(total, 2)))
        html = html.replace('{{AUDIO}}', self._audio_html())
        def sc(m):
            s, d = self.scenes[m.group(1)]
            return f'data-start="{s}" data-duration="{d}"'
        html = re.sub(r'\{\{SCENE:(\w+)\}\}', sc, html)
        left = re.findall(r'\{\{[^}]+\}\}', html)
        assert not left, left
        open(os.path.join(self.comp, 'index.html'), 'w', encoding='utf-8').write(html)
        self.rms(total)
