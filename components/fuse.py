import pygame as pg

class Fuse:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 80  # Wider fuse
        self.height = 30  # Taller fuse
        self.color = (50, 50, 50)  # Dark gray body
        self.cap_color = (150, 150, 150)  # Light gray for metal caps
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.node_offset = 30  # Farther node distance
        self.node_radius = 4    # Smaller green nodes

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.rect.collidepoint(event.pos):
                    self.dragging = True
                    mouse_x, mouse_y = event.pos
                    self.offset_x = self.x - mouse_x
                    self.offset_y = self.y - mouse_y

        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

        elif event.type == pg.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.x = mouse_x + self.offset_x
                self.y = mouse_y + self.offset_y

    def get_node_positions(self):
        center_y = self.y + self.height // 2
        left_node = (self.x - self.node_offset, center_y)
        right_node = (self.x + self.width + self.node_offset, center_y)
        return {"left": left_node, "right": right_node}

    def draw(self, surface):
        # Update rect
        self.rect.topleft = (self.x, self.y)
        center_y = self.y + self.height // 2

        # Draw connection wires from green node to fuse
        pg.draw.line(surface, (0, 0, 0), (self.x - self.node_offset + self.node_radius, center_y), (self.x, center_y), 3)
        pg.draw.line(surface, (0, 0, 0), (self.x + self.width, center_y), (self.x + self.width + self.node_offset - self.node_radius, center_y), 3)

        # Draw the fuse body (rounded rectangle)
        body_rect = pg.Rect(self.x, self.y, self.width, self.height)
        pg.draw.rect(surface, self.color, body_rect, border_radius=8)

        # Draw metal caps on each side
        cap_width = 10
        cap_left = pg.Rect(self.x, self.y, cap_width, self.height)
        cap_right = pg.Rect(self.x + self.width - cap_width, self.y, cap_width, self.height)
        pg.draw.rect(surface, self.cap_color, cap_left, border_radius=4)
        pg.draw.rect(surface, self.cap_color, cap_right, border_radius=4)

        # Draw green connection points (smaller and farther)
        node_positions = self.get_node_positions()
        for pos in node_positions.values():
            pg.draw.circle(surface, (0, 255, 0), pos, self.node_radius)
