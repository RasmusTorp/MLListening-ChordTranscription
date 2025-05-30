
import argparse
from basic_pitch import ICASSP_2022_MODEL_PATH
import time

from model import MLListening

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Real-time Chord Transcription Frontend")
    parser.add_argument("--midi_bus", type=str, default="IAC Driver Bus 1", help="MIDI bus name")
    parser.add_argument("--channels", type=int, default=1, help="Number of audio channels")
    parser.add_argument("--sample_rate", type=int, default=22050, help="Audio sample rate")
    parser.add_argument("--block_seconds", type=float, default=1.0, help="Block size in seconds")
    parser.add_argument("--repeat_same_chords", action="store_true", help="Repeat same chord in output (default: False)")
    parser.add_argument("--midi_offset", type=int, default=60, help="MIDI offset")
    parser.add_argument("--port", type=int, default=7860, help="Gradio server port")
    args = parser.parse_args()
    
    app = MLListening(
            basic_pitch_path=ICASSP_2022_MODEL_PATH,
            midi_bus=args.midi_bus,
            channels=args.channels,
            sample_rate=args.sample_rate,
            block_seconds=args.block_seconds,
            repeat_same_chords=args.repeat_same_chords,
            midi_offset=args.midi_offset
            )
    
    # Test
    chords = [[60, 64, 67], [62, 65, 69], [64, 67, 71]]
    i = 0
    while True:
        i += 1
        if i == len(chords):
            i = 0
        app.send_midi_pad(chords[i])
        time.sleep(4)