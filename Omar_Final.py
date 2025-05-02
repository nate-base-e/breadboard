import pygame as pg
from components.battery import Battery
from components.Resistor import Resistor
from components.wire import Wire
from components.lights import Lights

def test_resistor_voltage_current():
    pg.init()
    screen = pg.display.set_mode((1, 1))  # Needed to load images

    # Load light images
    on_img = pg.image.load("images/onled.png").convert_alpha()
    off_img = pg.image.load("images/offled.png").convert_alpha()

    # Create components
    battery = Battery(x=100, y=100, width=100, height=40, screen=screen)
    battery.set_voltage(9)

    resistor = Resistor(x=300, y=100)
    light = Lights(x=500, y=100, off_image=off_img, on_image=on_img)

    # Wire from battery to resistor
    wire1 = Wire(
        start_pos=battery.get_node_positions()['right'],
        end_pos=resistor.get_node_positions()['left'],
        start_comp=battery,
        end_comp=resistor,
        start_node='right',
        end_node='left'
    )
    wire1.transfer_power()

    # Manually send voltage from resistor to light
    light.set_voltage(resistor.voltage_drop)

    # Output test result
    print("=== Resistor Test ===")
    print(f"Battery Voltage: {battery.get_voltage()} V")
    print(f"Resistor Resistance: {resistor.resistance} Ω")
    print(f"Voltage Drop across Resistor: {resistor.voltage_drop:.2f} V")
    print(f"Current through Resistor: {resistor.current:.4f} A")
    print(f"Light On: {'Yes' if light.is_on() else 'No'}")

    pg.quit()

if __name__ == "__main__":
    test_resistor_voltage_current()
