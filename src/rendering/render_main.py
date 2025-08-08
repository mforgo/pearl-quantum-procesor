import pygame
from src.rendering import background
from src.rendering import frontground

class RenderMain:
    def __init__(self):
        pygame.init()
        self.fullscreen = True
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.RESIZABLE)
        else:
            self.screen = pygame.display.set_mode((1000, 800), pygame.RESIZABLE)
        pygame.display.set_caption("CPU Emulator")
        self.running = True
        self.base_color = (1, 1, 1)
        self.background = background.Background(self.screen, self.base_color)
        self.code_window = frontground.Code_window(self.screen, (40.74, 52.17), pos=(7.41, 8.7), base_color=self.base_color)
        self.language_button = frontground.LanguageToggleButton(self.screen, (15, 4), pos=(7.41, 4.35), base_color=self.base_color)
        self.clear_button = frontground.Button(self.screen, (3.7, 4.35), pos=(44.44, 21.74), base_color=self.base_color, symbol="CLEAR")
        self.run_button = frontground.Button(self.screen, (3.7, 4.35), pos=(44.44, 8.7), base_color=self.base_color, symbol="RUN")
        self.step_button = frontground.Button(self.screen, (3.7, 4.35), pos=(44.44, 13.04), base_color=self.base_color, symbol="STEP")
        self.stop_button = frontground.Button(self.screen, (3.7, 4.35), pos=(44.44, 17.39), base_color=self.base_color, symbol="STOP")
        self.console_window = frontground.Console(self.screen, (40.74, 26.09), pos=(7.41, 65.22), base_color=self.base_color)
        self.register_window = [
            frontground.RegisterWindow(self.screen, (18.52, 4.35), pos=(51.85, 8.7), base_color=self.base_color),
            frontground.RegisterWindow(self.screen, (18.52, 4.35), pos=(51.85, 17.39), base_color=self.base_color),
            frontground.RegisterWindow(self.screen, (18.52, 4.35), pos=(51.85, 26.09), base_color=self.base_color),
            frontground.RegisterWindow(self.screen, (18.52, 4.35), pos=(51.85, 34.78), base_color=self.base_color),
            frontground.RegisterWindow(self.screen, (18.52, 4.35), pos=(74.07, 8.7), base_color=self.base_color),
            frontground.RegisterWindow(self.screen, (18.52, 4.35), pos=(74.07, 17.39), base_color=self.base_color),
            frontground.RegisterWindow(self.screen, (18.52, 4.35), pos=(74.07, 26.09), base_color=self.base_color),
            frontground.RegisterWindow(self.screen, (18.52, 4.35), pos=(74.07, 34.78), base_color=self.base_color),
            ]
        self.memory_window = frontground.RegisterWindow(self.screen, (40.74, 47.83), pos=(51.85, 43.48), base_color=self.base_color)
        self.clock = pygame.time.Clock()
        
        # Initialize button state variables
        self.working = False
        self.stepping = False
        self.stopping = False
        self.clearing = False

    def run(self, ram, registers):
        self.memory = ram
        self.registers = registers
        return self.__main_loop()

    def __main_loop(self):
        self.__handle_events()
        self.__render()
        return self.running

    def __render(self):
        self.background.render()
        self.language_button.render()
        self.clear_button.render()
        self.code_window.render()
        self.run_button.render()
        self.step_button.render()
        self.stop_button.render()
        self.console_window.render()
        for i in range(8):
            self.register_window[i].render(f"Reg {i}: {self.registers[i]}")
        self.memory_window.render(self.memory)
        pygame.display.update()
        pygame.display.flip()
    
    def get_code(self):
        return self.code_window.return_text()
    
    def set_code(self, code):
        self.code_window.recive_text(code)
    
    def get_language(self):
        """Get current language"""
        return self.code_window.get_language()
    
    def get_code_with_language(self):
        """Get code with language information"""
        return {
            "language": self.code_window.get_language(),
            "code": self.code_window.return_text()
        }

    def get_console_text(self):
        return self.console_window.return_text()
    
    def set_console_text(self, text):
        if text is None:
            return
        self.console_window.add_output(text)
    
    def add_console_text(self, text):
        if text is None:
            return
        self.console_window.add_output(text)
    
    def request_console_input(self):
        return self.console_window.request_input()
    
    def get_console_input(self):
        return self.console_window.get_input()

    def set_highlight_line(self, line):
        self.code_window.highlight_line(line)
    
    def is_console_waiting_for_input(self):
        return self.console_window.is_waiting_for_input()
    
    def clear_console(self):
        """Clear the console window"""
        self.console_window.clear_console()
    
    def set_registers(self, registers):
        for i in range(len(self.register_window)):
            self.register_window[i].render(registers[i])

    def set_memory(self, memory):
        self.memory_window.render(memory)

    def get_buttons(self):
        return {
            "run": self.working,
            "step": self.stepping,
            "stop": self.stopping,
            "clear": self.clearing
        }
    
    def clear_code_window(self):
        """Clear the code window"""
        self.code_window.recive_text([""], erase=True)
    

    def __handle_events(self):
        # Reset button states at the beginning of each frame
        self.working = False
        self.stepping = False
        self.stopping = False
        self.clearing = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            
            # Handle button clicks
            if self.run_button.handle_event(event):
                self.working = True
            if self.step_button.handle_event(event):
                self.stepping = True
            if self.stop_button.handle_event(event):
                self.stopping = True
            if self.clear_button.handle_event(event):
                self.clearing = True
            
            # Handle language toggle
            new_language = self.language_button.handle_event(event)
            if new_language:
                self.code_window.set_language(new_language)
                
            self.code_window.handle_event(event)
            self.console_window.handle_event(event)
            if event.type == pygame.VIDEORESIZE:
                self.code_window._reinit()
                self.language_button._reinit()
                self.clear_button._reinit()
                self.run_button._reinit()
                self.step_button._reinit()
                self.stop_button._reinit()
                self.console_window._reinit()
                for window in self.register_window:
                    window._reinit()
                self.memory_window._reinit()
                


def main():
    render_main = RenderMain()
    render_main.run()

if __name__ == "__main__":
    main()