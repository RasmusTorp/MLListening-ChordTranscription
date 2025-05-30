# Real-Time Instrument Chord to MIDI Transcriber

This project listens to live instrument input, uses Spotify’s [Basic Pitch](https://github.com/spotify/basic-pitch) to transcribe notes, infers the underlying harmony, and sends it as MIDI messages to a virtual MIDI port (e.g., for use in Ableton Live).

Ideal for triggering synth pads or harmonies live with your instrument.

---

## How It Works

- Captures audio from your instrument in real time.
- Transcribes pitches using the **Basic Pitch** deep learning model.
- From the pitches it derives which chord if any is being played.
- Sends the detected chord via **MIDI** to an IAC virtual port.
- Allows you to drive instruments in DAWs like **Ableton Live** with your instrument.

---

## Requirements

- Virtual midi ports **IAC Driver** enabled (for virtual MIDI ports).
- Conda (recommended for managing Python version).
- Ableton Live or any DAW that can receive MIDI.

---

## Setup (Python 3.10 via Conda)

```bash
conda create -n ENV_NAME python=3.10
conda activate ENV_NAME

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

## 🔊 Listen on SoundCloud
An example of improvisation in tandem with this ML listening application!
[![Listen on SoundCloud](https://img.shields.io/badge/SoundCloud-Click%20to%20Listen-orange?logo=soundcloud)](https://soundcloud.com/rasmustorp-ai/ml_listening)

## Credits

Built using:
- [Basic Pitch](https://github.com/spotify/basic-pitch) by Spotify
