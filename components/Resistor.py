import pygame as pg
import os


class Resistor:
    def __init__(self, x, y):
        image_path = os.path.join("images", "Resistor.png")
        try:
            self.image = pg.image.load(image_path)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.image = pg.Surface((100, 40))
            self.image.fill((255, 20, 20))

        self.image = pg.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

        # === Add these lines ===
        self.resistance = 100  # ohms
        self.voltage_drop = 0
        self.current = 0

    def update_voltage(self, voltage):
        self.voltage_drop = voltage
        if self.resistance != 0:
            self.current = voltage / self.resistance
        else:
            self.current = 0

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

    def get_connection_points(self):
        left = (self.rect.left + 60, self.rect.centery)
        right = (self.rect.right - 60, self.rect.centery)
        return [left, right]

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

        # Debug: Draw connection points
        for point in self.get_connection_points():
            pg.draw.circle(screen, (0, 255, 0), point, 5)

    def is_dragging(self):
        return self.dragging

    @classmethod
    def center_top(cls, screen_width=1280, image_width=200, y=20):
        x = (screen_width - image_width) // 2
        return cls(x, y)


# This code is for the wire to call and get the nodes of this component, do not remove (unless you want to break something in which case go ahead).
    def get_node_positions(self):
        points = self.get_connection_points()
        return {
            "left": (points[0]),
            "right": (points[1])
        }
    def get_voltage(self):
        return self.voltage_drop
