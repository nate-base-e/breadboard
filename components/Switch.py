import pygame

class Switch:
    def __init__(self, x, y, on_image_path, off_image_path, name="Switch", initial_state=False):
        self.name = name
        self.state = initial_state
        self.x = x
        self.y = y

        self.on_image = pygame.transform.scale_by(on_image_path, 0.125)
        self.off_image = pygame.transform.scale_by(off_image_path, 0.125)

        self.rect = self.on_image.get_rect()
        self.rect.topleft = (x, y)

        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

        self.to_delete = False
        self.is_template = False

        self.mouse_down_pos = None
        self.drag_threshold = 5

        self.circle_radius = 4
        self.circle_color = (0, 255, 0)

    def toggle(self):
        self.state = not self.state
        return self.state

    def turn_on(self):
        self.state = True

    def turn_off(self):
        self.state = False

    def is_on(self):
        return self.state

    def delete(self):
        self.to_delete = True

    def draw(self, surface):
        image = self.on_image if self.state else self.off_image
        surface.blit(image, self.rect)

        # Get image dimensions
        width = self.on_image.get_width()
        height = self.on_image.get_height()

        # Calculate top node
        top_circle_x = self.x + width // 2
        top_circle_y = self.y - self.circle_radius - 8
        pygame.draw.circle(surface, self.circle_color,
                           (top_circle_x, top_circle_y), self.circle_radius)

        # Calculate bottom node
        bottom_circle_x = self.x + width // 2
        bottom_circle_y = self.y + height + self.circle_radius + 8
        pygame.draw.circle(surface, self.circle_color,
                           (bottom_circle_x, bottom_circle_y), self.circle_radius)

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()

        width = self.on_image.get_width()
        height = self.on_image.get_height()

        # Calculate top and bottom node positions
        top_circle_x = self.x + width // 2
        top_circle_y = self.y - self.circle_radius - 8
        bottom_circle_x = self.x + width // 2
        bottom_circle_y = self.y + height + self.circle_radius + 8

        # Check if mouse is over top node
        top_dist = ((mouse_pos[0] - top_circle_x) ** 2 +
                    (mouse_pos[1] - top_circle_y) ** 2)
        top_clicked = top_dist <= self.circle_radius ** 2

        # Check if mouse is over bottom node
        bottom_dist = ((mouse_pos[0] - bottom_circle_x) ** 2 +
                       (mouse_pos[1] - bottom_circle_y) ** 2)
        bottom_clicked = bottom_dist <= self.circle_radius ** 2

        if self.is_template:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.mouse_down_pos = event.pos
                mouse_x, mouse_y = event.pos
                self.offset_x = self.rect.x - mouse_x
                self.offset_y = self.rect.y - mouse_y
                return "selected"

            elif event.button == 3 and self.rect.collidepoint(event.pos):
                self.delete()
                return "deleted"

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.dragging:
                    self.dragging = False
                    self.mouse_down_pos = None
                    return "dropped"
                elif self.mouse_down_pos and self.rect.collidepoint(event.pos):
                    mouse_x, mouse_y = event.pos
                    initial_x, initial_y = self.mouse_down_pos
                    distance = ((mouse_x - initial_x) ** 2 + (mouse_y - initial_y) ** 2) ** 0.5
                    if distance <= self.drag_threshold:
                        self.toggle()
                        self.mouse_down_pos = None
                        return "toggled"
                self.mouse_down_pos = None

        elif event.type == pygame.MOUSEMOTION:
            if self.mouse_down_pos:
                mouse_x, mouse_y = event.pos
                initial_x, initial_y = self.mouse_down_pos
                distance = ((mouse_x - initial_x) ** 2 + (mouse_y - initial_y) ** 2) ** 0.5
                if distance > self.drag_threshold:
                    self.dragging = True

            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.rect.x = mouse_x + self.offset_x
                self.rect.y = mouse_y + self.offset_y
                self.x = self.rect.x
                self.y = self.rect.y
                return "dragging"

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE and self.rect.collidepoint(pygame.mouse.get_pos()):
                self.delete()
                return "deleted"

        return False

    # This code is for the wire to call and get the nodes of this component, do not remove (unless you want to break something in which case go ahead).
    def get_node_positions(self):
        width = self.on_image.get_width()
        height = self.on_image.get_height()
        return {
            "left": (self.x - self.circle_radius - 8, self.y + height // 2),
            "right": (self.x + width + self.circle_radius + 8, self.y + height // 2)
        }

    def __repr__(self):
        return f"<{self.name}: {'ON' if self.state else 'OFF'}>"
