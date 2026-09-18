#!/usr/bin/env python3
"""Procedural retro SFX + synthwave loop for the LAST TOKEN scene, plus OpenAI TTS announcer lines.

    python3 scripts/make-sfx.py            # writes into build/audio/
Needs numpy; TTS lines need OPENAI_API_KEY in the environment (skipped otherwise).
Import each WAV into Spline with ⌘O → Sound, then assign it to an Audio action in the Edit Event popover.
"""
import json, os, urllib.request, wave
import numpy as np

SR = 44100
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "build", "audio")
os.makedirs(OUT, exist_ok=True)


def save(name, x):
    x = np.clip(x, -1, 1)
    with wave.open(os.path.join(OUT, name), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())
    print(name, round(len(x) / SR, 2), "s")


def env(n, a=0.005, d=0.1, s=0.6, r=0.1):
    e = np.ones(n); A, D, R = int(a * SR), int(d * SR), int(r * SR)
    e[:A] = np.linspace(0, 1, A); e[A:A + D] = np.linspace(1, s, D); e[A + D:n - R] = s; e[n - R:] = np.linspace(s, 0, R)
    return e


def square(f, n, duty=0.5):
    t = np.arange(n) / SR
    return np.where((t * f) % 1 < duty, 1.0, -1.0)


def saw(f, n):
    t = np.arange(n) / SR
    return 2 * ((t * f) % 1) - 1


# --- camera flash: capacitor whine sweep + click + shutter noise
n = int(0.7 * SR); t = np.arange(n) / SR
save("sfx-flash.wav",
     np.sin(2 * np.pi * (1800 + 2600 * t / 0.7) * t) * np.exp(-t * 6) * 0.35
     + (np.random.rand(n) * 2 - 1) * np.exp(-t * 120) * 0.9
     + (np.random.rand(n) * 2 - 1) * np.exp(-(t - 0.12) ** 2 / 0.0004) * 0.5)

# --- dance hit: 8-bit arpeggio stab
notes = [523.25, 659.25, 783.99, 1046.5]; seg = int(0.09 * SR)
out = np.zeros(seg * 4 + int(0.25 * SR))
for i, f in enumerate(notes):
    out[i * seg:(i + 1) * seg] += square(f, seg, 0.25) * env(seg, 0.002, 0.02, 0.7, 0.03) * 0.5
tail = int(0.25 * SR); tt = np.arange(tail) / SR
out[seg * 4:] += square(1046.5 * (1 + 0.01 * np.sin(2 * np.pi * 6 * tt)), tail, 0.5) * np.exp(-tt * 9) * 0.5
save("sfx-dance.wav", out)

# --- jump: rising boing
n = int(0.35 * SR); t = np.arange(n) / SR
f = 300 + 900 * (t / 0.35) ** 0.7
save("sfx-jump.wav", np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t * 7) * 0.45)

# --- servo footsteps: two steps per 0.5 s, loops cleanly (Loop: Infinite in the 'move' container)
n = int(0.5 * SR); t = np.arange(n) / SR; out = np.zeros(n)
for k in (0.0, 0.25):
    m = (t >= k) & (t < k + 0.18); tt = t[m] - k
    out[m] += (np.sin(2 * np.pi * (220 + 160 * np.sin(2 * np.pi * tt / 0.18)) * tt) * np.hanning(m.sum()) * 0.22
               + (np.random.rand(m.sum()) * 2 - 1) * np.exp(-tt * 90) * 0.35)
save("sfx-servo-walk.wav", out)

# --- synthwave loop: 120 BPM, 4 bars Am F C G — kick, snare, hats, square bass, saw arp
bpm = 120; beat = 60 / bpm; bar = 4 * beat; mix = np.zeros(int(4 * bar * SR))
chords = [[220.0, 261.63, 329.63], [174.61, 220.0, 261.63], [130.81, 164.81, 196.0], [196.0, 246.94, 293.66]]
for b in range(4):
    root = chords[b][0]
    for s in range(8):
        st = int((b * bar + s * beat / 2) * SR); ln = int(beat / 2 * SR)
        mix[st:st + ln] += square(root / 2 if s % 2 == 0 else root, ln, 0.5) * env(ln, 0.003, 0.05, 0.5, 0.05) * 0.28
    for s in range(16):
        st = int((b * bar + s * beat / 4) * SR); ln = int(beat / 4 * SR)
        mix[st:st + ln] += saw(chords[b][s % 3] * 2, ln) * env(ln, 0.002, 0.03, 0.4, 0.03) * 0.12
    for k in range(4):
        st = int((b * bar + k * beat) * SR); ln = int(0.25 * SR); tk = np.arange(ln) / SR
        mix[st:st + ln] += np.sin(2 * np.pi * (150 * np.exp(-tk * 18)) * tk) * np.exp(-tk * 10) * 0.9
    for k in (1, 3):
        st = int((b * bar + k * beat) * SR); ln = int(0.2 * SR); tk = np.arange(ln) / SR
        mix[st:st + ln] += (np.random.rand(ln) * 2 - 1) * np.exp(-tk * 22) * 0.45
    for k in range(8):
        st = int((b * bar + k * beat / 2) * SR); ln = int(0.05 * SR); tk = np.arange(ln) / SR
        mix[st:st + ln] += (np.random.rand(ln) * 2 - 1) * np.exp(-tk * 80) * 0.15
save("loop-synthwave.wav", mix / (np.max(np.abs(mix)) + 1e-6) * 0.9)

# --- announcer lines (OpenAI TTS)
key = os.environ.get("OPENAI_API_KEY")
LINES = [("vo-say-cheese.wav", "Say cheese!"),
         ("vo-insert-coin.wav", "Insert coin. Last token!"),
         ("vo-cheer.wav", "Woo-hoo! Yeah!"),
         ("vo-hey.wav", "Hey there!"),
         ("vo-nice.wav", "Nice! Thumbs up!"),
         ("vo-dj.wav", "Hmm... where's the DJ?"),
         ("vo-break.wav", "Break it down!"),
         ("vo-zombie.wav", "Braaains... beep boop.")]
if key:
    for name, text in LINES:
        body = json.dumps({"model": "gpt-4o-mini-tts", "voice": "ash", "input": text, "response_format": "wav",
                           "instructions": "1980s arcade cabinet announcer: excited, punchy, slightly robotic, big smile."}).encode()
        req = urllib.request.Request("https://api.openai.com/v1/audio/speech", data=body,
                                     headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            open(os.path.join(OUT, name), "wb").write(r.read())
        print(name)
else:
    print("OPENAI_API_KEY not set — skipped the announcer lines")
