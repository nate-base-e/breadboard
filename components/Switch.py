import pygame

class Switch:
    #initializing the switch
    def __init__(self,x, y, on_image_path, off_image_path, name="Switch", initial_state=False):
        self.name = name
        self.state = initial_state
        self.x = x
        self.y = y

        self.on_image = pygame.image.load(on_image_path)
        self.off_image = pygame.image.load(off_image_path)

        self.rect = self.on_image.get_rect()
        self.rect.topleft = (x, y)

    #toggle the switch on or off
    def toggle(self):
        self.state = not self.state
        return self.state

    #turn switch on
    def turn_on(self):
        self.state = True

    #turn off switch
    def turn_off(self):
        self.state = False

    #checks what state the switch is on
    def is_on(self):
        return self.state

    #draw the surface on the provided surface
    def draw(self, surface):
        if self.state:
            surface.blit(self.on_image, self.rect)
        else:
            surface.blit(self.off_image, self.rect)

    #handle mouse events on toggling the switch
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.toggle()
                return True
        return False

    #shows what the switch is at
    def __repr__(self):
        return f"<{self.name}: {'ON' if self.state else 'OFF'}>"