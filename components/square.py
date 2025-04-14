#board that other components will be placed on
#45x80 grid 3600 total squares
#each square 16px
import pygame as pg

class Square():

    def __init__(self, surface, pos_x, pos_y):
        self.clicked = False
        pg.draw.rect(surface, (250, 241, 142), (pos_x, pos_y, 20, 20))
        pg.draw.circle(surface, (99, 96, 57), (pos_x, pos_y), 4)







