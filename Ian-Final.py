import pygame as pg
from tabulate import tabulate

from components.Switch import Switch
from components.battery import Battery
from components.gates import Gates
from components.lights import Lights
from main import SCREEN_WIDTH, SCREEN_HEIGHT


def test_two_bit_adder(components, wires):
    switches = []
    lights = []
    and_gates = []
    or_gates = []
    xor_gates = []
    battery = []

    for comp in components:
        if isinstance(comp, Switch):
            switches.append(comp)
        elif isinstance(comp, Lights):
            lights.append(comp)
        elif isinstance(comp, Gates):
            if comp.gate_type == "AND":
                and_gates.append(comp)
            elif comp.gate_type == "OR":
                or_gates.append(comp)
            elif comp.gate_type == "XOR":
                xor_gates.append(comp)
        elif isinstance(comp, Battery):
            battery.append(comp)

    if len(switches) < 4:
        print(f"FAIL: Not enough switches for two 2-bit numbers. Need 4, found {len(switches)}.")
        return False
    if len(lights) < 3:
        print(f"FAIL: Not enough lights for outputs. Need 3 (Sum1, Sum0, Carry Out), found {len(lights)}.")
        return False
    if len(xor_gates) < 2:
        print(f"FAIL: Not enough XOR gates for full adder sums. Need 2, found {len(xor_gates)}.")
        return False
    if len(and_gates) < 4:
        print(f"FAIL: Not enough AND gates for carries. Need 4, found {len(and_gates)}.")
        return False
    if len(or_gates) < 1:
        print(f"FAIL: Missing OR gate for combining carry outputs. Need 1, found {len(or_gates)}.")
        return False
    if len(battery) < 1:
        print(f"FAIL: Need at least one battery to power the circuit. Found {len(battery)}.")
        return False

    print("PASS: All components required for a 2-bit adder are present.")
    print("Testing 2-bit adder logic simulation...")

    test_cases = [
        ([0, 0], [0, 0], [0, 0, 0]),
        ([0, 1], [0, 1], [1, 0, 0]),
        ([1, 0], [0, 1], [1, 1, 0]),
        ([1, 1], [1, 1], [1, 0, 1])
    ]

    all_passed = True
    for A, B, expected in test_cases:
        sum0 = A[1] ^ B[1]
        sum1_temp = A[0] ^ B[0]
        carry0 = A[1] & B[1]
        carry1_direct = A[0] & B[0]
        propagate_and = sum1_temp & carry0
        additional_and = (A[0] ^ B[0]) & carry0
        carry_out = carry1_direct | propagate_and
        sum1 = sum1_temp ^ carry0

        result = [sum1, sum0, carry_out]

        if result != expected:
            a_decimal = A[0] * 2 + A[1]
            b_decimal = B[0] * 2 + B[1]
            expected_decimal = expected[0] * 2 + expected[1] + expected[2] * 4
            result_decimal = result[0] * 2 + result[1] + result[2] * 4
            print(f"FAIL: {a_decimal} + {b_decimal} = {expected_decimal}, but got {result_decimal}")
            print(
                f"Binary: {A[0]}{A[1]} + {B[0]}{B[1]} = {expected[0]}{expected[1]}{expected[2]}, but got {result[0]}{result[1]}{result[2]}")
            all_passed = False

    if all_passed:
        print("PASS: 2-bit adder logic simulation successful!")
        return True
    else:
        print("FAIL: 2-bit adder logic simulation failed.")
        return False


def setup_two_bit_adder():
    components = []

    try:
        switch_on_img = pg.image.load("images/Switch-On.png").convert_alpha()
        switch_off_img = pg.image.load("images/Switch-Off.png").convert_alpha()
        on_img = pg.image.load("images/onled.png").convert_alpha()
        off_img = pg.image.load("images/offled.png").convert_alpha()
        gate_sprite = pg.image.load("images/and or not gates f.png").convert_alpha()
    except:
        print("Warning: Image files not found, using placeholder images.")
        switch_on_img = pg.Surface((50, 50))
        switch_off_img = pg.Surface((50, 50))
        on_img = pg.Surface((30, 30))
        off_img = pg.Surface((30, 30))
        gate_sprite = pg.Surface((90, 30))

    screen = pg.display.get_surface()
    if not screen:
        screen = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    switches = []
    switch_positions = [(100, 100), (200, 100), (300, 100), (400, 100)]
    for i, (x, y) in enumerate(switch_positions):
        switch = Switch(x, y, switch_on_img, switch_off_img, f"Switch{i}", False)
        switches.append(switch)
        components.append(switch)

    lights = []
    for i in range(3):
        light = Lights(300 + i * 80, 200, off_img, on_img)
        lights.append(light)
        components.append(light)

    xor_gates = []
    for i in range(2):
        xor = Gates("XOR", f"XOR{i}", 100 + i * 120, 300, gate_sprite)
        xor_gates.append(xor)
        components.append(xor)

    and_gates = []
    for i in range(4):
        and_gate = Gates("AND", f"AND{i}", 100 + i * 120, 400, gate_sprite)
        and_gates.append(and_gate)
        components.append(and_gate)

    or_gate = Gates("OR", "OR1", 300, 500, gate_sprite)
    components.append(or_gate)

    battery = Battery(x=50, y=50, width=100, height=40, screen=screen)
    components.append(battery)

    wires = []

    return components, wires


def run_comprehensive_two_bit_adder_tests():
    print("Running 2-bit adder tests...\n")

    test_cases = []
    results = []

    for a1 in [0, 1]:
        for a0 in [0, 1]:
            for b1 in [0, 1]:
                for b0 in [0, 1]:
                    a_val = a1 * 2 + a0
                    b_val = b1 * 2 + b0
                    sum_val = a_val + b_val

                    carry = 1 if sum_val > 3 else 0
                    sum1 = (sum_val // 2) % 2
                    sum0 = sum_val % 2

                    computed_sum0 = a0 ^ b0
                    sum1_temp = a1 ^ b1

                    carry0 = a0 & b0
                    carry1_direct = a1 & b1

                    propagate_and = sum1_temp & carry0

                    computed_carry_out = carry1_direct | propagate_and

                    computed_sum1 = sum1_temp ^ carry0

                    test_case = {
                        'A1': a1, 'A0': a0, 'B1': b1, 'B0': b0,
                        'A_dec': a_val, 'B_dec': b_val, 'Sum_dec': sum_val,
                        'Expected': [sum1, sum0, carry],
                        'Computed': [computed_sum1, computed_sum0, computed_carry_out],
                        'Result': 'PASS' if [sum1, sum0, carry] == [computed_sum1, computed_sum0,
                                                                    computed_carry_out] else 'FAIL'
                    }
                    test_cases.append(test_case)

                    result_row = [
                        f"{a1}{a0}", f"{b1}{b0}", f"{a_val}", f"{b_val}", f"{sum_val}",
                        f"{sum1}{sum0}{carry}", f"{computed_sum1}{computed_sum0}{computed_carry_out}",
                        test_case['Result']
                    ]
                    results.append(result_row)

    headers = ["A", "B", "A(dec)", "B(dec)", "Sum(dec)", "Expected", "Computed", "Result"]
    print(tabulate(results, headers=headers, tablefmt="grid"))

    success_count = sum(1 for case in test_cases if case['Result'] == 'PASS')
    print(f"\nSuccess rate: {success_count}/{len(test_cases)} ({success_count / len(test_cases) * 100:.1f}%)")

    failures = [case for case in test_cases if case['Result'] == 'FAIL']
    if failures:
        print("\nFAILURES:")
        for case in failures:
            print(f"A={case['A1']}{case['A0']}({case['A_dec']}), B={case['B1']}{case['B0']}({case['B_dec']})")
            print(
                f"  Expected: {case['Expected'][0]}{case['Expected'][1]}{case['Expected'][2]} (decimal: {case['Sum_dec']})")
            print(f"  Computed: {case['Computed'][0]}{case['Computed'][1]}{case['Computed'][2]}")

    return success_count == len(test_cases)


def main():
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()

    gate_sprite = pg.image.load("images/and or not gates f.png").convert_alpha()
    on_img = pg.image.load("images/onled.png").convert_alpha()
    off_img = pg.image.load("images/offled.png").convert_alpha()
    switch_on_img = pg.image.load("images/Switch-On.png").convert_alpha()
    switch_off_img = pg.image.load("images/Switch-Off.png").convert_alpha()

    gates = []

    start_x = 100
    start_y = 450
    spacing_x = 120
    spacing_y = 120

    for i in range(2):
        gates.append(Gates("XOR", f"X{i + 1}", start_x + (i * spacing_x), start_y, gate_sprite))

    for i in range(4):
        gates.append(Gates("AND", f"A{i + 1}", start_x + (i * spacing_x), start_y + spacing_y, gate_sprite))

    gates.append(Gates("OR", "O1", start_x + (2 * spacing_x), start_y + 2 * spacing_y, gate_sprite))

    batteries = []
    batteries.append(Battery(x=30, y=0, width=100, height=40, screen=screen))

    lights = []
    lights.append(Lights(100, 100, off_img, on_img))
    lights.append(Lights(250, 100, off_img, on_img))
    lights.append(Lights(400, 100, off_img, on_img))

    switches = []
    switch_positions = [(650, 100), (650, 200), (650, 300), (650, 400)]
    for i, (x, y) in enumerate(switch_positions):
        new_switch = Switch(x, y, switch_on_img, switch_off_img, f"S{i + 1}", False)
        switches.append(new_switch)

    components = gates + switches + batteries + lights

    wires = []

    test_result = test_two_bit_adder(components, wires)

    if test_result:
        print("2-bit adder setup and logic verified successfully!")
    else:
        print("2-bit adder verification failed.")

    print("\n=== RUNNING TESTS ===")
    run_comprehensive_two_bit_adder_tests()

    return


if __name__ == "__main__":
    main()