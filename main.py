import pygame as pg
from random import random
from pygame import mixer

from components.Buttons import Button
from components.battery import Battery
from components.square import Square
from components.wire import Wire
from components.gates import Gates

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

    # gates assets
    gate_sprite = pg.image.load("images/and or not gates f.png").convert_alpha()
    gate_width = gate_sprite.get_width() // 3
    gap = 20

    and_gate = Gates("AND", "G1", 220, 100, gate_sprite)
    or_gate = Gates("OR", "G2", 220 + gate_width + gap, 100, gate_sprite)
    not_gate = Gates("NOT", "G3", 220 + (gate_width + gap) * 2, 100, gate_sprite)
    gates = [and_gate, or_gate, not_gate]




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

        # KWALPOLE---------------------------------------------------------
        # create list of squares 3600
        square_list = []
        MAX_SQUARES = 3600

        pos_x = 0
        pos_y = 0
        square_num = 0

        # while loop creates all squares and adds them to list, draw function is handled during object initialization
        # the creation of these squares needs to happen before all other draw functions, and after screen fill
        while square_num < MAX_SQUARES:
            square_obj = Square(screen, pos_x, pos_y)
            square_list.append(square_obj)

            square_num += 1
            pos_x += 16

            if pos_x == 1280:
                pos_y += 16
                pos_x = 0

        # ------------------------------------------------------------------

        # button event
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            button.handle_event(event)
            ngButton.handle_event(event)
            battery.handle_event(event)

            # Kory -- Wire Functionality
            # This code block is the engine for detecting mouse events to start creating a wire. --------------
            if event.type == pg.MOUSEBUTTONDOWN:
                wire_start = round(pg.mouse.get_pos()[0]/GRID_SIZE)*GRID_SIZE, round(pg.mouse.get_pos()[1]/GRID_SIZE)*GRID_SIZE
                drawing_wire = True

            elif event.type == pg.MOUSEBUTTONUP and drawing_wire:
                wire_end = round(pg.mouse.get_pos()[0]/GRID_SIZE)*GRID_SIZE, round(pg.mouse.get_pos()[1]/GRID_SIZE)*GRID_SIZE
                wires.append(Wire(wire_start, wire_end))
                print(f"Wire from {wire_start} to {wire_end}")
                drawing_wire = False
                wire_start = None
            # --------------------------------------------------------------------------------------------------



            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                True
                #STUFF HERE

            #gates info
            for gate in gates:
                gate.handle_event(event)

        for gate in gates:
            gate.draw(screen)

        button.draw(screen)
        ngButton.draw(screen)
        battery.draw(screen)




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

