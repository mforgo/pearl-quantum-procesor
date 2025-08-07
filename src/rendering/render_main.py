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
        self.run_button = frontground.Button(self.screen, (3.7, 4.35), pos=(44.44, 8.7), base_color=self.base_color, symbol="RUN")
        self.step_button = frontground.Button(self.screen, (3.7, 4.35), pos=(44.44, 13.04), base_color=self.base_color, symbol="STEP")
        self.stop_button = frontground.Button(self.screen, (3.7, 4.35), pos=(44.44, 17.39), base_color=self.base_color, symbol="STOP")
        self.console_window = frontground.Code_window(self.screen, (40.74, 26.09), pos=(7.41, 65.22), base_color=self.base_color, active=False)
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

    def run(self):
        return self.__main_loop()

    def __main_loop(self):
        self.console_window.recive_text("some text here", erase=True)
        self.__handle_events()
        self.__render()
        return self.running

    def __render(self):
        self.background.render()
        self.code_window.render()
        self.run_button.render()
        self.step_button.render()
        self.stop_button.render()
        self.console_window.render()
        for window in self.register_window:
            window.render("123456789012345678")
        self.memory_window.render("Memory content here")
        pygame.display.update()
        pygame.display.flip()
    
    def get_code(self):
        return self.code_window.return_text()

    def get_console_text(self):
        return self.console_window.return_text()
    
    def set_console_text(self, text):
        if text is None:
            return
        self.console_window.recive_text(text, erase=True)
    
    def add_console_text(self, text):
        if text is None:
            return
        self.console_window.recive_text(text, erase=False)
    
    def set_registers(self, registers):
        for register, i in zip(registers, range(len(self.register_window))):
            self.register_window[i].set_value(register)
    
    def set_memory(self, memory):
        self.memory_window.set_value(memory)
    
    def get_buttons(self):
        return {
            "run": self.working,
            "step": self.stepping,
            "stop": self.stopping
        }
    

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            self.working = self.run_button.handle_event(event)
            self.stepping = self.step_button.handle_event(event)
            self.stopping = self.stop_button.handle_event(event)
            self.code_window.handle_event(event)
            self.console_window.handle_event(event)
            if event.type == pygame.VIDEORESIZE:
                self.code_window._reinit()
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