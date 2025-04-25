import pygame as pg
import pygame.transform


class Lights:
    GRID_SIZE = 20

    def __init__(self,x,y,off_image,on_image):

        self.x = round(x / self.GRID_SIZE) * self.GRID_SIZE
        self.y = round(y / self.GRID_SIZE) * self.GRID_SIZE
        self.on_image = pygame.transform.scale(on_image,(70,112))
        self.off_image = pygame.transform.scale(off_image,(70,112))
        self.rect = self.off_image.get_rect(center=(self.x + self.GRID_SIZE // 2,(self.y + self.GRID_SIZE)))
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

        self.volt = False

        self.state = False

        self.nodes = {
            "anode": (
                self.rect.centerx + (self.rect.width // 4),  # Right terminal
                self.rect.bottom # Just above bottom edge
            ),
            "cathode": (
                self.rect.centerx - (self.rect.width // 4),  # Left terminal
                self.rect.bottom # Just above bottom edge
            )
        }

        self.nodes = {
            "anode": (
                round(self.nodes["anode"][0] / self.GRID_SIZE) * self.GRID_SIZE,
                round(self.nodes["anode"][1] / self.GRID_SIZE) * self.GRID_SIZE
            ),
            "cathode": (
                round(self.nodes["cathode"][0] / self.GRID_SIZE) * self.GRID_SIZE,
                round(self.nodes["cathode"][1] / self.GRID_SIZE) * self.GRID_SIZE
            )
        }

        self.node_voltages = {
            'anode': 0,
            'cathode': 0
        }

    def draw(self, surface):
        if self.state:
            surface.blit(self.on_image, self.rect)
        else:
            surface.blit(self.off_image, self.rect)

        for term_name, (dx, dy) in self.nodes.items():
            x = self.rect.x + dx
            y = self.rect.y + dy
            color = (0, 255, 0) if "input" in term_name else (255, 0, 0)  # Green=input, Red=output
            pg.draw.circle(surface, color, (x, y), 5)


    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                mouse_x, mouse_y = event.pos
                self.offset_x = self.rect.x - (round(mouse_x / self.GRID_SIZE) * self.GRID_SIZE)
                self.offset_y = self.rect.y - (round(mouse_y / self.GRID_SIZE) * self.GRID_SIZE)

            return True

        elif event.type == pg.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pg.MOUSEMOTION and self.dragging:
            mouse_x, mouse_y = event.pos
            new_x = round(mouse_x / self.GRID_SIZE) * self.GRID_SIZE + self.offset_x
            new_y = round(mouse_y / self.GRID_SIZE) * self.GRID_SIZE + self.offset_y

            # Update positions
            self.x = new_x
            self.y = new_y
            self.rect.topleft = (new_x, new_y)

            self.nodes = {
                "anode": (
                    new_x + self.rect.width // 2 + (self.rect.width // 4),
                    new_y + self.rect.height - (self.GRID_SIZE // 2) - self.GRID_SIZE
                ),
                "cathode": (
                    new_x + self.rect.width // 2 - (self.rect.width // 4),
                    new_y + self.rect.height - (self.GRID_SIZE // 2) - self.GRID_SIZE
                )
            }

            self.nodes = {
                "anode": (
                    round(self.nodes["anode"][0] / self.GRID_SIZE) * self.GRID_SIZE,
                    round(self.nodes["anode"][1] / self.GRID_SIZE) * self.GRID_SIZE
                ),
                "cathode": (
                    round(self.nodes["cathode"][0] / self.GRID_SIZE) * self.GRID_SIZE,
                    round(self.nodes["cathode"][1] / self.GRID_SIZE) * self.GRID_SIZE
                )
            }

        return False

    def stop_dragging(self):
        self.dragging = False

    def turn_on(self):
        self.state = True

    def turn_off(self):
        self.state = False

    def toggle(self):
        self.state = not self.state

    def is_on(self):
        return self.state

    def eval_state(self):
        if self.volt == True:
            self.turn_on()
        else:
            self.turn_off()

    def set_voltage(self, volt):
        self.volt = volt
        self.eval_state()

    def get_node_positions(self):
        return self.nodes




