import pygame

class Background:
    def __init__(self, screen, base_color=(0, 1, 0)):
        self.screen = screen
        self.black = (0, 0, 0)
        self.base_color = base_color

    def __color(self, percentage):
        """Returns a color based on the percentage."""
        base_color = [int(self.base_color[0] * 255), int(self.base_color[1] * 255), int(self.base_color[2] * 255)]
        if percentage <= 50:
            return (base_color[0] * (percentage / 50), base_color[1] * (percentage / 50), base_color[2] * (percentage / 50))
        else:
            return (255 if base_color[0] == 255 else base_color[0] * ((100 - percentage) / 50), 
                    255 if base_color[1] == 255 else base_color[1] * ((100 - percentage) / 50), 
                    255 if base_color[2] == 255 else base_color[2] * ((100 - percentage) / 50))

