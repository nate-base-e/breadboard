import pygame as pg

class Toolbox:
    def __init__(self, screen_width):
        self.width = screen_width
        self.height = 100  # height of the top toolbox
        self.bg_color = (100, 100, 100)  # gray background
        self.box_width = 100
        self.components = []  # component names or placeholders
        self.scroll_offset = 0

        # Sample placeholder components
        self.components = ['battery', 'Buttons', 'gates', 'lights', 'resistor', 'square', 'switch', 'wire']

    def draw(self, screen):
        # Draw background
        toolbox_rect = pg.Rect(0, 0, self.width, self.height)
        pg.draw.rect(screen, self.bg_color, toolbox_rect)

        # Draw boxes for each component
        for i, name in enumerate(self.components):
            x = i * self.box_width - self.scroll_offset
            box_rect = pg.Rect(x, 0, self.box_width, self.height)

            if box_rect.right < 0 or box_rect.left > self.width:
                continue  # skip off-screen boxes

            pg.draw.rect(screen, (255, 255, 255), box_rect, 2)  # white outline

            # Draw component name (placeholder text)
            font = pg.font.SysFont(None, 24)
            text = font.render(name, True, (255, 255, 255))
            text_rect = text.get_rect(center=(x + self.box_width // 2, self.height // 2))
            screen.blit(text, text_rect)

    def handle_scroll(self, direction):
        max_offset = max(0, len(self.components) * self.box_width - self.width)
        if direction == 'left':
            self.scroll_offset = max(0, self.scroll_offset - 40)
        elif direction == 'right':
            self.scroll_offset = min(max_offset, self.scroll_offset + 40)
