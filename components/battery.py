import pygame
import pygame.gfxdraw
import sys
pygame.init()

GRID_SIZE = 20

# Kasey - Circuit function. Lots of bugs but most of the logic is there.
'''
def check_circuit(components, wires):
    inputs = ["cathode", "bottom", "in", "in1", "in2"]
    outputs = ["anode", "top", "out", "right"]
    and_sum = 0

    for comp in components:  # Get all components
        for node, pos in comp.get_node_positions().items():  # Get all nodes
            for wire in wires:  # Get all wires
                if wire.get_other_end(comp, node):  # Is the component connected to something?
                    connected_comp = wire.get_other_end(comp, node)[0]
                    connected_node = wire.get_other_end(comp, node)[1]
                    if node in outputs and connected_node in inputs:  # An output is connected to an input
                        if isinstance(connected_comp, Gates):  # Is the input a gate?
                            if connected_comp.get_gate_type() == "NOT":  # Is the input a NOT gate?
                                if isinstance(comp, Battery):  # Is the output a battery?
                                    connected_comp.set_voltage(not comp.has_voltage())  # Yes: Use has_voltage
                                else:
                                    connected_comp.set_voltage(not comp.get_voltage())

                            elif connected_comp.get_gate_type() == "AND":  # Is the input an AND gate?
                                if connected_node == "in1" and comp.get_voltage():
                                    and_sum += 1
                                if connected_node == "in2" and comp.get_voltage():
                                    and_sum += 1
                                if and_sum == 2:  # Both inputs have voltage coming in
                                    connected_comp.set_voltage(True)
                                else:
                                    connected_comp.set_voltage(False)

                            else:  # OR gate
                                if comp.get_voltage():
                                    connected_comp.set_voltage(True)

                        else:  # Input is not a gate
                            if isinstance(comp, Switch):  # Is the output a switch?
                                if comp.get_voltage() and comp.is_on():
                                    connected_comp.set_voltage(True)
                            else:
                                if comp.get_voltage():
                                    connected_comp.set_voltage(True)
'''
class Battery:
    def __init__(self, x, y, width, height, screen):
        self.voltage = 1.5
        self.font = pygame.font.SysFont('Times New Roman', 15)
        self.text = '1.5V'

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.circle_radius = 2
        self.circle_color = (0, 255, 0)

        self.dragging = False

        self.properties = BatteryProperties(self, screen)

    def get_voltage(self):
        return self.voltage

    def has_voltage(self):
        return self.voltage > 0

    def set_voltage(self, voltage):
        self.voltage = voltage
        self.text = f"{round(voltage, 1)}V"

    def move(self, pos):
        self.x, self.y = abs(pos[0] - self.width/2), abs(pos[1] - self.height/2)

    def draw(self, screen):
        # Render the text
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_x = (self.x + (self.width - text_surface.get_width()) // 2) + 10
        text_y = self.y + (self.height - text_surface.get_height()) // 2

        # Render the image
        image = pygame.image.load('images/Battery.png')
        image = pygame.transform.scale(image, (self.width, self.height))
        screen.blit(image, (self.x, self.y))
        screen.blit(text_surface, (text_x, text_y))

        # Draw left node
        left_circle_x = self.x - self.circle_radius - 8
        left_circle_y = self.y + self.height // 2
        pygame.draw.circle(screen, self.circle_color,
                           (left_circle_x, left_circle_y), self.circle_radius)

        # Draw right node
        right_circle_x = self.x + self.width + self.circle_radius + 8
        right_circle_y = self.y + self.height // 2
        pygame.draw.circle(screen, self.circle_color,
                           (right_circle_x, right_circle_y), self.circle_radius)

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()

        # Calculate node positions
        left_circle_x = self.x - self.circle_radius - 8
        left_circle_y = self.y + self.height // 2
        right_circle_x = self.x + self.width + self.circle_radius + 8
        right_circle_y = self.y + self.height // 2

        # Check if mouse is over left node
        left_dist = ((mouse_pos[0] - left_circle_x) ** 2 +
                     (mouse_pos[1] - left_circle_y) ** 2)
        left_clicked = left_dist <= self.circle_radius ** 2

        # Check if mouse is over right node
        right_dist = ((mouse_pos[0] - right_circle_x) ** 2 +
                      (mouse_pos[1] - right_circle_y) ** 2)
        right_clicked = right_dist <= self.circle_radius ** 2

        # Check for click events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if left_clicked:  # Click left node
                    return True
                elif right_clicked:  # Click right node
                    return True
                elif (self.x < mouse_pos[0] < self.x + self.width and
                      self.y < mouse_pos[1] < self.y + self.height):  # Click battery body
                    self.dragging = True
                    self.properties.visible = False
                    pos = round(mouse_pos[0]/GRID_SIZE)*GRID_SIZE, round(mouse_pos[1]/GRID_SIZE)*GRID_SIZE
                    self.move(pos)
                    return True
            elif event.button == 3:  # Right click
                if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
                    self.properties.visible = not self.properties.visible

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Released left click
                self.dragging = False

        elif event.type == pygame.MOUSEMOTION:  # Moving mouse
            if self.dragging:  # If dragging, then move the battery
                pos = round(mouse_pos[0]/GRID_SIZE)*20, round(mouse_pos[1]/GRID_SIZE)*GRID_SIZE
                self.move(pos)

        return False

    # This code is for the wire to call and get the nodes of this component, do not remove (unless you want to break something in which case go ahead).
    def get_node_positions(self):
        return {
            "left": (self.x - self.circle_radius - 8, self.y + self.height // 2),
            "right": (self.x + self.width + self.circle_radius + 8, self.y + self.height // 2)
        }


# Creates a window that allows the user to adjust the voltage of the battery
class BatteryProperties:
    def __init__(self, battery, screen, x=450, y=320):
        self.battery = battery
        self.current_voltage = battery.get_voltage()
        self.prev_valid_voltage = self.current_voltage
        self.screen = screen
        self.x = x
        self.y = y
        self.visible = False
        self.width = 380  # Width of the properties panel
        self.height = 80   # Height of the properties panel

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.DARK_GRAY = (150, 150, 150)
        self.PANEL_BG = (240, 240, 240)  # Slightly off-white for the panel
        self.BORDER_COLOR = (180, 180, 180)  # Light gray border

        # Font
        self.font = pygame.font.SysFont('Times New Roman', 20)

        # Panel background rectangle
        self.panel_rect = pygame.Rect(x, y, self.width, self.height)

        # Text input (positioned relative to panel)
        self.input_rect = pygame.Rect(x + 80, y + 35, 100, 32)
        self.input_text = str(self.current_voltage)
        self.active = False

        # Slider (positioned relative to panel)
        self.slider_rect = pygame.Rect(x + 205, y + 48, 150, 5)
        self.slider_handle_rect = pygame.Rect(0, y + 35, 15, 30)
        self.update_slider_handle()
        self.dragging = False

        # Exit button
        self.exit_rect = pygame.Rect(x+360, y, 15, 15)

    def move(self, x, y):
        self.x = x
        self.y = y

    def update_slider_handle(self):
        # Position handle based on current voltage (0-12V range)
        pos = (self.current_voltage / 12.0) * 150
        self.slider_handle_rect.x = self.x + 205 + pos - 12  # Center handle

    def handle_event(self, event):
        if not self.visible:
            return False  # Not visible, don't handle events

        # Check if event is inside our panel
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            if not self.panel_rect.collidepoint(event.pos):
                return False  # Event outside our panel

        # Text input handling
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

            if self.exit_rect.collidepoint(event.pos):
                self.visible = False

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
        return True  # Event was handled

    def handle_slider_drag(self, mouse_x):
        # Constrain to slider area
        mouse_x = max(self.slider_rect.left, min(mouse_x, self.slider_rect.right))
        self.current_voltage = ((mouse_x - self.slider_rect.left) / self.slider_rect.width) * 12
        self.current_voltage = round(self.current_voltage, 2)
        self.input_text = str(self.current_voltage)
        self.battery.set_voltage(self.current_voltage)
        self.prev_valid_voltage = self.current_voltage
        self.update_slider_handle()

    def update_from_text(self):
        try:
            new_voltage = float(self.input_text)
            if 0 <= new_voltage <= 12:
                self.current_voltage = new_voltage
                self.prev_valid_voltage = new_voltage
                self.battery.set_voltage(new_voltage)
                self.update_slider_handle()
            elif new_voltage < 0:
                self.current_voltage = 0
                self.prev_valid_voltage = 0
                self.battery.set_voltage(0)
                self.update_slider_handle()
            elif new_voltage > 12:
                self.current_voltage = 12
                self.prev_valid_voltage = 12
                self.battery.set_voltage(12)
                self.update_slider_handle()
        except ValueError:
            pass

    def draw(self):
        if not self.visible:
            return

        # Draw the background panel with border
        pygame.draw.rect(self.screen, self.PANEL_BG, self.panel_rect)
        pygame.draw.rect(self.screen, self.BORDER_COLOR, self.panel_rect, 2)

        # Draw title
        title = self.font.render("Battery properties:", True, self.BLACK)
        self.screen.blit(title, (self.x + 10, self.y + 5))

        # Draw voltage label
        voltage_label = self.font.render("Voltage", True, self.BLACK)
        self.screen.blit(voltage_label, (self.x + 10, self.y + 40))

        # Draw text input box
        color = self.BLACK if self.active else self.GRAY
        pygame.draw.rect(self.screen, self.WHITE, self.input_rect)  # White background for input
        pygame.draw.rect(self.screen, color, self.input_rect, 2)  # Border
        text_surface = self.font.render(self.input_text, True, self.BLACK)
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

        # Draw slider track
        pygame.draw.rect(self.screen, self.DARK_GRAY, self.slider_rect)

        # Draw slider handle with nice appearance
        handle_color = self.WHITE
        pygame.draw.rect(self.screen, handle_color, self.slider_handle_rect, border_radius=3)
        pygame.draw.rect(self.screen, self.BLACK, self.slider_handle_rect, 1, border_radius=3)

        # Draw text
        text_surface = self.font.render("X", True, (0, 0, 0))
        self.screen.blit(text_surface, (self.x+360, self.y))