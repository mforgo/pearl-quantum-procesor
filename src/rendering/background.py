import pygame
from random import randint

class Background:
    def __init__(self, screen, base_color=(0, 1, 0)):
        self.screen = screen
        self.base_color = base_color
        self.black = self.__color(0)
        self.filling_percentage = 50
        self.screen_size = screen.get_size()
        self.char_size = self.screen_size[0] // 10

    def __color(self, percentage):
        """Returns a color based on the percentage."""
        base_color = [int(self.base_color[0] * 255), int(self.base_color[1] * 255), int(self.base_color[2] * 255)]
        if percentage <= 50:
            return (base_color[0] * (percentage / 50), base_color[1] * (percentage / 50), base_color[2] * (percentage / 50))
        else:
            factor = (percentage - 50) / 50
            return (
                int(base_color[0] + (255 - base_color[0]) * factor),
                int(base_color[1] + (255 - base_color[1]) * factor),
                int(base_color[2] + (255 - base_color[2]) * factor)
            )
    
    def calculate_one(self, position, length):
        pass

    def render(self):
        self.screen.fill(self.black)
        for i in range(0, self.screen_size[0], self.char_size):
            for j in range(0, self.screen_size[1], self.char_size):
                letter = self.random_letter(randint(0, 93))
                color = self.__color(self.filling_percentage)
                font = pygame.font.SysFont(None, self.char_size)
                text = font.render(letter, True, color)
                self.screen.blit(text, (i, j))

    def random_letter(self, index):
        """Returns a random letter based on the index."""
        return chr(index % 94 + 33)  # 33 - 126

pygame.init()
pygame.font.init()

test = Background(pygame.display.set_mode((800, 600)))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    test.render()
    pygame.display.flip()