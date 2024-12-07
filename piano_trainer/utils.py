import appdirs
from pathlib import Path

import pygame.midi

BLACK_KEYS = {1, 3, 6, 8, 10}
ENHARMONICS = {
    "C#": "Db",
    "D#": "Eb",
    "F#": "Gb",
    "G#": "Ab",
    "A#": "Bb",
}


def is_black_note(midi_note_idx):
    return (midi_note_idx % 12) in BLACK_KEYS


def velocity_to_color(velocity):
    return (191 + (velocity / 127) * 64, 0, 0)


def get_white_keys_count(midi_idxs):
    count = 0
    for midi_idx in midi_idxs:
        if not is_black_note(midi_idx):
            count += 1
    return count


def get_chord_notes_names(root_note_idx, chord_quality):
    return [get_note_name(root_note_idx + delta) for delta in chord_quality]


def get_note_name(midi_note_idx, include_octave=False):
    if include_octave:
        return pygame.midi.midi_to_ansi_note(midi_note_idx)
    else:
        note = pygame.midi.midi_to_ansi_note(midi_note_idx)[:-1]
        if "-" in note:
            raise RuntimeError("Not implemented, negative octaves must be handled here")
        return note


def sharp_to_flat(note_name):
    return ENHARMONICS[note_name]


def get_app_data_dir():
    path = Path(appdirs.user_data_dir("piano_trainer", "zodiac"))
    path.mkdir(parents=True, exist_ok=True)
    return path
