import gradio as gr
from model import MLListening
from basic_pitch import ICASSP_2022_MODEL_PATH
import webbrowser
import time
import threading
import argparse  # <-- Add this import

class GradioInterface:
    def __init__(self, ml_listening):
        self.ml_listening = ml_listening
        self.transcribed_chords = []

    def chord_stream(self):
        last_chord = None
        while True:
            current_chord = self.ml_listening.current_chord
            if current_chord and (not self.transcribed_chords or current_chord != self.transcribed_chords[-1]):
                self.transcribed_chords.append(current_chord)
                yield "\n".join(self.transcribed_chords)
            time.sleep(0.2)

    def create_interface(self):
        with gr.Blocks() as demo:
            gr.Markdown("## Real-time Chord Transcription")
            chord_output = gr.Textbox(label="Transcribed Chords", interactive=False)
            demo.load(self.chord_stream, outputs=chord_output)
        return demo

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Real-time Chord Transcription Frontend")
    parser.add_argument("--midi_bus", type=str, default="IAC Driver ML_listening", help="MIDI bus name")
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

    threading.Thread(target=app.start_transcription, daemon=True).start()

    gradio_app = GradioInterface(app)
    gradio_app.create_interface().launch(server_port=7860)

    webbrowser.open("http://localhost:7860", new=2)  # Open in a new tab