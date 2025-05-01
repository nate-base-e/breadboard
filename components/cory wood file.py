#put just below
# for event in pg.event.get():
def check_circuit(components, wires):
    visited = set()
    queue = deque()
    signal_values = {}  # tracks logic level at each (component, node)

    # init BFS from battery right node
    for comp in components:
        if isinstance(comp, Battery):
            start = (comp, "right")
            queue.append(start)
            visited.add(start)
            signal_values[start] = 1

    # build adjacency graph
    adjacency = {}
    for wire in wires:
        a = (wire.start_comp, wire.start_node)
        b = (wire.end_comp, wire.end_node)
        adjacency.setdefault(a, []).append(b)
        adjacency.setdefault(b, []).append(a)

    #BFS traversal with signal logic
    while queue:
        current = queue.popleft()
        current_comp, current_node = current
        current_signal = signal_values.get(current, 0)

        # set inputs if applicable
        if hasattr(current_comp, 'set_inputs') and current_node.startswith("in"):
            inputs = []
            for node in adjacency.get(current, []):
                if signal_values.get(node, 0):
                    inputs.append(1)
            if inputs:
                current_comp.set_inputs(*inputs)

        # propagate to neighbors
        for neighbor in adjacency.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                neighbor_comp, neighbor_node = neighbor

                # Evaluate logic if it's an output node
                if hasattr(current_comp, 'output') and current_node.startswith("out"):
                    signal_values[neighbor] = current_comp.output()
                else:
                    signal_values[neighbor] = current_signal

                queue.append(neighbor)

    # check all lights
    all_lights_connected = True
    for comp in components:
        if isinstance(comp, Lights):
            anode = (comp, "anode")
            cathode = (comp, "cathode")

            if signal_values.get(anode, 0) and signal_values.get(cathode, 0):
                comp.turn_on()
                print(f"Light {comp} is ON")
            else:
                comp.turn_off()
                all_lights_connected = False
                print(f"Light {comp} is OFF or not connected properly")

    if all_lights_connected:
        print("All lights are connected correctly!")
    else:
        print("Some lights are not properly connected.")

        # put right above  pg.display.flip() in main
        # clock.tick(60)
        #checks to see if everything is connected and receiving signal
    if pg.key.get_pressed()[pg.K_c]:  # Press 'C' to check the circuit
        check_circuit(components, wires)


