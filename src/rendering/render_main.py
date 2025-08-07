import pygame
import background
import frontground

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
        self.console_window = frontground.Code_window(self.screen, (40.74, 26.09), pos=(7.41, 65.22), base_color=self.base_color)
        self.register_window = [
            frontground.RegisterWindow(self.screen, (16.67, 4.35), pos=(51.85, 8.7), base_color=self.base_color),
            frontground.RegisterWindow(self.screen, (16.67, 4.35), pos=(51.85, 17.39), base_color=self.base_color),
            frontground.RegisterWindow(self.screen, (16.67, 4.35), pos=(51.85, 26.09), base_color=self.base_color),
            frontground.RegisterWindow(self.screen, (16.67, 4.35), pos=(51.85, 34.78), base_color=self.base_color),
            frontground.RegisterWindow(self.screen, (16.67, 4.35), pos=(72.22, 8.7), base_color=self.base_color),
            frontground.RegisterWindow(self.screen, (16.67, 4.35), pos=(72.22, 17.39), base_color=self.base_color),
            frontground.RegisterWindow(self.screen, (16.67, 4.35), pos=(72.22, 26.09), base_color=self.base_color),
            frontground.RegisterWindow(self.screen, (16.67, 4.35), pos=(72.22, 34.78), base_color=self.base_color),
            ]
        self.memory_window = frontground.RegisterWindow(self.screen, (40.74, 47.83), pos=(51.85, 43.48), base_color=self.base_color)
        self.clock = pygame.time.Clock()

    def run(self):
        self.__main_loop()
        pygame.quit()

    def __color(self, percentage):
        """Returns a color based on the percentage."""
        base_color = [int(self.base_color[0] * 255), int(self.base_color[1] * 255), int(self.base_color[2] * 255)]
        if percentage <= 50:
            return (base_color[0] * (percentage / 50), base_color[1] * (percentage / 50), base_color[2] * (percentage / 50))
        else:
            return (255 if base_color[0] == 255 else base_color[0] * ((100 - percentage) / 50), 
                    255 if base_color[1] == 255 else base_color[1] * ((100 - percentage) / 50), 
                    255 if base_color[2] == 255 else base_color[2] * ((100 - percentage) / 50))

    def __main_loop(self):
        self.console_window.recive_text("some text here", erase=False)
        while self.running:
            self.__handle_events()
            self.__render()
            self.clock.tick(20)

    def __render(self):
        self.background.render()
        self.code_window.render()
        self.console_window.render()
        for window in self.register_window:
            window.render("123456789012345678")
        self.memory_window.render("Memory content here")
        pygame.display.update()
        pygame.display.flip()
    
    def __handle_events(self):
        for event in pygame.event.get():
            self.code_window.handle_event(event)
            self.console_window.handle_event(event)
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            if event.type == pygame.VIDEORESIZE:
                self.code_window._reinit()
                self.console_window._reinit()
                for window in self.register_window:
                    window._reinit()
                self.memory_window._reinit()
                


def main():
    render_main = RenderMain()
    render_main.run()

if __name__ == "__main__":
    main()