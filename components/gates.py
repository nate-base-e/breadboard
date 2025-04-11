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
        gate_width = self.image.get_width() // 3
        gate_height = self.image.get_height()
        src_rect = pg.Rect(self.sprite_index * gate_width, 0, gate_width, gate_height)
        surface.blit(self.image, self.rect, area=src_rect)  # blit that section at current position

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

    def stop_dragging(self):
        self.dragging = False



