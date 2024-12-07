import os
import time
import copy
import pickle
import random
import statistics
from itertools import product
from datetime import datetime
from collections import defaultdict

import matplotlib.pyplot as plt

import music
import utils


def analyze_session(session_data):
    avg_time_to_find = sum(session_data.values()) / len(session_data)
    root_mean_times, chord_quality_mean_times = compute_mean_times(session_data)
    return avg_time_to_find, root_mean_times, chord_quality_mean_times


def compute_mean_times(session_results):
    root_times = defaultdict(list)
    chord_quality_times = defaultdict(list)
    for (first_key, second_key), time_value in session_results.items():
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
        sorted(chord_quality_mean_times.items(), key=lambda item: item[1], reverse=True)
    )
    return root_mean_times, chord_quality_mean_times


def plot(global_stats):
    # Convert epoch times to human-readable dates for x-axis
    x = [
        datetime.fromtimestamp(epoch_time).strftime("%Y-%m-%d %H:%M:%S")
        for epoch_time in list(global_stats.keys())
    ]
    # Extract avg_time data
    avg_time_y = [values[0] / 1000 for values in global_stats.values()]
    # Root key subplot
    root_key_data = {key: [] for key in music.KEYS}
    for values in global_stats.values():
        root_key_dict = values[1]
        for key in music.KEYS:
            tmp = root_key_dict.get(key, None)
            if tmp is not None:
                tmp /= 1000
            root_key_data[key].append(tmp)
    # Chord quality subplot
    chord_quality_data = {key: [] for key in music.CHORDS.keys()}
    for values in global_stats.values():
        chord_quality_dict = values[2]
        for key in music.CHORDS.keys():
            tmp = chord_quality_dict.get(key, None)
            if tmp is not None:
                tmp /= 1000
            chord_quality_data[key].append(tmp)

    _, axes = plt.subplots(3, 1, figsize=(12, 15), sharex=True)  # Share x-axis
    # Plot avg_time
    axes[0].plot(x, avg_time_y, marker="o", color="blue")
    axes[0].set_title("Average time (s)")
    axes[0].tick_params(axis="x", which="both", bottom=False, labelbottom=False)
    # Plot root_key
    for key, y_values in root_key_data.items():
        axes[1].plot(x, y_values, marker="o", label=f"{key}")
    axes[1].set_title("Root keys average time (s)")
    axes[1].legend()
    axes[1].tick_params(axis="x", which="both", bottom=False, labelbottom=False)
    # Plot chord_quality
    for key, y_values in chord_quality_data.items():
        axes[2].plot(x, y_values, marker="o", label=f"{key}")
    axes[2].set_xlabel("Session date")
    axes[2].set_title("Chord qualities average time (s)")
    axes[2].legend()

    plt.tight_layout()
    plt.show()


def analyze_and_save(results_filepath, session_results, show_plot):
    session_results = session_results
    results_filepath = results_filepath
    epoch_time = int(time.time())
    # Load every data available, return if there's none
    global_results = {}
    if os.path.isfile(results_filepath):
        with open(results_filepath, "rb") as file:
            global_results = pickle.load(file)
    if session_results:
        session_result_timestamped = {epoch_time: session_results}
        global_results.update(session_result_timestamped)
        with open(results_filepath, "wb") as file:
            pickle.dump(global_results, file)
    if not global_results:
        return
    # Analyze and plot
    global_stats = {}
    for session_timestamp, session_data in global_results.items():
        global_stats[session_timestamp] = analyze_session(session_data)
    if show_plot:
        plot(global_stats)


class PlayChord:
    def __init__(self, results_dirpath, show_plot):
        self.show_plot = show_plot
        self.results_dirpath = results_dirpath
        self.results_filepath = os.path.join(results_dirpath, "playchord.pkl")
        self.results = {}
        # To ensure a useful random repartition, construct all the possible combinations
        # and we'll pop them one by one
        root_notes_midi_idxs = list(range(60, 72))
        chord_qualities = list(music.CHORDS.items())
        self.total_available_chords = list(
            product(root_notes_midi_idxs, chord_qualities)
        )
        self.chords = copy.deepcopy(self.total_available_chords)
        random.shuffle(self.chords)
        self.choose_new_chord(0)

    def __del__(self):
        analyze_and_save(self.results_filepath, self.results, self.show_plot)

    def get_display_text(self):
        # Remove the explicit Major notation if needed
        tmp = self.target_chord_data[1]
        if tmp == "Major":
            tmp = ""
        res = self.target_chord_data[0] + tmp
        if len(self.results) > 0:
            avg_time_to_find = (sum(self.results.values()) / len(self.results)) / 1000
            res += f"{' '*10}{avg_time_to_find:.2f}"
        return res

    def choose_new_chord(self, tick):
        self.start_timer = tick
        if not self.chords:
            self.chords = copy.deepcopy(self.total_available_chords)
        root_note_idx, chord_quality = self.chords.pop()
        # Here, if possible, we want to randomly chose between enharmonic notes.
        # The name string is not used for the program logic, only display and logging
        # which is perfect as we want the stats to differentiate between enharmonic notes.
        # The program logic only operates on sharps,
        # as this is what pygame.midi.midi_to_ansi_note() returns
        root_note_name = utils.get_note_name(root_note_idx)
        if "#" in root_note_name and random.randint(0, 1):
            root_note_name = utils.sharp_to_flat(root_note_name)

        self.target_chord_notes = set(
            utils.get_chord_notes_names(root_note_idx, chord_quality[1])
        )
        self.target_chord_data = (root_note_name, chord_quality[0])

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
            self.results[self.target_chord_data] = time_to_find
            self.choose_new_chord(tick)
            return {
                "text": self.get_display_text(),
                "background_color": (0, 255, 0),
                "sound": "piano_trainer/data/sounds/success.wav",
            }
        elif len(self.target_chord_notes) == len(played_notes):
            return {
                "text": self.get_display_text(),
                "background_color": (255, 0, 0),
                "sound": "piano_trainer/data/sounds/fail.wav",
            }
        return {
            "text": self.get_display_text(),
        }
