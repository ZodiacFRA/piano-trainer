import argparse
import pygame

import utils
import game_modes
from gui import GUI
from keyboard import Keyboard


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run the game with customizable settings."
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=120,
        help="Frames per second for the game (default: 120)",
    )
    parser.add_argument(
        "-c",
        "--keyboard-key-count",
        type=int,
        default=44,
        help="Number of keys on the keyboard (default: 44)",
    )
    parser.add_argument(
        "-i",
        "--first-key-midi-idx",
        type=int,
        default=41,  # F
        help="MIDI index of the first key on the keyboard (default: 41)",
    )
    parser.add_argument(
        "--plot",
        type=bool,
        default=False,
        help="Whether or not you want to plot the test results at the end",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    if args.keyboard_key_count + args.first_key_midi_idx > 128:
        raise RuntimeError(
            "Invalid key count - first midi note combination: "
            + f"The highest requested note does not exist in MIDI ({args.keyboard_key_count + args.first_key_midi_idx})"
        )
    gui = GUI(args.keyboard_key_count, args.first_key_midi_idx)
    keyboard = Keyboard(3)
    game_mode = game_modes.PlayChord(
        results_dirpath=utils.get_app_data_dir(), show_plot=args.plot
    )

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        keyboard.update_notes_data()

        gui_settings = game_mode.do_turn(pygame.time.get_ticks(), keyboard.notes_data)
        gui.draw(keyboard.notes_data, gui_settings)
        clock.tick(args.fps)

    keyboard.close()
    pygame.quit()


if __name__ == "__main__":
    main()
