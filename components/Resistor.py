#Resistor file
import pygame as pg
import os

class Resistor:
    def __init__(self, x, y):
        image_path = os.path.join("images", "Resistor.png")
        self.image = pg.image.load(image_path)
        self.image = pg.transform.scale(self.image, (300, 300))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.dragging = True
            mouse_x, mouse_y = event.pos
            self.offset_x = self.rect.x - mouse_x
            self.offset_y = self.rect.y - mouse_y

        elif event.type == pg.MOUSEBUTTONUP and self.dragging:
            self.dragging = False
            self.snap_to_grid()

        elif event.type == pg.MOUSEMOTION and self.dragging:
            mouse_x, mouse_y = event.pos
            self.rect.x = mouse_x + self.offset_x
            self.rect.y = mouse_y + self.offset_y

    def snap_to_grid(self, grid_size=20):
        self.rect.x = round(self.rect.x / grid_size) * grid_size
        self.rect.y = round(self.rect.y / grid_size) * grid_size

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def is_dragging(self):
        return self.dragging
