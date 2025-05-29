# Real-Time instrument Chord to MIDI Transcriber

This project listens to live instrument input, uses Spotify’s [Basic Pitch](https://github.com/spotify/basic-pitch) to transcribe notes, and sends them as MIDI messages to a virtual MIDI port (e.g., for use in Ableton Live).

Ideal for triggering synth pads or harmonies live with your instrument.

---

## How It Works

- Captures audio from your instrument in real time.
- Transcribes pitches using the **Basic Pitch** deep learning model.
- Sends detected notes via **MIDI** to an IAC virtual port on macOS.
- Allows you to drive instruments in DAWs like **Ableton Live** with your instrument.

---

## Requirements

- macOS with **IAC Driver** enabled (for virtual MIDI ports).
- Conda (recommended for managing Python version).
- Ableton Live or any DAW that can receive MIDI.

---

## Setup (Python 3.10 via Conda)

```bash
conda create -n instrument-midi python=3.10
conda activate instrument-midi

pip install -r requirements.txt
```

---

## Set Up MIDI Routing

1. Open **Audio MIDI Setup** → **MIDI Studio**.
2. Enable the **IAC Driver**.
3. Create a port named `ML_listening`.
4. In **Ableton Live**, set `ML_listening` as a MIDI input on a track with a synth/pad.

---

## Run the App

```bash
python frontend.py
```

Open port 7680 in your browser to see the transcribed chords.

You’ll see "Listening..." in the terminal. Start playing your instrument — MIDI notes will be sent as chords to your DAW.

---

## 📝 Credits

Built using:
- [Basic Pitch](https://github.com/spotify/basic-pitch) by Spotify
