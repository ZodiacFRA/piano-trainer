import pygame.midi


class Keyboard:
    """
    MIDI event: [[status byte, note midi idx, velocity], timestamp]

    Status Bytes:
    144 (0x90)	Note On	A note is being played.
    128 (0x80)	Note Off	A note is being released.
    176 (0xB0)	Control Change	A controller value has changed (e.g., volume, pan).
    248 (0xF8)	Timing Clock	Sent 24 times per quarter note for tempo sync.
    255 (0xFF)	System Reset
    """

    def __init__(self, midi_input_idx=None):
        pygame.midi.init()

        if midi_input_idx is None:
            # If no midi_input_idx provided, print available devices, and use the default one
            input_count = pygame.midi.get_count()
            print(f"Available MIDI Input Devices: {input_count}")
            for i in range(input_count):
                device_info = pygame.midi.get_device_info(i)
                # if device_info[2] == 1:  # Input device
                print(f"ID {i}: {device_info[1].decode('utf-8')}")
            midi_input_idx = pygame.midi.get_default_input_id()

        self.midi_input = pygame.midi.Input(midi_input_idx)

        # Initialize notes buffer (128 for full midi range)
        self.notes_data = [0] * 128

    def update_notes_data(self):
        while self.midi_input.poll():
            midi_events = self.midi_input.read(1)
            for event in midi_events:
                midi_event = event[0]
                # [[status byte, note midi idx, velocity], timestamp]
                status_byte = midi_event[0]
                velocity = -1
                if status_byte == 128:  # Note Off
                    velocity = 0
                elif status_byte == 144:
                    velocity = midi_event[2]  # Velocity (volume)
                if velocity >= 0:
                    note_idx = midi_event[1]
                    self.notes_data[note_idx] = velocity

    def close(self):
        self.midi_input.close()
        pygame.midi.quit()