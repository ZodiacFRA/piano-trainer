import pygame

import game_modes
from gui import GUI
from keyboard import Keyboard

FPS = 120
KEYBOARD_KEY_COUNT = 44
FIRST_KEY_MIDI_IDX = 41


def main():
    gui = GUI(KEYBOARD_KEY_COUNT, FIRST_KEY_MIDI_IDX)
    keyboard = Keyboard()
    game_mode = game_modes.PlayChord()

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        keyboard.update_notes_data()

        text = game_mode.do_turn(pygame.time.get_ticks(), keyboard.notes_data)
        gui.draw(keyboard.notes_data, text)
        clock.tick(FPS)

    keyboard.close()
    pygame.quit()


if __name__ == "__main__":
    main()
