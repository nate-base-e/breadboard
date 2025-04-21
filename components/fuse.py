import pygame as pg

class Fuse:
    def __init__(self, x, y, width=120, height=30):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pg.Rect(x, y, width, height)
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.blown = False

    def draw(self, surface):
        self.rect.topleft = (self.x, self.y)
        center_y = self.y + self.height // 2

        # Draw metal caps
        cap_width = 15
        cap_color = (150, 150, 150)
        left_cap = pg.Rect(self.x, self.y, cap_width, self.height)
        right_cap = pg.Rect(self.x + self.width - cap_width, self.y, cap_width, self.height)
        pg.draw.rect(surface, cap_color, left_cap, border_radius=5)
        pg.draw.rect(surface, cap_color, right_cap, border_radius=5)

        # Draw glass body
        glass_color = (180, 230, 255)
        glass_rect = pg.Rect(self.x + cap_width, self.y, self.width - 2 * cap_width, self.height)
        pg.draw.rect(surface, glass_color, glass_rect, border_radius=6)

        # Draw filament (zigzag wire inside)
        if not self.blown:
            points = []
            start_x = self.x + cap_width + 5
            step = (self.width - 2 * cap_width - 10) // 6
            for i in range(7):
                x = start_x + i * step
                y = center_y - 6 if i % 2 == 0 else center_y + 6
                points.append((x, y))
            pg.draw.lines(surface, (100, 100, 100), False, points, 2)
        else:
            # Draw broken filament
            pg.draw.line(surface, (255, 100, 0), (self.x + cap_width + 5, center_y - 6),
                         (self.x + self.width - cap_width - 5, center_y + 6), 2)

            # Optional: overlay X to show it's blown
            pg.draw.line(surface, (255, 0, 0), self.rect.topleft, self.rect.bottomright, 2)
            pg.draw.line(surface, (255, 0, 0), self.rect.topright, self.rect.bottomleft, 2)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                mouse_x, mouse_y = event.pos
                self.offset_x = self.x - mouse_x
                self.offset_y = self.y - mouse_y

        elif event.type == pg.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pg.MOUSEMOTION and self.dragging:
            mouse_x, mouse_y = event.pos
            self.x = mouse_x + self.offset_x
            self.y = mouse_y + self.offset_y
