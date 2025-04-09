#board that other components will be placed on
#45x80 grid
#each square 16px
import pygame as pg

class Square():

    def __init__(self):
        self.clicked = False

    def draw(self, surface, pos_x, pos_y):
        pg.draw.rect(surface, (250, 241, 142), (pos_x, pos_y, 16, 16))
        pg.draw.circle(surface, (99, 96, 57), (pos_x + 8, pos_y + 8), 4)







