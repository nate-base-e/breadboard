#board that other components will be placed on
#45x80 grid 3600 total squares
#each square 16px
import pygame as pg


#couldn't get it to work, but I'm not sure where to go from here.

"""def check_voltage(components, wires):
    adder: int = 0
    node_inputs = ["in1", "in2", "left", "cathode" "top"]
    node_outputs = ["out", "right", "anode", "bottom"]

    for comp in components: #access all components
        #print(comp)
        for node, pos in comp.get_node_positions().items(): #access all nodes
            #print(node, pos)
            for wire in wires: #access all wires
                #print(wire)
                if wire.get_other_end(comp, node): #check if wire is connected
                    print("main component: ", comp, " main node: ", node)
                    wired_comp = wire.get_other_end(comp, node)[0]
                    wired_node = wire.get_other_end(comp, node)[1]
                    print("wired component: ", wired_comp, " wired_node: ", wired_node)
                    if node in node_outputs and wired_node in node_inputs: #wire goes from output to input
                        if isinstance(wired_comp, Battery): #check if wire is connected to battery
                            print("wire is connected to battery")
                            adder += 1
                            print(adder)
                        if isinstance(wired_comp, Switch): #check if wire is connected to switch
                            print("wire is connected to switch")
                            if wired_comp.is_on(): #check if switch is on or not if on no change if off -1 to adder
                                print(adder)
                            elif wired_comp.is_off():
                                adder -=1
                        if isinstance(wired_comp, Lights): #check if light is connected to wire
                            if bin(adder)[-1] == 1: #check last digit of binary number of adder
                                wired_comp.turn_on()
                                print("light should be on")
                            elif bin(adder)[-1] == 0:
                                wired_comp.turn_off()
                        if isinstance(wired_comp, Gates): #check if wire is connected to gate
                            if wired_comp.get_gate_type() == "AND": #if AND gate add one to adder
                                adder+=1"""

class Square():

    def __init__(self, surface, pos_x, pos_y):
        self.clicked = False
        pg.draw.rect(surface, (250, 241, 142), (pos_x, pos_y, 20, 20))
        pg.draw.circle(surface, (99, 96, 57), (pos_x, pos_y), 4)







