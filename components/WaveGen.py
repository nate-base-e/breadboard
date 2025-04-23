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