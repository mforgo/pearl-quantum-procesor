import pygame
from random import randint
from src.rendering import frontground

# === CONFIGURATION ===
CHAR_COLUMNS = 80         # Number of columns of characters
FPS = 20                  # Frames per second
FONT_SCALE = 1.5          # Font size multiplier
COLUMN_LENGTH_FACTOR = 0.5  # Fraction of screen height for column length

class Background:
    def __init__(self, screen, base_color=(0, 1, 0)):
        """
        Initialize the background effect.

        Args:
            screen: Pygame surface to draw on.
            base_color: Tuple of RGB values (0-1) for the base color.
        """
        self.screen = screen
        self.base_color = base_color
        self.black = self._color(0)
        self.screen_size = self.screen.get_size()
        self.char_columns = CHAR_COLUMNS
        self.char_size = max(self.screen_size[0] // self.char_columns, 1)
        self.y_offset = 0
        self.font = pygame.font.SysFont(None, int(self.char_size * FONT_SCALE))
        self.color_cache = [self._color(p) for p in range(101)]
        self.char_lines = []
        self._init_char_lines()

    def _init_char_lines(self):
        """
        Initialize the starting positions for each column.
        """
        width, height = self.screen.get_size()
        self.char_size = max(width // self.char_columns, 1)
        self.char_lines = [
            [x, randint(0, int(height * (1 + COLUMN_LENGTH_FACTOR))), randint(0, int(height * COLUMN_LENGTH_FACTOR))]
            for x in range(0, width, self.char_size)
        ]

    def _color(self, percentage):
        """
        Calculate color based on percentage (0-100).
        """
        base = [int(c * 255) for c in self.base_color]
        if percentage <= 50:
            factor = percentage / 50
            return tuple(int(b * factor) for b in base)
        else:
            factor = (percentage - 50) / 50
            return tuple(
                int(b + (255 - b) * factor) for b in base
            )

    def _random_letter(self, index):
        """
        Generate a pseudo-random ASCII character based on index.
        """
        return chr(index % 94 + 33)  # ASCII 33-126

    def _render_letter(self, letter, pos, color):
        """
        Render a single letter at the given position and color.
        """
        text = self.font.render(letter, True, color)
        self.screen.blit(text, pos)

    def _draw_column(self, x, y0, length, repeat_offset):
        """
        Draw a vertical column of letters.
        """
        for i in range(length):
            y = (y0 - i * self.char_size) % (self.screen_size[1] + repeat_offset)
            letter = self._random_letter(hash((x, y)))
            color_idx = min(max(int((i / length) * -100) + 100, 0), 100)
            color = self.color_cache[color_idx]
            self._render_letter(letter, (x, y), color)

    def render(self):
        """
        Render the background effect.
        """
        # Update screen size and char size if window resized
        if self.screen_size != self.screen.get_size():
            self.screen_size = self.screen.get_size()
            self._init_char_lines()
            self.font = pygame.font.SysFont(None, int(self.char_size * FONT_SCALE))

        self.screen.fill(self.black)
        width, height = self.screen.get_size()
        self.char_size = max(width // self.char_columns, 1)
        num_columns = width // self.char_size
        length = max(int(height // self.char_size * COLUMN_LENGTH_FACTOR), 1)

        # Reinitialize char_lines if needed
        if len(self.char_lines) != num_columns:
            self._init_char_lines()

        for x, y, repeat_offset in self.char_lines:
            self._draw_column(x, self.y_offset + y, length, repeat_offset)
        self.y_offset = (self.y_offset + self.char_size)# % (self.screen_size[1] * 2)

def main():
    """
    Main loop for the background effect demo.
    """
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    bg = Background(screen)
    clock = pygame.time.Clock()

    fg = frontground.TextWindow(screen, (60, 60), pos=(20, 20))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            fg.handle_event(event)

        bg.render()
        fg.render()
        pygame.display.flip()
        clock.tick(FPS)  # Limits the loop to FPS frames per second.

    pygame.quit()

if __name__ == "__main__":
    main()