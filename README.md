# 🎸 Real-Time Guitar Chord to MIDI Transcriber

This project listens to live guitar input, uses Spotify’s [Basic Pitch](https://github.com/spotify/basic-pitch) to transcribe notes, and sends them as MIDI messages to a virtual MIDI port (e.g., for use in Ableton Live).

Ideal for triggering synth pads or harmonies live with your guitar.

---

## 🧠 How It Works

- Captures audio from your guitar in real time.
- Transcribes pitches using the **Basic Pitch** deep learning model.
- Sends detected notes via **MIDI** to an IAC virtual port on macOS.
- Allows you to drive instruments in DAWs like **Ableton Live** with your guitar.

---

## 🧰 Requirements

- macOS with **IAC Driver** enabled (for virtual MIDI ports).
- Conda (recommended for managing Python version).
- Ableton Live or any DAW that can receive MIDI.

---

## 🐍 Setup (Python 3.10 via Conda)

```bash
conda create -n guitar-midi python=3.10
conda activate guitar-midi

pip install -r requirements.txt
```

**requirements.txt**
```txt
sounddevice
numpy
basic-pitch
mido
python-rtmidi
torch
torchaudio
soundfile
```

---

## 🎹 Set Up MIDI Routing

1. Open **Audio MIDI Setup** → **MIDI Studio**.
2. Enable the **IAC Driver**.
3. Create a port named `ML_listening`.
4. In **Ableton Live**, set `ML_listening` as a MIDI input on a track with a synth/pad.

---

## 🚀 Run the App

```bash
python main.py
```

You’ll see "Listening..." in the terminal. Start playing your guitar — MIDI notes will be sent as chords to your DAW.

---

## 📦 Todo / Extensions

- Chord labeling (e.g., Cmaj, Am7)
- Sustain logic (hold chord until new one is detected)
- CLI controls (e.g., freeze, retrigger manually)

---

## 📝 Credits

Built using:
- [Basic Pitch](https://github.com/spotify/basic-pitch) by Spotify
- [SoundDevice](https://python-sounddevice.readthedocs.io/)
- [Mido + RtMidi](https://mido.readthedocs.io/)