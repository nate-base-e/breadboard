# wire.py

import pygame as pg
import math
import os

class Wire:
    wire_start_img = None
    wire_middle_img = None
    wire_end_img = None

    def __init__(self, start_pos, end_pos, start_comp, end_comp, start_node, end_node):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.start_comp = start_comp
        self.end_comp = end_comp
        self.start_node = start_node
        self.end_node = end_node

        if Wire.wire_start_img is None:
            current_dir = os.path.dirname(__file__)
            image_path = os.path.join(current_dir, "..", "images", "WireSprite.png")
            try:
                full_img = pg.image.load(image_path).convert_alpha()

                start_width = 100
                end_width = 100
                middle_width = full_img.get_width() - start_width - end_width
                height = full_img.get_height()

                Wire.wire_start_img = full_img.subsurface((0, 0, start_width, height))
                Wire.wire_middle_img = full_img.subsurface((start_width, 0, middle_width, height))
                Wire.wire_end_img = full_img.subsurface((start_width + middle_width, 0, end_width, height))

            except Exception as e:
                print("Failed to load/slice wire sprite:", e)

    def draw(self, screen):
        if not all([Wire.wire_start_img, Wire.wire_middle_img, Wire.wire_end_img]):
            # fallback to a simple line
            pg.draw.line(screen, (200, 0, 0), self.start_pos, self.end_pos, 3)
            return

        dx = self.end_pos[0] - self.start_pos[0]
        dy = self.end_pos[1] - self.start_pos[1]
        angle = math.atan2(dy, dx)
        length = math.hypot(dx, dy)

        total_height = 12  # wire thickness
        start_scaled = pg.transform.smoothscale(Wire.wire_start_img, (10, total_height))
        end_scaled = pg.transform.smoothscale(Wire.wire_end_img, (10, total_height))

        middle_tile_width = 8
        middle_scaled = pg.transform.smoothscale(Wire.wire_middle_img, (middle_tile_width, total_height))
        middle_count = max(1, int((length - 20) / middle_tile_width))

        wire_surface = pg.Surface((int(length), total_height), pg.SRCALPHA)
        wire_surface.blit(start_scaled, (0, 0))
        for i in range(middle_count):
            wire_surface.blit(middle_scaled, (10 + i * middle_tile_width, 0))
        wire_surface.blit(end_scaled, (10 + middle_count * middle_tile_width, 0))

        rotated_wire = pg.transform.rotate(wire_surface, -math.degrees(angle))
        center_x = (self.start_pos[0] + self.end_pos[0]) // 2
        center_y = (self.start_pos[1] + self.end_pos[1]) // 2
        rotated_rect = rotated_wire.get_rect(center=(center_x, center_y))

        screen.blit(rotated_wire, rotated_rect.topleft)



# this fuction is for when a component wants to call the other end of the wire
    def get_other_end(self, comp, node):
        """Returns (other_comp, other_node) if the input matches one end of the wire.
        Otherwise, returns None."""
        if comp == self.start_comp and node == self.start_node:
            return self.end_comp, self.end_node
        elif comp == self.end_comp and node == self.end_node:
            return self.start_comp, self.start_node
        else:
            return None


# this code checks for when the wire is being hovered over
    def is_hovered(self, mouse_pos, threshold=5):
        # Distance from point to line segment
        x1, y1 = self.start_pos
        x2, y2 = self.end_pos
        px, py = mouse_pos

        dx = x2 - x1
        dy = y2 - y1
        if dx == dy == 0:
            return (px - x1) ** 2 + (py - y1) ** 2 < threshold ** 2

        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy

        dist_sq = (px - closest_x) ** 2 + (py - closest_y) ** 2
        return dist_sq <= threshold ** 2

    # added by omar for testing
    # this is for passing power from battery to resistor using the wire
    # used for Omar_Final.py test file
    # Omar update for wire-based power simulation
    def transfer_power(self):
        # Battery to Resistor
        if hasattr(self.start_comp, 'get_voltage') and hasattr(self.end_comp, 'update_voltage'):
            voltage = self.start_comp.get_voltage()
            self.end_comp.update_voltage(voltage)

        # Resistor to Light
        elif hasattr(self.start_comp, 'get_voltage') and hasattr(self.end_comp, 'set_voltage'):
            voltage = self.start_comp.get_voltage()
            self.end_comp.set_voltage(voltage)

        # Reverse connections
        elif hasattr(self.end_comp, 'get_voltage') and hasattr(self.start_comp, 'update_voltage'):
            voltage = self.end_comp.get_voltage()
            self.start_comp.update_voltage(voltage)

        elif hasattr(self.end_comp, 'get_voltage') and hasattr(self.start_comp, 'set_voltage'):
            voltage = self.end_comp.get_voltage()
            self.start_comp.set_voltage(voltage)

    #this code dosent quite work without some uniform input and output for each compoenent but this code could work

    #these two funcitons go inside of main but not in the main game loop
    # def build_circuit_graph(wires):
    #     graph = {}
    #     for wire in wires:
    #         graph.setdefault(wire.start_comp, []).append(wire.end_comp)
    #         graph.setdefault(wire.end_comp, []).append(wire.start_comp)
    #     return graph
    #
    # def propagate_signal(graph, start_comp, value, visited=None):
    #     if visited is None:
    #         visited = set()
    #
    #     visited.add(start_comp)
    #
    #     for neighbor in graph.get(start_comp, []):
    #         if neighbor in visited:
    #             continue
    #
    #         if hasattr(neighbor, "add_input"):
    #             neighbor.add_input(value)
    #         elif hasattr(neighbor, "set_input"):
    #             neighbor.set_input(value)
    #
    #         output = value
    #         if hasattr(neighbor, "get_output"):
    #             output = neighbor.get_output()
    #
    #         propagate_signal(graph, neighbor, output, visited)
    #
    #
    #     #this code goes in the main game loop
    #     if event.type == pg.KEYDOWN:
    #         if event.key == pg.K_c:  # Press 'C' key
    #             circuit_graph = build_circuit_graph(wires)
    #     if event.type == pg.KEYDOWN:
    #         if event.key == pg.K_v:
    #             walk_circuit(circuit_graph, battery)