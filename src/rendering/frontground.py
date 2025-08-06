import pygame

class Code_window:
    """
    Renders a text input window for code editing.
    """
    def __init__(
        self, 
        screen,  
        size, 
        pos=(0, 0), 
        base_color=(0, 1, 0)
    ):
        self.screen = screen
        screen_size = screen.get_size()
        self.percentage_size = (size[0] / 100, size[1] / 100)
        self.size = (screen_size[0] * self.percentage_size[0], screen_size[1] * self.percentage_size[1])
        self.percentage_pos = (pos[0] / 100, pos[1] / 100)
        self.pos = (screen_size[0] * self.percentage_pos[0], screen_size[1] * self.percentage_pos[1])
        self.base_color = base_color

        self.text_lines = [""]           # List of text lines
        self.cursor_pos = [0, 0]         # [line, column]
        self.active = True

        self._reinit()

        self.padding = 8                 # Padding inside window

    def _reinit(self):
        self.screen_size = self.screen.get_size()
        self.char_size = max(self.screen_size[0] // 60, 1)
        self.font = pygame.font.SysFont("consolas", int(self.char_size * 1.5))
        self.bg_color = self._color(10)  # Background color
        self.text_color = self._color(50)
        self.caret_color = self._color(80)
        screen_size = self.screen.get_size()
        self.size = (screen_size[0] * self.percentage_size[0], screen_size[1] * self.percentage_size[1])
        self.pos = (screen_size[0] * self.percentage_pos[0], screen_size[1] * self.percentage_pos[1])

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
            return tuple(int(b + (255 - b) * factor) for b in base)

    def handle_event(self, event):
        if not self.active:
            return

        if event.type == pygame.KEYDOWN:
            line, col = self.cursor_pos

            # Enter: new line
            if event.key == pygame.K_RETURN:
                self.text_lines.insert(line + 1, "")
                self.cursor_pos = [line + 1, 0]

            # Backspace: delete character or merge lines
            elif event.key == pygame.K_BACKSPACE:
                if col > 0:
                    self.text_lines[line] = (
                        self.text_lines[line][:col - 1] +
                        self.text_lines[line][col:]
                    )
                    self.cursor_pos[1] -= 1
                elif line > 0:
                    prev_len = len(self.text_lines[line - 1])
                    self.text_lines[line - 1] += self.text_lines[line]
                    del self.text_lines[line]
                    self.cursor_pos = [line - 1, prev_len]

            # Tab: insert spaces
            elif event.key == pygame.K_TAB:
                self.text_lines[line] = (
                    self.text_lines[line][:col] +
                    "    " +
                    self.text_lines[line][col:]
                )
                self.cursor_pos[1] += 4

            # Arrow keys: move cursor
            elif event.key == pygame.K_LEFT:
                if col > 0:
                    self.cursor_pos[1] -= 1
                elif line > 0:
                    self.cursor_pos[0] -= 1
                    self.cursor_pos[1] = len(self.text_lines[self.cursor_pos[0]])

            elif event.key == pygame.K_RIGHT:
                if col < len(self.text_lines[line]):
                    self.cursor_pos[1] += 1
                elif line < len(self.text_lines) - 1:
                    self.cursor_pos[0] += 1
                    self.cursor_pos[1] = 0

            elif event.key == pygame.K_UP:
                if line > 0:
                    self.cursor_pos[0] -= 1
                    self.cursor_pos[1] = min(
                        self.cursor_pos[1], 
                        len(self.text_lines[self.cursor_pos[0]])
                    )

            elif event.key == pygame.K_DOWN:
                if line < len(self.text_lines) - 1:
                    self.cursor_pos[0] += 1
                    self.cursor_pos[1] = min(
                        self.cursor_pos[1], 
                        len(self.text_lines[self.cursor_pos[0]])
                    )
            
            #insert character
            elif event.unicode and len(event.unicode) == 1:
                self.text_lines[line] = (
                    self.text_lines[line][:col] +
                    event.unicode +
                    self.text_lines[line][col:]
                )
                self.cursor_pos[1] += 1

    def render(self):
        # Draw background
        pygame.draw.rect(
            self.screen, 
            self.bg_color,
            (*self.pos, *self.size)
        )
        # Draw outline
        outline_rect = pygame.Rect(
            self.pos[0], self.pos[1], self.size[0], self.size[1]
        )
        pygame.draw.rect(
            self.screen,
            self._color(50),
            outline_rect,
            2  # thickness
        )

        # Draw text lines
        x = self.pos[0] + self.padding
        y = self.pos[1] + self.padding
        line_height = self.font.get_height()

        for i, line in enumerate(self.text_lines):
            text_surface = self.font.render(line, True, self.text_color)
            self.screen.blit(text_surface, (x, y + i * line_height))

        # Draw caret
        line, col = self.cursor_pos
        caret_x = x + self.font.size(self.text_lines[line][:col])[0]
        caret_y = y + line * line_height
        pygame.draw.line(
            self.screen, 
            self.caret_color,
            (caret_x, caret_y),
            (caret_x, caret_y + line_height), 
            2
        )
    
    def return_text(self):
        """
        Return the text content of the window.
        """
        return "\n".join(self.text_lines)

class Text_output_window:

    def __init__(self, screen, size, pos=(0, 0), base_color=(0, 1, 0)):
        self.screen = screen
        self.percentage_size = (size[0] / 100, size[1] / 100)
        self.percentage_pos = (pos[0] / 100, pos[1] / 100)
        self.base_color = base_color
        self._reinit()
    
    def _reinit(self):
        self.screen_size = self.screen.get_size()
        self.char_size = max(self.screen_size[0] // 60, 1)
        self.font = pygame.font.SysFont("consolas", int(self.char_size * 1.5))
        self.size = (self.screen_size[0] * self.percentage_size[0], self.screen_size[1] * self.percentage_size[1])
        self.pos = (self.screen_size[0] * self.percentage_pos[0], self.screen_size[1] * self.percentage_pos[1])
    
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
            return tuple(int(b + (255 - b) * factor) for b in base)
    
    def render(self, text):
        # Draw background
        pygame.draw.rect(
            self.screen, 
            self._color(10),
            (*self.pos, *self.size)
        )
        # Draw outline
        outline_rect = pygame.Rect(
            self.pos[0], self.pos[1], self.size[0], self.size[1]
        )
        pygame.draw.rect(
            self.screen,
            self._color(50),
            outline_rect,
            2  # thickness
        )

        # Draw text
        x = self.pos[0] + 8
        y = self.pos[1] + 8
        line_height = self.font.get_height()
        
        for i, line in enumerate(text.splitlines()):
            text_surface = self.font.render(line, True, self._color(50))
            self.screen.blit(text_surface, (x, y + i * line_height))

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
    pygame.display.set_caption("TextWindow Demo")
    #text_window = Code_window(screen, (60, 60), pos=(20, 20))
    text_output = Text_output_window(screen, (30, 30), pos=(20, 20))

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                #text_window._reinit()
                text_output._reinit()
            #else:
                #text_window.handle_event(event)

        screen.fill((30, 30, 30))
        #text_window.render()
        text_output.render("idk tvoje mama smrdi\nna hovno")
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()