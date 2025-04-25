import pygame as pg
class Lights:
    GRID_SIZE = 20

    def __init__(self,x,y,off_image,on_image):

        self.x = round(x / self.GRID_SIZE) * self.GRID_SIZE
        self.y = round(y / self.GRID_SIZE) * self.GRID_SIZE
        self.on_image = on_image
        self.off_image = off_image
        self.rect = off_image.get_rect(center=(self.x + self.GRID_SIZE // 2,(self.y + self.GRID_SIZE // 2) - self.GRID_SIZE))
        self.voltage = 0
        self.voltageThreshold = 2

        self.nodes = {
            "anode": (
                self.rect.centerx + (self.rect.width // 4),  # Right terminal
                self.rect.bottom - (self.GRID_SIZE // 2) - self.GRID_SIZE # Just above bottom edge
            ),
            "cathode": (
                self.rect.centerx - (self.rect.width // 4),  # Left terminal
                self.rect.bottom - (self.GRID_SIZE // 2) - self.GRID_SIZE # Just above bottom edge
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

        self.state = False

        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def draw(self, surface):
        if self.state:
            surface.blit(self.on_image, self.rect)
        else:
            surface.blit(self.off_image, self.rect)


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
        if self.voltage > self.voltageThreshold:
            self.state = True
        else:
            self.state = False

    def return_volt(self):
        return self.voltage

    def set_voltage(self,volt):
        self.voltage = volt
        self.eval_state()




