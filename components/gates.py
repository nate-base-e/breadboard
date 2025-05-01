# dcaclab.com
import pygame as pg

class Gates:
    def __init__(self, gateType, gateID, x, y, image):
        self.gate_id = gateID
        self.gate_type = gateType.upper()  # AND, OR, NOT

        # Display properties
        self.x = x
        self.y = y
        self.image = image
        self.scale_factor = 0.5  # 50% smaller

        full_width = self.image.get_width()
        full_height = self.image.get_height()
        gate_width = int((full_width // 3) * self.scale_factor)
        gate_height = int(full_height * self.scale_factor)
        self.rect = pg.Rect(x, y, gate_width, gate_height)
        self.dragging = False

        # Dragging offsets
        self.offset_x = 0
        self.offset_y = 0

        # Logic processing
        self.inputs = []  # list of input values (0 or 1)
        self.output_val = None  # cached output after eval

        # Determine which part of the sprite sheet to use
        self.sprite_index = {"AND": 0, "OR": 1, "NOT": 2}.get(self.gate_type, 0)

        # Node variables
        self.circle_radius = 4
        self.circle_color = (0, 255, 0)  # green nodes

        self.update_nodes()

        self.voltage = False

    def update_nodes(self):
        self.input_nodes = []

        node_offset = 8  # distance from gate edge outward

        if self.gate_type == "NOT":
            self.input_nodes.append((self.rect.left - node_offset, self.rect.centery))
        else:
            self.input_nodes.append((self.rect.left - node_offset, self.rect.top + self.rect.height * 0.25))
            self.input_nodes.append((self.rect.left - node_offset, self.rect.bottom - self.rect.height * 0.25))

        self.output_node = (self.rect.right + node_offset, self.rect.centery)

    def set_inputs(self, *inputs):
        self.inputs = inputs

    def eval(self):
        if self.gate_type == "AND":
            return int(all(self.inputs))
        elif self.gate_type == "OR":
            return int(any(self.inputs))
        elif self.gate_type == "NOT":
            if len(self.inputs) != 1:
                raise ValueError("NOT gate must have exactly one input")
            return int(not self.inputs[0])
        else:
            raise ValueError(f"Unknown gate type: {self.gate_type}")

    def output(self):
        self.output_val = self.eval()
        return self.output_val

    def draw(self, surface):
        # Draw the gate sprite first
        full_width = self.image.get_width()
        full_height = self.image.get_height()
        original_gate_width = full_width // 3

        crop_left = 2
        crop_right = 2
        src_x = self.sprite_index * original_gate_width + crop_left
        src_rect = pg.Rect(src_x, 0, original_gate_width - crop_left - crop_right, full_height)

        # Crop and scale the gate image
        gate_image = pg.Surface((src_rect.width, src_rect.height), pg.SRCALPHA)
        gate_image.blit(self.image, (0, 0), area=src_rect)
        scaled_width = int((original_gate_width - crop_left - crop_right) * self.scale_factor)
        scaled_height = int(full_height * self.scale_factor)
        gate_image = pg.transform.smoothscale(gate_image, (scaled_width, scaled_height))

        surface.blit(gate_image, self.rect)

        # Draw the nodes on top
        mouse_pos = pg.mouse.get_pos()

        for pos in self.input_nodes:
            color = (255, 0, 0) if (pg.Vector2(mouse_pos) - pg.Vector2(pos)).length() <= self.circle_radius else self.circle_color
            pg.draw.circle(surface, color, pos, self.circle_radius)

        color = (255, 0, 0) if (pg.Vector2(mouse_pos) - pg.Vector2(self.output_node)).length() <= self.circle_radius else self.circle_color
        pg.draw.circle(surface, color, self.output_node, self.circle_radius)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # Don't start dragging if user clicked a node!
            if self.get_clicked_node(event.pos) is None:
                if self.rect.collidepoint(event.pos):
                    self.dragging = True
                    mouse_x, mouse_y = event.pos
                    self.offset_x = self.rect.x - mouse_x
                    self.offset_y = self.rect.y - mouse_y

        elif event.type == pg.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pg.MOUSEMOTION and self.dragging:
            mouse_x, mouse_y = event.pos
            self.rect.x = mouse_x + self.offset_x
            self.rect.y = mouse_y + self.offset_y

        self.update_nodes()
    #fixes recognization of node being clicked
    def get_clicked_node(self, mouse_pos):
        for i, pos in enumerate(self.input_nodes):
            if (pg.Vector2(mouse_pos) - pg.Vector2(pos)).length() <= self.circle_radius:
                return ("input", i, pos)  # include pos!
        if (pg.Vector2(mouse_pos) - pg.Vector2(self.output_node)).length() <= self.circle_radius:
            return ("output", 0, self.output_node)
        return None
    #allows usage with wires.
    def get_node_positions(self):
        positions = {}

        if self.gate_type == "NOT":
            positions["in"] = self.input_nodes[0]
        else:
            positions["in1"] = self.input_nodes[0]
            positions["in2"] = self.input_nodes[1]

        positions["out"] = self.output_node
        return positions

    def stop_dragging(self):
        self.dragging = False

    def get_gate_type(self):
        return self.gate_type

    def set_voltage(self, voltage):
        self.voltage = voltage

    def get_voltage(self):
        return self.voltage
