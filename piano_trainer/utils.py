import pygame.midi


BLACK_KEYS = {1, 3, 6, 8, 10}


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
        return pygame.midi.midi_to_ansi_note(midi_note_idx)[:-1]
