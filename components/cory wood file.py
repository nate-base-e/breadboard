def check_circuit(components, wires):
    visited = set()
    queue = deque()

    # Step 1: Find all starting points (batteries "right" node)
    for comp in components:
        if isinstance(comp, Battery):
            queue.append((comp, "right"))
            visited.add((comp, "right"))

    # Step 2: Build adjacency list from wires
    adjacency = {}
    for wire in wires:
        a = (wire.start_comp, wire.start_node)
        b = (wire.end_comp, wire.end_node)
        adjacency.setdefault(a, []).append(b)
        adjacency.setdefault(b, []).append(a)

    # Step 3: BFS traversal
    while queue:
        current = queue.popleft()

        neighbors = adjacency.get(current, [])
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    # Step 4: Check if all lights are connected
    all_lights_connected = True
    for comp in components:
        if isinstance(comp, Lights):
            anode = (comp, "anode")
            cathode = (comp, "cathode")

            # At least anode or cathode must be reachable
            if anode not in visited and cathode not in visited:
                all_lights_connected = False
                print(f"Light {comp} is NOT connected properly!")

    if all_lights_connected:
        print("✅ All lights are connected correctly!")
    else:
        print("❌ Some lights are not properly connected.")

        #put it right above main

    if pg.key.get_pressed()[pg.K_c]:  # Press 'C' to check the circuit
        check_circuit(components, wires)

        #put right above  pg.display.flip()
        #clock.tick(60)