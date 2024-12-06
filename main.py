import pygame

from gui import GUI
from keyboard import Keyboard

FPS = 60
KEYBOARD_KEY_COUNT = 44
FIRST_KEY_MIDI_IDX = 41


def main():
    gui = GUI(KEYBOARD_KEY_COUNT, FIRST_KEY_MIDI_IDX)
    keyboard = Keyboard()

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keyboard.update_notes_data()
        gui.draw_keyboard(keyboard.notes_data)
        clock.tick(FPS)

    keyboard.close()
    pygame.quit()


if __name__ == "__main__":
    main()
