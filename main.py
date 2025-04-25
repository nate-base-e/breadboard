import pygame as pg
from random import random
from pygame import mixer

from components.Switch import Switch
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

# This checks for a node on the component clicked
def get_clicked_node(components, mouse_pos, radius=10):
    for comp in components:
        if hasattr(comp, 'get_node_positions'):
            for node_name, pos in comp.get_node_positions().items():
                dist_sq = (mouse_pos[0] - pos[0])**2 + (mouse_pos[1] - pos[1])**2
                if dist_sq <= radius**2:
                    return comp, node_name, pos
    return None, None, None

wire_start_info = None



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

    #switch assets
    switch_on_img = pg.image.load("images/Switch-On.png").convert_alpha()
    switch_off_img = pg.image.load("images/Switch-Off.png").convert_alpha()

    #template switch for top bar
    template_switch = Switch(650, 25, switch_on_img, switch_off_img, "TEMPLATE_SWITCH", False)
    template_switch.is_template = True

    # Batteries
    batteries = []  # Allows for multiple batteries
    batteries.append(Battery(x=30, y=0, width=100, height=40, screen=screen))

    lights = []
    lights.append(Lights(100,100,off_img,on_img))

    #List for active switches
    switches = []

    #Flag to track if creating new switch
    creating_new_switch = False
    new_switch = None

    resistor = Resistor(x=300, y=300)
    fuse = Fuse(500, 300)  # adjust position as needed
    wavegen = WaveGen("images/WaveGen.jpg", (600, 100))
    hI = 0
    rollTime = 0

    # ALL COMPONENTS NEED TO BE INDEXED WITHIN THIS LIST
    components = [ and_gate, or_gate, not_gate, resistor, fuse, WaveGen, switches]
    components.extend(batteries)  # Adds all batteries to components
    components.extend(lights)

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

            resistor.handle_event(event)
            fuse.handle_event(event)
            wavegen.handle_event(event)

            #handle template switch for creating new instances
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if template_switch.rect.collidepoint(event.pos):
                    creating_new_switch = True
                    mouse_x, mouse_y = event.pos
                    new_switch = Switch(mouse_x, mouse_y, switch_on_img, switch_off_img,f"S{len(switches)+1}", False)
                    new_switch.dragging = True
                    new_switch.offset_x = 0
                    new_switch.offset_y = 0
                    new_switch.mouse_down_pos = event.pos

            elif event.type == pg.MOUSEMOTION and creating_new_switch and new_switch:
                #update pos while dragging new switch
                mouse_x, mouse_y = event.pos
                new_switch.rect.x = mouse_x + new_switch.offset_x
                new_switch.rect.y = mouse_y + new_switch.offset_y
                new_switch.x = new_switch.rect.x
                new_switch.y = new_switch.rect.y

            elif event.type == pg.MOUSEBUTTONUP and event.button == 1 and creating_new_switch and new_switch:
                #Finish creating the new switch
                if creating_new_switch and new_switch:
                    creating_new_switch = False
                    new_switch.dragging = False

                    if new_switch.rect.y > 75:
                        switches.append(new_switch)
                        components.append(new_switch)

                    new_switch = None

                    # Release any existing switches that are being dragged
                for switch in switches:
                    if switch.dragging:
                        switch.dragging = False

            #handle existing switches
            for switch in switches[:]:
                result = switch.handle_event(event)
                if result == "deleted":
                    switches.remove(switch)
                    components.remove(switch)

            #gates info
            for gate in gates:
                gate.handle_event(event)

            # Batteries
            for battery in batteries:
                battery.handle_event(event)
                if battery.properties.visible:
                    battery.properties.handle_event(event)

            for light in lights:
                light.handle_event(event)

            # Kory -- Wire Functionality
            # This code block is the engine for detecting mouse events to start creating a wire. --------------
            if not is_any_component_dragging(components):
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 3:  # Right-click
                        mouse_pos = pg.mouse.get_pos()
                        for wire in wires[:]:  # copy to avoid modifying list while iterating
                            if wire.is_hovered(mouse_pos):
                                wires.remove(wire)
                                print("Wire removed")
                                break

                    mouse_pos = pg.mouse.get_pos()
                    comp, node_name, pos = get_clicked_node(components, mouse_pos)
                    if comp:
                        wire_start_info = (comp, node_name, pos)
                        drawing_wire = True

                elif event.type == pg.MOUSEBUTTONUP and drawing_wire:
                    mouse_pos = pg.mouse.get_pos()
                    comp, node_name, pos = get_clicked_node(components, mouse_pos)
                    if comp and wire_start_info:
                        start_comp, start_node, start_pos = wire_start_info
                        if comp == start_comp and node_name == start_node:
                            print("Cannot connect a wire to the same node on both ends.")
                        else:
                            wires.append(Wire(start_pos, pos, start_comp, comp, start_node, node_name))
                            print(f"Wire from {start_node} of {start_comp} to {node_name} of {comp}")
                    drawing_wire = False
                    wire_start_info = None
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

        for light in lights:
            light.draw(screen)

        resistor.draw(screen)
        fuse.draw(screen)
        wavegen.draw(screen)


        #draw template switch
        template_switch.draw(screen)

        #draw new switch being created
        if creating_new_switch and new_switch:
            new_switch.draw(screen)

        #draw existing switches
        for switch in switches:
            switch.draw(screen)


        # Draw wires
        for wire in wires:
            wire.draw(screen)

        if drawing_wire and wire_start_info and not is_any_component_dragging(components):
            _, _, start_pos = wire_start_info
            current_pos = round(pg.mouse.get_pos()[0] / GRID_SIZE) * GRID_SIZE, round(
                pg.mouse.get_pos()[1] / GRID_SIZE) * GRID_SIZE
            pg.draw.line(screen, (200, 200, 200), start_pos, current_pos, 2)


        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()