import pygame

class Switch:
    def __init__(self, name="Switch", initial_state=False):
        self.name = name
        self.state = initial_state

    def toggle(self):
        self.state = not self.state

    def turn_on(self):
        self.state = True

    def turn_off(self):
        self.state = False

    def is_on(self):
        return self.state

    def __repr__(self):
        return f"<{self.name}: {'ON' if self.state else 'OFF'}>"