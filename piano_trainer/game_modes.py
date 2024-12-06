import random

import music
import utils

"""
modes: (measure speed and accuracy everytime)
- recognize a chord drawn on the keyboard and name it
- play the named chord
- play a scale (both hands?)
"""


class PlayChord:
    def __init__(self):
        self.choose_new_chord()

    def choose_new_chord(self):
        root_note_idx = random.randint(60, 71)
        chord_quality = random.choice(list(music.CHORDS.items()))
        target_chord_text = utils.get_note_name(root_note_idx) + chord_quality[0]
        self.target_chord_notes = set(
            utils.get_chord_notes_names(root_note_idx, chord_quality[1])
        )
        self.text = target_chord_text
        self.timer = None

    def do_turn(self, tick, notes_data):
        played_notes_idxs = [
            index for index, value in enumerate(notes_data) if value > 0
        ]
        played_notes = set(
            [utils.get_note_name(note_idx) for note_idx in played_notes_idxs]
        )
        if self.target_chord_notes == played_notes:
            self.text = "WELL DONE"
            self.timer = tick
        if self.timer is not None and tick - self.timer > 500:
            # The chord has been guessed correctly, and 2seconds elapsed
            self.choose_new_chord()
        return self.text
