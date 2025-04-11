import pygame

# example of how to draw it in main: lights.drawNumber(screen,3)
class Lights:

    def __init__(self,x,y):

        self.x = x
        self.y = y

        self.segment_positions = [
            (x+5,y,20,5),
            (x+25,y+5,5,20),
            (x+25,y+30,5,20),
            (x+5,y+50,20,5),
            (x,y+30,5,20),
            (x,y+5,5,20),
            (x+5,y+25,20,5)
        ]

        # dictionary for each segments and there sizes for the rectangles when drawn
        self.binaries = {0:[1,1,1,1,1,1,0],
                         1:[0,1,1,0,0,0,0],
                         2:[1,1,0,1,1,0,1],
                         3:[1,1,1,1,0,0,1],
                         4:[0,1,1,0,0,1,1],
                         5:[1,0,1,1,0,1,1],
                         6:[1,0,1,1,1,1,1],
                         7:[1,1,1,0,0,0,0],
                         8:[1,1,1,1,1,1,1],
                         9:[1,1,1,0,0,1,1]}

    def drawNumber(self,surface,number):
        segments = self.binaries[number]
        pygame.draw.rect(surface,'black',(self.x,self.y,30,55))
        for i, on in enumerate(segments):
            if on:
                pygame.draw.rect(surface,'red',self.segment_positions[i])
            else:
                pygame.draw.rect(surface, 'black', self.segment_positions[i])