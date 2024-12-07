import pygame

import utils

SCALE = 2
# Shapes
WHITE_KEY_WIDTH = 25 * SCALE
WHITE_KEY_HEIGHT = 150 * SCALE
BLACK_KEY_WIDTH = 15 * SCALE
BLACK_KEY_HEIGHT = 90 * SCALE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class GUI:
    def __init__(self, notes_count=44, first_key_midi_idx=41):
        self.notes_count = notes_count
        self.first_key_midi_idx = first_key_midi_idx
        self.last_key_midi_idx = self.first_key_midi_idx + self.notes_count

        self.KEYBOARD_WIDTH = WHITE_KEY_WIDTH * utils.get_white_keys_count(
            list(range(self.first_key_midi_idx, self.last_key_midi_idx))
        )

        self.PADDING = 2 * WHITE_KEY_WIDTH
        self.WINDOWS_WIDTH = self.KEYBOARD_WIDTH + 2 * self.PADDING
        self.WINDOW_HEIGHT = WHITE_KEY_HEIGHT + 2 * self.PADDING

        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOWS_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Keyboard")
        self.font = pygame.font.Font(None, 100)

    def draw_white_key(self, key_position_idx, velocity):
        color = utils.velocity_to_color(velocity) if velocity > 0 else WHITE
        x = self.PADDING + (key_position_idx * WHITE_KEY_WIDTH)
        pygame.draw.rect(
            self.screen,
            color,
            (x, self.PADDING, WHITE_KEY_WIDTH - 1, WHITE_KEY_HEIGHT),
        )
        pygame.draw.rect(
            self.screen,
            (0, 0, 0),
            (x, self.PADDING, WHITE_KEY_WIDTH - 1, WHITE_KEY_HEIGHT),
            1,
        )

    def draw_black_key(self, key_position_idx, velocity):
        color = utils.velocity_to_color(velocity) if velocity > 0 else BLACK
        x = self.PADDING + (key_position_idx * WHITE_KEY_WIDTH) - BLACK_KEY_WIDTH // 2
        pygame.draw.rect(
            self.screen,
            color,
            (x, self.PADDING, BLACK_KEY_WIDTH, BLACK_KEY_HEIGHT),
        )
        if velocity > 0:
            pygame.draw.rect(
                self.screen,
                BLACK,
                (x, self.PADDING, BLACK_KEY_WIDTH, BLACK_KEY_HEIGHT),
                1,
            )

    def draw_keyboard(self, notes_data):
        """Draw all the keys. Looping twice as we need to draw black keys last"""
        key_position_idx = 0
        for midi_note_idx in range(self.first_key_midi_idx, self.last_key_midi_idx):
            if not utils.is_black_note(midi_note_idx):
                self.draw_white_key(key_position_idx, notes_data[midi_note_idx])
                key_position_idx += 1

        key_position_idx = 0
        for midi_note_idx in range(self.first_key_midi_idx, self.last_key_midi_idx):
            if not utils.is_black_note(midi_note_idx):
                # We place black keys relative to the white ones, so only count the white ones
                key_position_idx += 1
            else:
                self.draw_black_key(key_position_idx, notes_data[midi_note_idx])

    def draw_text(self, text):
        text_surface = self.font.render(text, True, BLACK)
        self.screen.blit(text_surface, (int(self.WINDOWS_WIDTH / 2.5), 20))

    def draw(self, notes_data, gui_settings):
        color = gui_settings.get("background_color", WHITE)
        if "sound" in gui_settings:
            self.play_sound(gui_settings["sound"])
        self.screen.fill(color)
        self.draw_keyboard(notes_data)
        self.draw_text(gui_settings["text"])
        pygame.display.flip()

    def play_sound(self, filepath, volume=1.0):
        pygame.mixer.init()
        sound = pygame.mixer.Sound(filepath)
        sound.set_volume(volume)
        sound.play()
