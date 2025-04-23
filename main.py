import pygame as pg
from random import random
from pygame import mixer

from components.battery import Battery
from components.square import Square
from components.wire import Wire
from components.gates import Gates
from components.lights import Lights
from components.Resistor import Resistor
from components.fuse import Fuse
from components.WaveGen import WaveGen

GRID_SIZE = 20
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


# This checks if any component that exists is being dragged. All components should return if not being dragged "self.dragging = False"
def is_any_component_dragging(components):
    return any(getattr(comp, 'dragging', False) for comp in components)



def main():
    # Your program's code goes here
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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

    # lights assets
    on_img = pg.image.load("images/onled.png").convert_alpha()
    off_img = pg.image.load("images/offled.png").convert_alpha()

    # Batteries
    batteries = []  # Allows for multiple batteries
    batteries.append(Battery(x=30, y=0, width=100, height=40, screen=screen))


    resistor = Resistor(x=300, y=300)
    led = Lights(100,100,off_img,on_img)
    fuse = Fuse(500, 300)  # adjust position as needed
    wavegen = WaveGen("images/WaveGen.jpg", (600, 100))
    hI = 0
    rollTime = 0

    # ALL COMPONENTS NEED TO BE INDEXED WITHIN THIS LIST
    components = [led,and_gate,or_gate,not_gate,resistor,fuse, WaveGen]
    components.extend(batteries)  # Adds all batteries to components

    while running:
        screen.fill((30, 30, 30))

        # Square grid
        square_list = []
        #Keegan
        #MAX_SQUARES now changes according do SCREEN_WIDTH and SCREEN_HEIGHT
        MAX_SQUARES = (SCREEN_WIDTH/GRID_SIZE) * (SCREEN_HEIGHT/GRID_SIZE)
        #------------------------------------------------------------------
        pos_x = 0
        pos_y = 0
        square_num = 0

        while square_num < MAX_SQUARES:
            square_obj = Square(screen, pos_x, pos_y)
            square_list.append(square_obj)

            square_num += 1
            pos_x += GRID_SIZE

            if pos_x == SCREEN_WIDTH:
                pos_y += GRID_SIZE
                pos_x = 0


        # Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            led.handle_event(event)
            resistor.handle_event(event)
            fuse.handle_event(event)
            wavegen.handle_event(event)


            #gates info
            for gate in gates:
                gate.handle_event(event)

            # Batteries
            for battery in batteries:
                battery.handle_event(event)
                if battery.properties.visible:
                    battery.properties.handle_event(event)

            # Kory -- Wire Functionality
            # This code block is the engine for detecting mouse events to start creating a wire. --------------
            if not is_any_component_dragging(components):
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
            #fugeeeeeeee


            #fugeeeeeeeeee

            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                pass


        # more gate info
        for gate in gates:
            gate.draw(screen)

        for battery in batteries:
            battery.draw(screen)
            if battery.properties.visible:
                battery.properties.draw()

        led.draw(screen)
        resistor.draw(screen)
        fuse.draw(screen)
        wavegen.draw(screen)




        # Draw wires
        for wire in wires:
            wire.draw(screen)

        if drawing_wire and wire_start and not is_any_component_dragging(components):
            current_pos = round(pg.mouse.get_pos()[0]/GRID_SIZE)*GRID_SIZE, round(pg.mouse.get_pos()[1]/GRID_SIZE)*GRID_SIZE
            pg.draw.line(screen, (200, 200, 200), wire_start, current_pos, 2)


        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()