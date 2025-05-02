import pygame as pg
import pygame.transform

'''
def circut():

    # creating the graph that will hold what is connected to what

    graph = {}
    for wire in wires:
        start = (wire.start_comp, wire.start_terminal)
        end = (wire.end_comp, wire.end_terminal)
        
        if start not in graph:
            graph[start] = []
        graph[start].append(end)
        
        if end not in graph:
            graph[end] = []
        graph[end].append(start)
        
    # create a queue
    queue = []
    
    # look through the components for the batteries
    # we look for the battery first to start the queue
    
    for comp in components:
        if isinstance(comp, Battery):
            for node_name in comp.output_node():
                key = (comp, node_name)
                queue.append(key)
                
                
    # start going through the queue to share information between components
    while queue:
    
        # temporary variable to store the first component and remove it from the queue
        temp = queue.pop(0)
        
        # split the variable in the component and the node
        temp_comp, temp_outnode = temp
        
        # this is a check to see if the node is a output not if it is not skip this node
        if current_term not in current_comp.output_nodes():
            continue
        
        # assume the component will have a get output function to retrieve the output of a node
        voltage = temp_comp.get_output(temp_outnode)
        
        # check the nodes connected to this node and put it in a array
        for neighbor in graph.get(temp, []):
            
            # split the node in to its component and node
            neighbor_comp, neighbor_node = neighbor
            
            # skip this node if the node is not a input node
            if neighbor_node not in neighbor_comp.input_nodes():
                continue
            
            # adjust the connected nodes input state to be the voltage given from the output node from the last component
            # this assumes the component will have a function to adjusts the nodes voltage
            # we also now assume from this the component will run a function when we set the input to update the output 
            # based on whatever logic is for the given component
            neighbor_comp.set_input(neighbor_term, voltage)
            
            # make a new key for the output node of the neighbor node and add it to the queue to continue checking through all connects connected
            for node_name in neighbor_comp.output_node():
                output_key = (neighbor_comp, node_name)
                queue.append(output_key)
'''
class Lights:
    GRID_SIZE = 20

    def __init__(self,x,y,off_image,on_image):

        self.x = round(x / self.GRID_SIZE) * self.GRID_SIZE
        self.y = round(y / self.GRID_SIZE) * self.GRID_SIZE
        self.on_image = pygame.transform.scale(on_image,(70,112))
        self.off_image = pygame.transform.scale(off_image,(70,112))
        self.rect = self.off_image.get_rect(center=(self.x + self.GRID_SIZE // 2,(self.y + self.GRID_SIZE)))
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

        self.volt = False
        self.state = False

        self.nodes = {
            "anode": (
                self.rect.centerx + (self.rect.width // 4),  # Right terminal
                self.rect.bottom + 10 # Just above bottom edge
            ),
            "cathode": (
                self.rect.centerx - (self.rect.width // 4),  # Left terminal
                self.rect.bottom + 10 # Just above bottom edge
            )
        }

        self.nodes = {
            "anode": (
                round(self.nodes["anode"][0] / self.GRID_SIZE) * self.GRID_SIZE,
                round(self.nodes["anode"][1] / self.GRID_SIZE) * self.GRID_SIZE
            ),
            "cathode": (
                round(self.nodes["cathode"][0] / self.GRID_SIZE) * self.GRID_SIZE,
                round(self.nodes["cathode"][1] / self.GRID_SIZE) * self.GRID_SIZE
            )
        }

        self.node_voltages = {
            'anode': 0,
            'cathode': 0
        }

    def draw(self, surface):
        if self.state:
            surface.blit(self.on_image, self.rect)
        else:
            surface.blit(self.off_image, self.rect)

        circle_radius = 4
        circle_color = (0,255,0)

        for pos in self.nodes.values():
            pg.draw.circle(surface,circle_color,pos,circle_radius)


    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                mouse_x, mouse_y = event.pos
                self.offset_x = self.rect.x - (round(mouse_x / self.GRID_SIZE) * self.GRID_SIZE)
                self.offset_y = self.rect.y - (round(mouse_y / self.GRID_SIZE) * self.GRID_SIZE)

            return True

        elif event.type == pg.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pg.MOUSEMOTION and self.dragging:
            mouse_x, mouse_y = event.pos
            new_x = round(mouse_x / self.GRID_SIZE) * self.GRID_SIZE + self.offset_x
            new_y = round(mouse_y / self.GRID_SIZE) * self.GRID_SIZE + self.offset_y

            # Update positions
            self.x = new_x
            self.y = new_y
            self.rect.topleft = (new_x, new_y)

            self.nodes = {
                "anode": (
                    new_x + self.rect.width // 2 + (self.rect.width // 4),
                    new_y + self.rect.height + 10
                ),
                "cathode": (
                    new_x + self.rect.width // 2 - (self.rect.width // 4),
                    new_y + self.rect.height + 10
                )
            }

            self.nodes = {
                "anode": (
                    round(self.nodes["anode"][0] / self.GRID_SIZE) * self.GRID_SIZE,
                    round(self.nodes["anode"][1] / self.GRID_SIZE) * self.GRID_SIZE
                ),
                "cathode": (
                    round(self.nodes["cathode"][0] / self.GRID_SIZE) * self.GRID_SIZE,
                    round(self.nodes["cathode"][1] / self.GRID_SIZE) * self.GRID_SIZE
                )
            }

        return False

    def stop_dragging(self):
        self.dragging = False

    def turn_on(self):
        self.state = True

    def turn_off(self):
        self.state = False

    def toggle(self):
        self.state = not self.state

    def is_on(self):
        return self.state

    def eval_state(self):
        if self.volt > 0:   #omar change it for testing and making lights work on testing
            self.turn_on()
        else:
            self.turn_off()

    def set_voltage(self, volt):
        self.volt = volt
        self.eval_state()

    def get_voltage(self):
        return self.volt

    def get_node_positions(self):
        return self.nodes






