import pygame

class Switch:
    #initializing the switch
    def __init__(self, name="Switch", initial_state=False):
        self.name = name
        self.state = initial_state

    #toggle the switch on or off
    def toggle(self):
        self.state = not self.state

    #turn switch on
    def turn_on(self):
        self.state = True

    #turn off switch
    def turn_off(self):
        self.state = False

    #checks what state the switch is on
    def is_on(self):
        return self.state

    #shows what the switch is at
    def __repr__(self):
        return f"<{self.name}: {'ON' if self.state else 'OFF'}>"