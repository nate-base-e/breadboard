import pygame

class WaveGen:
    def __init__(self, image_path, position=(0, 0)):
        # Load and scale the wave generator image
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (60, 60))

        # Set the image's position and get the rectangle object for collisions
        self.rect = self.image.get_rect(topleft=position)

        # Dragging state
        self.dragging = False

        # Voltage output of the wave generator
        self.voltage = 1.5

    def draw(self, screen):
        # Draw the component on the screen at its current position
        screen.blit(self.image, self.rect.topleft)

    def handle_event(self, event):
        # When mouse button is pressed down
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if mouse is over the component
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                mouse_x, mouse_y = event.pos
                offset_x = self.rect.x - mouse_x
                offset_y = self.rect.y - mouse_y
                self.offset = (offset_x, offset_y)

        # When mouse button is released
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                # Check if it's placed on the breadboard area
                if self.rect.top > 200:
                    print(f"WaveGen placed on breadboard at {self.rect.topleft}")
                else:
                    print(f"WaveGen placed in upper container at {self.rect.topleft}")

        # When mouse is moving and dragging is True
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.rect.x = mouse_x + self.offset[0]
                self.rect.y = mouse_y + self.offset[1]

    def get_voltage(self):
        # Return the voltage output of the component
        return self.voltage






################## updated test function ##########################
class TesterComponent:
    def __init__(self, display):
        self.display = display
        self.test_cases = {}  # Changed from list of tuples to dictionary
        self.test_names = []
        self.test_index = 0
        self.completed = False

    def add_test(self, test_label, component):
        self.test_cases[test_label] = component
        self.test_names.append(test_label)

    def execute_current_test(self):
        if self.completed or not self.test_names:
            return

        current_label = self.test_names[self.test_index]
        current_component = self.test_cases[current_label]

        self.display.fill((50, 50, 50))  # Fill background

        if hasattr(current_component, 'draw'):
            current_component.draw(self.display)

        # Display the test name
        font = pg.font.Font(None, 36)
        test_text = font.render(f"Running Test: {current_label}", True, (255, 255, 255))
        self.display.blit(test_text, (20, 20))

    def advance_test(self):
        self.test_index += 1
        if self.test_index >= len(self.test_names):
            self.completed = True

    def restart_tests(self):
        self.test_index = 0
        self.completed = False


# Instantiate the tester with the screen
tester = TesterComponent(screen)

# Register test cases
tester.add_test("Battery", batteries[0])
tester.add_test("Wire", Wire((100, 100), (200, 200), None, None, "start", "end"))
tester.add_test("Light", lights[0])

##########test section #############
# Only the battery works for now
tester.execute_current_test()

# Check for key press to advance
# keys = pg.key.get_pressed()
if keys[pg.K_SPACE]:  # SPACE advances to next test
    tester.advance_test()