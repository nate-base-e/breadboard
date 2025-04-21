#Resistor file
import pygame as pg
import os

class Resistor:
    def __init__(self, x, y):
        # Load image from images folder
        image_path = os.path.join("images", "Resistor.png")
        try:
            self.image = pg.image.load(image_path)
        except Exception as e:
            print(f"Failed to load resistor image at {image_path}: {e}")
            self.image = pg.Surface((100, 40))
            self.image.fill((255, 0, 0))

        self.image = pg.transform.scale(self.image, (250, 200))  # size of the resistor
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

        elif event.type == pg.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                self.snap_to_grid()

        elif event.type == pg.MOUSEMOTION:
            if self.dragging:
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

