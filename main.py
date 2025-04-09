import pygame as pg
from random import random
from pygame import mixer

from components.Buttons import Button
from components.battery import Battery
from components.wire import Wire

# pygame setup


def main():
    # Your program's code goes here
    pg.init()
    screen = pg.display.set_mode((1280, 720))
    clock = pg.time.Clock()
    running = True
    dt = 0

    # Wire Variables
    wires = []
    drawing_wire = False
    wire_start = None

    def PushButton():
        print('button pushed')

    def PushBattery():
        print('battery pushed')

    button = Button(680, 500, 140, 52, "Button 1", 32, (45, 45, 45), (100, 100, 100), (100, 100, 100), (0, 0, 0),PushButton)
    ngButton = Button(680, 580, 140, 52, "Button 2", 32, (45, 45, 45), (100, 100, 100), (100, 100, 100), (0, 0, 0), PushButton)
    battery = Battery(x=100, y=100, width=100, height=40, callback=PushBattery)
    hI = 0
    rollTime = 0

    while running:
        screen.fill((30,30,30))
        # button event
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            button.handle_event(event)
            ngButton.handle_event(event)
            battery.handle_event(event)

            # Kory -- Wire start and end location obtain code
            # Wire Code -------------------------------------------------------------------------------
            if event.type == pg.MOUSEBUTTONDOWN:
                wire_start = pg.mouse.get_pos() #wire_start = breadboard.getLocation(AtLocationOfClick)
                #wire_component1 = breadboard.getComponentNode(AtLocationOfClick)
                drawing_wire = True

            elif event.type == pg.MOUSEBUTTONUP and drawing_wire:
                wire_end = pg.mouse.get_pos() #wire_end = breadboard.getLocation(AtLocationOfClick)
                # wire_component2 = breadboard.getComponentNode(AtLocationOfClick)
                wires.append(Wire(wire_start, wire_end)) #wires.append(Wire(wire_start, wire_component1, wire_end, wire_component2))
                print(f"Wire from {wire_start} to {wire_end}")
                drawing_wire = False
                wire_start = None
            # Wire Code---------------------------------------------------------------------------------

            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                True
                #STUFF HERE

        button.draw(screen)
        ngButton.draw(screen)
        battery.draw(screen)

        # Kory -- Wire Draw
        # Draw Wires -------------------------------------------------------------------------
        for wire in wires:
            wire.draw(screen)

        if drawing_wire and wire_start:
            current_pos = pg.mouse.get_pos()
            pg.draw.line(screen, (200, 200, 200), wire_start, current_pos, 2)
        # Draw Wires -------------------------------------------------------------------------


        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()