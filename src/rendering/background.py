import pygame
from random import randint

class Background:
    def __init__(self, screen, base_color=(0, 1, 0)):
        self.screen = screen
        self.black = (0, 0, 0)
        self.base_color = base_color
        self.filling_percentage = 50
        self.screen_size = screen.get_size()
        self.char_size = self.screen_size[0] // 100

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
        pass

    def random_letter(self, index):
        """Returns a random letter based on the index."""
        return chr(index)