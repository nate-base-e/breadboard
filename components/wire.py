# wire.py

import pygame as pg

class Wire:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def draw(self, screen):
        pg.draw.line(screen, (255, 0, 0), self.start, self.end, 3)
