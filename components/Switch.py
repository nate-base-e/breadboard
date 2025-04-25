import pygame


class Switch:
    # initializing the switch
    def __init__(self, x, y, on_image_path, off_image_path, name="Switch", initial_state=False):
        self.name = name
        self.state = initial_state
        self.x = x
        self.y = y

        self.on_image = pygame.transform.scale_by(on_image_path, .25)
        self.off_image = pygame.transform.scale_by(off_image_path,.25)

        self.rect = self.on_image.get_rect()
        self.rect.topleft = (x, y)

        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

        self.to_delete = False
        self.is_template = False  # Flag to mark template switches

        self.mouse_down_pos = None
        self.drag_threshold = 5

    # toggle the switch on or off
    def toggle(self):
        self.state = not self.state
        return self.state

    # turn switch on
    def turn_on(self):
        self.state = True

    # turn off switch
    def turn_off(self):
        self.state = False

    # checks what state the switch is on
    def is_on(self):
        return self.state

    def delete(self):
        self.to_delete = True

    # draw the surface on the provided surface
    def draw(self, surface):
        if self.state:
            surface.blit(self.on_image, self.rect)
        else:
            surface.blit(self.off_image, self.rect)

    # handle mouse events on toggling the switch
    def handle_event(self, event):
        # For template switches, we handle creation differently in the main loop
        if self.is_template:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left Mouse button
                if self.rect.collidepoint(event.pos):
                    # Store init position for drag detection
                    self.mouse_down_pos = event.pos
                    # calc offset for smooth dragging
                    mouse_x, mouse_y = event.pos
                    self.offset_x = self.rect.x - mouse_x
                    self.offset_y = self.rect.y - mouse_y
                    return "selected"

            elif event.button == 3:  # right mouse button
                if self.rect.collidepoint(event.pos):
                    self.delete()
                    return "deleted"

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # left mouse button
                if self.dragging:
                    # end dragging
                    self.dragging = False
                    return "dropped"
                elif self.mouse_down_pos and self.rect.collidepoint(event.pos):
                    # mouse released at same position, toggle switch
                    mouse_x, mouse_y = event.pos
                    initial_x, initial_y = self.mouse_down_pos
                    distance = ((mouse_x - initial_x) ** 2 + (mouse_y - initial_y) ** 2) ** 0.5

                    if distance <= self.drag_threshold:
                        self.toggle()
                        return "toggled"

                self.mouse_down_pos = None

        elif event.type == pygame.MOUSEMOTION:
            if self.mouse_down_pos and not self.dragging:
                # check if moved enough to start dragging
                mouse_x, mouse_y = event.pos
                initial_x, initial_y = self.mouse_down_pos
                distance = ((mouse_x - initial_x) ** 2 + (mouse_y - initial_y) ** 2) ** 0.5

                if distance > self.drag_threshold:
                    self.dragging = True

            if self.dragging:
                # update pos while dragging
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

    # shows what the switch is at
    def __repr__(self):
        return f"<{self.name}: {'ON' if self.state else 'OFF'}>"