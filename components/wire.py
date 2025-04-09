# wire.py

import pygame as pg
import math

try:
    WIRE_IMAGE = pg.image.load("/images/WireSprite.png").convert_alpha()
except Exception as e:
    print("Failed to load wire sprite:", e)
    WIRE_IMAGE = None

class Wire:
    def __init__(self, start, end): #(self, start, component1, end, component2)
        self.start = start
        #self.component1 = component1
        self.end = end
        #self.component2 = component2

    def draw(self, screen):
        if WIRE_IMAGE:
            # Calculating angle and distance
            dx = self.end[0] - self.start[0]
            dy = self.end[1] - self.start[1]
            angle = math.degrees(math.atan2(-dy, dx))
            length = math.hypot(dx, dy)

            # Scaling the image based on the length
            scaled_image = pg.transform.smoothscale(WIRE_IMAGE, (int(length), 12))  # 12 is wire thickness
            rotated_image = pg.transform.rotate(scaled_image, angle)
            rect = rotated_image.get_rect(center=((self.start[0] + self.end[0]) // 2, (self.start[1] + self.end[1]) // 2))

            # Draw
            screen.blit(rotated_image, rect.topleft)
        else:
            # fallback to a line or something simple
            pg.draw.line(screen, (200, 0, 0), self.start, self.end, 3)

    # def getotherend(self, location):
    #     if location == self.end:
    #         return self.component2
    #     elif location == self.start:
    #         return self.component1


    #need a function to call the breadboard at the location of the wire start
    #the breadboard node should contain information of what component node is on it
    #get the component from breadboard and associate with start/end variables
    #check the nodes agianst themsevles. if the node is the same as the one that is calling the other end, filter out that node.