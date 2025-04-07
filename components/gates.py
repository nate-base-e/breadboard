# dcaclab.com
class Gates:
    def __init__(self, gateType, gateID):
        self.gate_id = gateID
        self.gate_type = gateType.upper() #AND OR NOT
        self.inputs = []
        self.output_val = None

    def set_inputs(self, *inputs):
        self.inputs = inputs

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
