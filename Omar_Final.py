import pygame as pg
from components.battery import Battery
from components.Resistor import Resistor
from components.wire import Wire

def test_resistor_voltage_current():
    pg.init()
    screen = pg.display.set_mode((1, 1))  # Needed to load images

    # Create battery and set 9V
    battery = Battery(x=100, y=100, width=100, height=40, screen=screen)
    battery.setVoltage(9)

    # Create resistor
    resistor = Resistor(x=300, y=100)

    # Connect battery right to resistor left
    wire = Wire(
        start_pos=battery.get_node_positions()['right'],
        end_pos=resistor.get_node_positions()['left'],
        start_comp=battery,
        end_comp=resistor,
        start_node='right',
        end_node='left'
    )

    # Transfer power
    wire.transfer_power()

    # Show test result
    print("=== Resistor Test ===")
    print(f"Battery Voltage: {battery.getVoltage()} V")
    print(f"Resistor Resistance: {resistor.resistance} Ω")
    print(f"Voltage Drop across Resistor: {resistor.voltage_drop:.2f} V")
    print(f"Current through Resistor: {resistor.current:.4f} A")

    pg.quit()

if __name__ == "__main__":
    test_resistor_voltage_current()
