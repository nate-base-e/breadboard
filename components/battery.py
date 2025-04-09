import pygame
import pygame.gfxdraw
import sys
pygame.init()


class Battery:
    def __init__(self, x, y, width, height, callback):
        self.voltage = 1.5
        self.font = pygame.font.SysFont('Times New Roman', 15)
        self.text = '1.5V'

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.callback = callback

    def getVoltage(self):
        return self.voltage

    def setVoltage(self, voltage):
        self.voltage = voltage
        self.text = f"{round(self.voltage, 1)}V"

    def draw(self, screen):
        # Render the text
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_x = (self.x + (self.width - text_surface.get_width()) // 2) + 10
        text_y = self.y + (self.height - text_surface.get_height()) // 2

        image = pygame.image.load('images/Battery.png')
        image = pygame.transform.scale(image, (self.width, self.height))
        screen.blit(image, (self.x, self.y))
        screen.blit(text_surface, (text_x, text_y))

    def handle_event(self, event):
        # Check if mouse is hovering over the button
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            # Check for click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.callback:
                    self.callback()  # Execute callback function


class BatteryProperties:
    def __init__(self, battery):
        self.battery = battery
        self.current_voltage = battery.getVoltage()
        self.prev_valid_voltage = self.current_voltage

        pygame.init()
        self.width, self.height = 400, 80
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Battery Properties")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.DARK_GRAY = (150, 150, 150)

        # Font
        self.font = pygame.font.SysFont('Times New Roman', 20)

        # Text input
        self.input_rect = pygame.Rect(100, 35, 100, 32)
        self.input_text = str(self.current_voltage)
        self.active = False

        # Slider
        self.slider_rect = pygame.Rect(225, 47.5, 150, 5)
        self.slider_handle_rect = pygame.Rect(0, 35, 15, 30)
        self.update_slider_handle()
        self.dragging = False

        self.run()

    def update_slider_handle(self):
        # Position handle based on current voltage (0-12V range)
        pos = (self.current_voltage / 12.0) * 150
        self.slider_handle_rect.x = 225 + pos - 12  # Center handle

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Text input handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False

                # Check if clicked on slider handle or track
                if (self.slider_handle_rect.collidepoint(event.pos) or
                        self.slider_rect.collidepoint(event.pos)):
                    self.dragging = True
                    # Immediate update to clicked position
                    self.handle_slider_drag(pygame.mouse.get_pos()[0])

            if event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False

            if event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    self.handle_slider_drag(event.pos[0])

            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        self.active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        if event.unicode.isdigit() or event.unicode == '.':
                            self.input_text += event.unicode

                    # Update voltage from text input
                    self.update_from_text()

    def handle_slider_drag(self, mouse_x):
        # Constrain to slider area
        mouse_x = max(self.slider_rect.left, min(mouse_x, self.slider_rect.right))
        self.current_voltage = ((mouse_x - self.slider_rect.left) / self.slider_rect.width) * 12
        self.current_voltage = round(self.current_voltage, 2)
        self.input_text = str(self.current_voltage)
        self.battery.setVoltage(self.current_voltage)
        self.prev_valid_voltage = self.current_voltage
        self.update_slider_handle()

    def update_from_text(self):
        try:
            new_voltage = float(self.input_text)
            if 0 <= new_voltage <= 12:
                self.current_voltage = new_voltage
                self.prev_valid_voltage = new_voltage
                self.battery.setVoltage(new_voltage)
                self.update_slider_handle()
            elif new_voltage < 0:
                self.current_voltage = 0
                self.prev_valid_voltage = 0
                self.battery.setVoltage(0)
                self.update_slider_handle()
            elif new_voltage > 12:
                self.current_voltage = 12
                self.prev_valid_voltage = 12
                self.battery.setVoltage(12)
                self.update_slider_handle()
        except ValueError:
            pass

    def draw(self):
        self.screen.fill(self.WHITE)

        # Draw title
        title = self.font.render("Battery properties:", True, self.BLACK)
        self.screen.blit(title, (20, 5))

        # Draw voltage label
        voltage_label = self.font.render("Voltage", True, self.BLACK)
        self.screen.blit(voltage_label, (20, 40))

        # Draw text input box
        color = self.BLACK if self.active else self.GRAY
        pygame.draw.rect(self.screen, color, self.input_rect, 2)
        text_surface = self.font.render(self.input_text, True, self.BLACK)
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

        # Draw slider track
        pygame.draw.rect(self.screen, self.DARK_GRAY, self.slider_rect)

        # Draw slider handle
        handle_color = self.WHITE
        pygame.draw.rect(self.screen, handle_color, self.slider_handle_rect)
        pygame.draw.rect(self.screen, self.BLACK, self.slider_handle_rect, 1)

        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.handle_events()
            self.draw()
            clock.tick(60)


if __name__ == "__main__":
    BatteryProperties(Battery(0,0,0,0,None))