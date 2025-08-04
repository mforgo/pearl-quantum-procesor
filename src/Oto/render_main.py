import pygame

class RenderMain:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("CPU Emulator")
        self.running = True
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.light_green = 50
        self.dark_green = 50

    def run(self):
        self.__main_loop()
        pygame.quit()

    def __green(self, percentage):
        if percentage <= 50:
            return (0, 255 * (percentage / 50), 0)
        else:
            return (255 * ((100 - percentage) / 50), 255, 255 * ((100 - percentage) / 50))

    def __main_loop(self):
        while self.running:
            self.__handle_events()
            self.__render()
    
    def __render(self):
        self.screen.fill(self.black)
        pygame.display.flip()
    
    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

test = RenderMain()
test.run()