import pygame as pg
from random import random
from pygame import mixer

from components.Buttons import Button
from components.battery import Battery
from components.wire import Wire

# pygame setup

GRID_SIZE = 20

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

    def PushBattery(part, x, y):
        if part == "body":  # Pushing the body of the battery
            pos = round(x/GRID_SIZE)*GRID_SIZE, round(y/GRID_SIZE)*GRID_SIZE  # Grid movement
            battery.move(pos)

    button = Button(680, 500, 140, 52, "Button 1", 32, (45, 45, 45), (100, 100, 100), (100, 100, 100), (0, 0, 0),PushButton)
    ngButton = Button(680, 580, 140, 52, "Button 2", 32, (45, 45, 45), (100, 100, 100), (100, 100, 100), (0, 0, 0), PushButton)
    battery = Battery(x=30, y=0, width=100, height=40, callback=PushBattery)
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

            if event.type == pg.MOUSEBUTTONDOWN:
                wire_start = round(pg.mouse.get_pos()[0]/GRID_SIZE)*GRID_SIZE, round(pg.mouse.get_pos()[1]/GRID_SIZE)*GRID_SIZE
                drawing_wire = True

            elif event.type == pg.MOUSEBUTTONUP and drawing_wire:
                wire_end = round(pg.mouse.get_pos()[0]/20)*20, round(pg.mouse.get_pos()[1]/20)*20
                wires.append(Wire(wire_start, wire_end))
                print(f"Wire from {wire_start} to {wire_end}")
                drawing_wire = False
                wire_start = None

            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                True
                #STUFF HERE

        button.draw(screen)
        ngButton.draw(screen)
        battery.draw(screen)

        #KWALPOLE---------------------------------------------------------
        #create list of squares 3600

        #for loop of drawing each square in list

        #------------------------------------------------------------------


        # Draw wires
        for wire in wires:
            wire.draw(screen)

        if drawing_wire and wire_start:
            current_pos = round(pg.mouse.get_pos()[0]/GRID_SIZE)*GRID_SIZE, round(pg.mouse.get_pos()[1]/GRID_SIZE)*GRID_SIZE
            pg.draw.line(screen, (200, 200, 200), wire_start, current_pos, 2)


        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()