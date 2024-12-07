import time
import random

import statistics
from collections import defaultdict

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
        self.choose_new_chord(0)
        self.results = {}

    def __del__(self):
        if not self.results:
            return
        self.print_results()
        with open("./playchord_results.txt", "a+", encoding="utf-8") as f:
            epoch_time = int(time.time())  # Get current epoch time as integer
            f.write(f"{epoch_time}\n")  # Write epoch time to the file
            for chord, time_to_find in self.results.items():
                f.write(f"{chord}\t{time_to_find}\n")

    def print_results(self):
        avg_time_to_find = (sum(self.results.values()) / len(self.results)) / 1000
        print(f"==== Global mean find time: {avg_time_to_find:.2f}s")
        root_mean_times, chord_quality_mean_times = self.compute_mean_times()
        print("==== Root keys average times")
        for k, v in root_mean_times.items():
            print(f"{k}:\t{(v/1000):.2f}s")
        print("==== Chord qualities average times")
        for k, v in chord_quality_mean_times.items():
            if not k:
                k = "M"
            print(f"{k}:\t{(v/1000):.2f}s")

    def compute_mean_times(self):
        root_times = defaultdict(list)
        chord_quality_times = defaultdict(list)
        for (first_key, second_key), time_value in self.results.items():
            root_times[first_key].append(time_value)
            chord_quality_times[second_key].append(time_value)
        root_mean_times = {
            root: statistics.mean(times) for root, times in root_times.items()
        }
        root_mean_times = dict(
            sorted(root_mean_times.items(), key=lambda item: item[1], reverse=True)
        )
        chord_quality_mean_times = {
            chord_quality: statistics.mean(times)
            for chord_quality, times in chord_quality_times.items()
        }
        chord_quality_mean_times = dict(
            sorted(
                chord_quality_mean_times.items(), key=lambda item: item[1], reverse=True
            )
        )
        return root_mean_times, chord_quality_mean_times

    def choose_new_chord(self, tick):
        self.start_timer = tick

        root_note_idx = random.randint(60, 71)
        chord_quality = random.choice(list(music.CHORDS.items()))
        self.target_chord_notes = set(
            utils.get_chord_notes_names(root_note_idx, chord_quality[1])
        )
        self.target_chord_text = (utils.get_note_name(root_note_idx), chord_quality[0])

    def get_text(self):
        res = self.target_chord_text[0] + self.target_chord_text[1]
        if len(self.results) > 0:
            avg_time_to_find = (sum(self.results.values()) / len(self.results)) / 1000
            res += f"{' '*10}{avg_time_to_find:.2f}"
        return res

    def do_turn(self, tick, notes_data):
        played_notes_idxs = [
            index for index, value in enumerate(notes_data) if value > 0
        ]
        played_notes = set(
            [utils.get_note_name(note_idx) for note_idx in played_notes_idxs]
        )
        if self.target_chord_notes == played_notes:
            # User played the correct chord
            time_to_find = tick - self.start_timer
            self.results[self.target_chord_text] = time_to_find
            self.choose_new_chord(tick)
            return {
                "text": self.get_text(),
                "background_color": (0, 255, 0),
                "sound": "piano_trainer/data/sounds/success.wav",
            }
        elif len(self.target_chord_notes) == len(played_notes):
            # print("failed:", tick, played_notes, self.target_chord_notes)
            return {
                "text": self.get_text(),
                "sound": "piano_trainer/data/sounds/fail.wav",
            }
        return {
            "text": self.get_text(),
        }
