import pygame

class Code_window:
    """
    Renders a text input window for code editing with language switching.
    """
    def __init__(
        self, 
        screen,  
        size, 
        pos=(0, 0), 
        base_color=(0, 1, 0),
        active=True
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
        self.active = active
        self.highlighted_line = None
        self.language = "assembly"       # Current language: "assembly" or "piquang"
        self._reinit()

        self.padding = 8                 # Padding inside window

    def _reinit(self):
        self.screen_size = self.screen.get_size()
        self.char_size = max(self.screen_size[0] // 130, 1)
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if (self.pos[0] <= mouse_x <= self.pos[0] + self.size[0] and
                self.pos[1] <= mouse_y <= self.pos[1] + self.size[1]):
                self.active = True
            else:
                self.active = False
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

        # Draw text lines, with highlighted line
        x = self.pos[0] + self.padding
        y = self.pos[1] + self.padding
        line_height = self.font.get_height()

        for i, line in enumerate(self.text_lines):
            if i == self.highlighted_line:
                text_surface = self.font.render(line, True, self._color(20))
                pygame.draw.rect(
                    self.screen,
                    self._color(70),
                    (x - 3, y + i * line_height, self.size[0] - 3, line_height)
                )
            else:
                text_surface = self.font.render(line, True, self.text_color)
            self.screen.blit(text_surface, (x, y + i * line_height))

        # Draw caret
        line, col = self.cursor_pos
        caret_x = x + self.font.size(self.text_lines[line][:col])[0]
        caret_y = y + line * line_height
        if self.highlighted_line == line:
            pygame.draw.line(
                self.screen,
                self._color(20),
                (caret_x, caret_y),
                (caret_x, caret_y + line_height), 
                2
            )
        else:
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
    
    def recive_text(self, text, erase=True):
        if erase:
            self.text_lines = text
            self.cursor_pos = [0, 0]
        else:
            self.text_lines.append(text)
            self.text_lines.append("")  
            self.cursor_pos[1] = len(self.text_lines[0])
    
    def highlight_line(self, line):
        self.highlighted_line = line
    
    def get_language(self):
        """Get current language"""
        return self.language
    
    def set_language(self, language):
        """Set current language"""
        if language in ["assembly", "piquang"]:
            self.language = language

class Console:
    """
    A console window for input/output with cursor at the end.
    """
    def __init__(self, screen, size, pos=(0, 0), base_color=(0, 1, 0)):
        self.screen = screen
        self.percentage_size = (size[0] / 100, size[1] / 100)
        self.percentage_pos = (pos[0] / 100, pos[1] / 100)
        self.base_color = base_color
        self.output_lines = []
        self.input_buffer = ""
        self.waiting_for_input = False
        self.input_prompt = "in: "
        self.output_prefix = "out: "
        self.scroll_offset = 0  # Track how many lines to scroll up
        self.max_visible_lines = 15  # Maximum lines visible at once
        self._reinit()
    
    def _reinit(self):
        self.screen_size = self.screen.get_size()
        self.char_size = max(self.screen_size[0] // 130, 1)
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
    
    def add_output(self, text):
        """
        Add output text with 'out:' prefix.
        """
        # Remove the "OUT: " prefix if it's already in the text
        if text.startswith("OUT: "):
            text = text[5:]  # Remove "OUT: " prefix
        
        self.output_lines.append(f"{self.output_prefix}{text}")
        # Keep only last 20 lines to prevent overflow
        if len(self.output_lines) > 20:
            self.output_lines = self.output_lines[-20:]
    
    def clear_console(self):
        """
        Clear all output lines and reset input buffer.
        """
        self.output_lines = []
        self.input_buffer = ""
        self.waiting_for_input = False
    
    def request_input(self):
        """
        Request input from user. Returns True if input is ready.
        """
        self.waiting_for_input = True
        return False
    
    def get_input(self):
        """
        Get the current input buffer and clear it.
        """
        if self.input_buffer:
            input_value = self.input_buffer
            self.input_buffer = ""
            self.waiting_for_input = False
            return input_value
        return None
    
    def is_waiting_for_input(self):
        """
        Check if console is waiting for input.
        """
        return self.waiting_for_input
    
    def handle_event(self, event):
        """
        Handle keyboard events for input.
        """
        if not self.waiting_for_input:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Input complete - add the input to output lines
                if self.input_buffer:
                    self.output_lines.append(f"{self.input_prompt}{self.input_buffer}")
                self.waiting_for_input = False
                return True
            elif event.key == pygame.K_BACKSPACE:
                if self.input_buffer:
                    self.input_buffer = self.input_buffer[:-1]
            elif event.unicode and event.unicode.isprintable():
                self.input_buffer += event.unicode
        return False
    
    def render(self):
        """
        Render the console with output and input.
        """
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
        line_height = self.font.get_height() + 2
        
        # Draw output lines
        for line in self.output_lines:
            text_surface = self.font.render(line, True, self._color(50))
            self.screen.blit(text_surface, (x, y))
            y += line_height
        
        # Draw input line with cursor only when waiting for input
        if self.waiting_for_input:
            input_line = f"{self.input_prompt}{self.input_buffer}"
            # Add blinking cursor
            import time
            if int(time.time() * 2) % 2:  # Blink every 0.5 seconds
                input_line += "|"
            
            text_surface = self.font.render(input_line, True, self._color(50))
            self.screen.blit(text_surface, (x, y))


class RegisterWindow:
    

    def __init__(self, screen, size, pos=(0, 0), base_color=(0, 1, 0)):
        self.screen = screen
        self.percentage_size = (size[0] / 100, size[1] / 100)
        self.percentage_pos = (pos[0] / 100, pos[1] / 100)
        self.base_color = base_color
        self._reinit()
    
    def _reinit(self):
        self.screen_size = self.screen.get_size()
        self.char_size = max(self.screen_size[0] // 130, 1)
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
    
    def render(self, text=""):
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
        
        text_surface = self.font.render(str(text), True, self._color(50))
        self.screen.blit(text_surface, (x, y))

class LanguageToggleButton:
    """
    A button for switching between assembly and Piquang languages.
    """
    def __init__(self, screen, size, pos=(0, 0), base_color=(0, 1, 0)):
        self.screen = screen
        self.percentage_size = (size[0] / 100, size[1] / 100)
        self.percentage_pos = (pos[0] / 100, pos[1] / 100)
        self.base_color = base_color
        self.language = "assembly"  # Current language
        self._reinit()
    
    def _reinit(self):
        self.screen_size = self.screen.get_size()
        self.size = (self.screen_size[0] * self.percentage_size[0], self.screen_size[1] * self.percentage_size[1])
        self.pos = (self.screen_size[0] * self.percentage_pos[0], self.screen_size[1] * self.percentage_pos[1])
        self.char_size = max(self.screen_size[0] // 130, 1)
        self.font = pygame.font.SysFont("consolas", int(self.char_size * 1.2))
    
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
    
    def toggle_language(self):
        """Toggle between assembly and Piquang"""
        if self.language == "assembly":
            self.language = "piquang"
        else:
            self.language = "assembly"
        return self.language
    
    def get_language(self):
        """Get current language"""
        return self.language
    
    def render(self):
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
        
        # Draw language text
        text = f"Lang: {self.language.upper()}"
        text_surface = self.font.render(text, True, self._color(50))
        text_rect = text_surface.get_rect(center=(self.pos[0] + self.size[0] // 2, 
                                                  self.pos[1] + self.size[1] // 2))
        self.screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if (self.pos[0] <= mouse_x <= self.pos[0] + self.size[0] and
                self.pos[1] <= mouse_y <= self.pos[1] + self.size[1]):
                return self.toggle_language()  # Return the new language
        return None  # No language change

class Button:
    """
    A simple button class for rendering buttons.
    """
    def __init__(self, screen, size, pos=(0, 0), base_color=(0, 1, 0), symbol=""):
        self.screen = screen
        self.percentage_size = (size[0] / 100, size[1] / 100)
        self.percentage_pos = (pos[0] / 100, pos[1] / 100)
        self.base_color = base_color
        self.symbol = symbol
        self._reinit()
    
    def _reinit(self):
        self.screen_size = self.screen.get_size()
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
    
    def _draw_symbol(self):
        """
        Draw the button symbol if it exists.
        """
        if self.symbol:
            if self.symbol == "RUN":
                pygame.draw.polygon(self.screen, self._color(50), [
                    (self.pos[0] + self.size[0] / 4, self.pos[1] + self.size[1] / 4),
                    (self.pos[0] + self.size[0] / 4 * 3, self.pos[1] + self.size[1] / 2),
                    (self.pos[0] + self.size[0] / 4, self.pos[1] + self.size[1] / 4 * 3)
                ])
            elif self.symbol == "STOP":
                pygame.draw.rect(self.screen, self._color(50), (
                    self.pos[0] + self.size[0] / 4,
                    self.pos[1] + self.size[1] / 4,
                    self.size[0] / 2,
                    self.size[1] / 2
                ))
            elif self.symbol == "STEP":
                pygame.draw.polygon(self.screen, self._color(50), [
                    (self.pos[0] + self.size[0] / 4, self.pos[1] + self.size[1] / 4),
                    (self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 4),
                    (self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2),
                    (self.pos[0] + self.size[0] / 4 * 3, self.pos[1] + self.size[1] / 2),
                    (self.pos[0] + self.size[0] / 4 * 3, self.pos[1] + self.size[1] / 4 * 3),
                    (self.pos[0] + self.size[0] / 4, self.pos[1] + self.size[1] / 4 * 3)
                ])
            elif self.symbol == "CLEAR":
                # Draw an X symbol for clear
                pygame.draw.line(self.screen, self._color(50), 
                    (self.pos[0] + self.size[0] / 4, self.pos[1] + self.size[1] / 4),
                    (self.pos[0] + self.size[0] * 3 / 4, self.pos[1] + self.size[1] * 3 / 4), 3)
                pygame.draw.line(self.screen, self._color(50), 
                    (self.pos[0] + self.size[0] * 3 / 4, self.pos[1] + self.size[1] / 4),
                    (self.pos[0] + self.size[0] / 4, self.pos[1] + self.size[1] * 3 / 4), 3)

    def render(self):
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
        self._draw_symbol()
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if (self.pos[0] <= mouse_x <= self.pos[0] + self.size[0] and
                self.pos[1] <= mouse_y <= self.pos[1] + self.size[1]):
                return True  # Button clicked
        return False  # Button not clicked

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
    pygame.display.set_caption("TextWindow Demo")
    #text_window = Code_window(screen, (60, 60), pos=(20, 20))
    text_output = RegisterWindow(screen, (30, 30), pos=(20, 20))
    button = Button(screen, (20, 10), pos=(70, 70), base_color=(0, 1, 0), symbol="STEP")
    button2 = Button(screen, (20, 10), pos=(70, 90), base_color=(0, 1, 0), symbol="RUN")
    button3 = Button(screen, (20, 10), pos=(50, 70), base_color=(0, 1, 0), symbol="STOP")

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if button.handle_event(event):
                print("Step button clicked")
            if button2.handle_event(event):
                print("Run button clicked")
            if button3.handle_event(event):
                print("Stop button clicked")
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                #text_window._reinit()
                text_output._reinit()
                button._reinit()
                button2._reinit()
                button3._reinit()
            #else:
                #text_window.handle_event(event)

        screen.fill((30, 30, 30))
        #text_window.render()
        button.render()
        button2.render()
        button3.render()
        text_output.render("idk")
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()