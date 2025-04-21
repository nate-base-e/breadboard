# wire.py

import pygame as pg
import math
import os

class Wire:

    wire_start_img = None
    wire_middle_img = None
    wire_end_img = None

    def __init__(self, start, end): #(self, start, component1, end, component2)
        self.start = start
        #self.component1 = component1
        self.end = end
        #self.component2 = component2

        if Wire.wire_start_img is None:
            current_dir = os.path.dirname(__file__)
            image_path = os.path.join(current_dir, "..", "images", "WireSprite.png")
            try:
                full_img = pg.image.load(image_path).convert_alpha()

                start_width = 100
                end_width = 100
                middle_width = full_img.get_width() - start_width - end_width
                height = full_img.get_height()

                Wire.wire_start_img = full_img.subsurface((0, 0, start_width, height))
                Wire.wire_middle_img = full_img.subsurface((start_width, 0, middle_width, height))
                Wire.wire_end_img = full_img.subsurface((start_width + middle_width, 0, end_width, height))

            except Exception as e:
                print("Failed to load/slice wire sprite:", e)


    def draw(self, screen):
        if not all([Wire.wire_start_img, Wire.wire_middle_img, Wire.wire_end_img]):
            # fallback to a line or something simple
            pg.draw.line(screen, (200, 0, 0), self.start, self.end, 3)

        dx = self.end[0] - self.start[0]
        dy = self.end[1] - self.start[1]
        angle = math.atan2(dy, dx)
        length = math.hypot(dx, dy)

        total_height = 12  # wire thickness
        start_scaled = pg.transform.smoothscale(Wire.wire_start_img, (10, total_height))
        end_scaled = pg.transform.smoothscale(Wire.wire_end_img, (10, total_height))

        middle_tile_width = 8
        middle_scaled = pg.transform.smoothscale(Wire.wire_middle_img, (middle_tile_width, total_height))
        middle_count = max(1, int((length - 20) / middle_tile_width))

        wire_surface = pg.Surface((int(length), total_height), pg.SRCALPHA)
        wire_surface.blit(start_scaled, (0, 0))
        for i in range(middle_count):
            wire_surface.blit(middle_scaled, (10 + i * middle_tile_width, 0))
        wire_surface.blit(end_scaled, (10 + middle_count * middle_tile_width, 0))

        rotated_wire = pg.transform.rotate(wire_surface, -math.degrees(angle))
        center_x = (self.start[0] + self.end[0]) // 2
        center_y = (self.start[1] + self.end[1]) // 2
        rotated_rect = rotated_wire.get_rect(center=(center_x, center_y))

        screen.blit(rotated_wire, rotated_rect.topleft)

    # def getotherend(self, location):
    #     if location == self.end:
    #         return self.component2
    #     elif location == self.start:
    #         return self.component1


    #need a function to call the breadboard at the location of the wire start
    #the breadboard node should contain information of what component node is on it
    #get the component from breadboard and associate with start/end variables
    #check the nodes agianst themsevles. if the node is the same as the one that is calling the other end, filter out that node.