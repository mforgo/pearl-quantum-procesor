import pygame
import background
import frontground

class RenderMain:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("CPU Emulator")
        self.running = True
        self.base_color = (0, 1, 0)
        self.background = background.Background(self.screen, self.base_color)
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
        while self.running:
            self.__handle_events()
            self.__render()
            self.clock.tick(20)

    def __render(self):
        self.background.render()
        pygame.display.update()
        pygame.display.flip()
    
    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

test = RenderMain()
test.run()