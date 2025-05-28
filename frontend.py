import gradio as gr
from main import MLListening
from basic_pitch import ICASSP_2022_MODEL_PATH
import time

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
    app = MLListening(
            basic_pitch_path=ICASSP_2022_MODEL_PATH,
            midi_bus="IAC Driver ML_listening",
            channels=1,
            sample_rate=22050,
            block_seconds=1.0,
            chord_seconds=0.0,
            repeat_same_chord=False,
            midi_offset=60
            )
    # Start transcription in a background thread
    import threading
    threading.Thread(target=app.start_transcription, daemon=True).start()

    gradio_app = GradioInterface(app)
    gradio_app.create_interface().launch()