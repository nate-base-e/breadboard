# dcaclab.com
import pygame as pg

class Gates:
    def __init__(self, gateType, gateID, x, y, image):
        self.gate_id = gateID
        self.gate_type = gateType.upper() #AND OR NOT
        #display properties
        self.x = x
        self.y = y
        self.image = image
        gate_width = int(self.image.get_width() // 3)
        gate_height = self.image.get_height()
        self.rect = pg.Rect(x, y, gate_width, gate_height)
        self.dragging = False

        #dragging
        self.offset_x = 0
        self.offset_y = 0

        #logic processing
        self.inputs = []  #list of input values (0 or 1)
        self.output_val = None #cached output after eval

        #determine which part of the picture is being shown (which gate)
        #0 = AND 1 = OR 2 = NOT
        self.sprite_index = {"AND": 0, "OR": 1, "NOT": 2}.get(self.gate_type, 0)

        #node variables
        self.circle_radius = 4
        self.circle_color = (0, 255, 0)  # green nodes

        self.update_nodes()

    def update_nodes(self):
        self.input_nodes = []

        inset = -50  # pixels from the edge

        if self.gate_type == "NOT":
            self.input_nodes.append((self.rect.left - inset, self.rect.centery))
        else:
            self.input_nodes.append((self.rect.left - inset, self.rect.top + 10))
            self.input_nodes.append((self.rect.left - inset, self.rect.bottom - 10))

        self.output_node = (self.rect.right + inset, self.rect.centery)

    def set_inputs(self, *inputs):
        #set input vals for this gate
        self.inputs = inputs

    #evaluate logic gate and output based on it's type
    def eval(self):
        if self.gate_type =="AND":
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
        #draw the correct part of the sprite sheet onto the screen
        full_width = self.image.get_width()
        gate_width = full_width // 3
        gate_height = self.image.get_height()
        # crop 2px from left and right to remove border lines (aesthetic)
        crop_left = 2
        crop_right = 2
        cropped_width = gate_width - (crop_left + crop_right)

        src_x = self.sprite_index * gate_width + crop_left
        src_rect = pg.Rect(src_x, 0, cropped_width, gate_height)

        # adjust drawing size to match cropped width
        draw_rect = pg.Rect(self.rect.x, self.rect.y, cropped_width, gate_height)
        surface.blit(self.image, draw_rect, area=src_rect) # blit that section at current position

        # drawing nodes
        for pos in self.input_nodes:
            pg.draw.circle(surface, self.circle_color, pos, self.circle_radius)

        # Draw output node
        pg.draw.circle(surface, self.circle_color, self.output_node, self.circle_radius)

    def handle_event(self, event):
        #handle mouse events for dragging the gate
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                mouse_x, mouse_y = event.pos
                self.offset_x = self.rect.x - mouse_x
                self.offset_y = self.rect.y - mouse_y

        elif event.type == pg.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pg.MOUSEMOTION and self.dragging:
            #while dragging, update position based on mouse movement
            mouse_x, mouse_y = event.pos
            self.rect.x = mouse_x + self.offset_x
            self.rect.y = mouse_y + self.offset_y

        self.update_nodes()

    #checks if nodes are clicked for seamless wire use
    def get_clicked_node(self, mouse_pos):
        for i, pos in enumerate(self.input_nodes):
            if (pg.Vector2(mouse_pos) - pg.Vector2(pos)).length() <= self.circle_radius:
                return ("input", i)
        if (pg.Vector2(mouse_pos) - pg.Vector2(self.output_node)).length() <= self.circle_radius:
            return ("output", 0)
        return None

    def stop_dragging(self):
        self.dragging = False