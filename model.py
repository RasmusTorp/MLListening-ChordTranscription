import sounddevice as sd
import numpy as np
import threading
import queue
import time
import tempfile
import soundfile as sf
from basic_pitch.inference import predict, Model
from basic_pitch import ICASSP_2022_MODEL_PATH
import mido
from mido import Message
from pychord import find_chords_from_notes

class MLListening:
    def __init__(self, basic_pitch_path, midi_bus, 
                channels=1, 
                sample_rate=22050, 
                block_seconds=1.0, 
                repeat_same_chords=False, 
                midi_offset=60,
                minimum_velocity=40):
        
        self.midi_bus = midi_bus
        self.channels = channels
        self.sample_rate = sample_rate
        self.block_seconds = block_seconds
        
        self.repeat_same_chords = repeat_same_chords  # Flag to control chord repetition
        self.midi_offset = midi_offset  # MIDI note offset for middle C (C4)
        
        self.block_size = int(sample_rate * block_seconds)
        self.current_chord = None  # Store the current chord
        
        self.note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        self.midi_port = mido.open_output(midi_bus)  # Your IAC virtual port name
        self.audio_queue = queue.Queue()
        self.basic_pitch_model = Model(basic_pitch_path)
        
        self.currently_playing_midi = set()  # Track currently playing MIDI notes
        self.minimum_velocity = minimum_velocity  # Minimum velocity for MIDI notes
        
    def start_transcription(self):
        threading.Thread(target=self.transcription_loop, daemon=True).start()
        
        print("Starting transcription loop")
        with sd.InputStream(callback=self.audio_callback, channels=self.channels, samplerate=self.sample_rate, blocksize=self.block_size):
            print("Listening... Press Ctrl+C to exit")
            while True:
                time.sleep(0.1)

    def transcription_loop(self):
        print("Basic Pitch inference thread started")
        while True:
            audio_chunk = self.audio_queue.get()
            with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
                sf.write(tmp.name, audio_chunk, self.sample_rate)
                output, midi_data, note_events = predict(tmp.name, self.basic_pitch_model)
                '''
                    note_events: List[Tuple[float, float, int, float, Optional[List[int]]]],
            
                    Args:
                        note_events: A list of note event tuples to save. Tuples have the format
                            ("start_time_s", "end_time_s", "pitch_midi", "velocity", "list of pitch bend values")
                '''
            
            pitches = sorted(set([int(note[2]) for note in note_events]))
            
            note_names = sorted(set([self.note_number_to_name(p) for p in pitches]))
            velocities = sorted(set([self.velocity_float_to_int_repr(note[3]) for note in note_events]))
            
            if note_names:
                chords = find_chords_from_notes(note_names)
                if chords:
                    detected_chord = chords[0].chord
                    
                    if self.current_chord == detected_chord and not self.repeat_same_chords:
                        continue
                    
                    self.current_velocity = max(int(np.mean(np.array(velocities))), self.minimum_velocity) if velocities else 80
                    self.current_chord = detected_chord
                    print(f"Detected chord: {detected_chord}, velocity: {self.current_velocity}")
                    
                    chord_components = chords[0].components()
                    
                    midi_notes = [self.note_name_to_number(note) for note in chord_components]
                    
                    if not midi_notes:
                        continue

                    self.send_midi_pad(midi_notes)
                    
    ### Helper methods ###

    def audio_callback(self, indata, frames, time_info, status):
        audio = indata[:, 0]
        self.audio_queue.put(audio.copy())
        
    def velocity_float_to_int_repr(self, velocity_float):
        return int(velocity_float * 127)                    
                    
    def send_midi_pad(self, midi_notes):
        
        # Stops currently playing MIDI notes
        for note in self.currently_playing_midi:
            if note is None:
                continue
            if note < 0 or note > 127:
                continue
            
            self.midi_port.send(Message('note_off', note=note, velocity=self.current_velocity))
        
        self.currently_playing_midi = set(midi_notes)  # Update currently playing notes
        
        for note in midi_notes:
            if note is None:
                continue
            if note < 0 or note > 127:
                continue
            
            self.midi_port.send(Message('note_on', note=note))
            
    def note_number_to_name(self, midi_number):
        return self.note_names[midi_number % 12]
    
    def note_name_to_number(self, note_name):
        # dictionary to map note names to MIDI numbers
        note_name = self.normalize_note_names([note_name])[0]  # Normalize input
        note_to_number = {name: i for i, name in enumerate(self.note_names)}
        return note_to_number.get(note_name, None) + self.midi_offset
            
    
    def normalize_note_names(self, notes):
        # Map flats to sharps for MIDI lookup
        flat_to_sharp = {
            "Db": "C#",
            "Eb": "D#",
            "Gb": "F#",
            "Ab": "G#",
            "Bb": "A#"
        }
        return [flat_to_sharp.get(note, note) for note in notes]                    

if __name__ == "__main__":
    
    app = MLListening(
                    basic_pitch_path=ICASSP_2022_MODEL_PATH,
                    midi_bus="IAC Driver ML_listening",
                    channels=1,
                    sample_rate=22050,
                    block_seconds=1.0,
                    chord_seconds=0.0,
                    repeat_same_chord=False
                    )
    
    chords = [[60, 64, 67], [62, 65, 69], [64, 67, 71]]  # Example chords in MIDI note numbers
    
    # i = 0
    # while True:
        
    #     i += 1
    #     if i == len(chords):
    #         i = 0
            
    #     app.send_midi_pad(chords[i])  # Send C4, E4, G4 as an example chord
    #     time.sleep(4)
    #     print("Sending MIDI messages...")
    
    app.start_transcription()
