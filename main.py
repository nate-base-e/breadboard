import pygame as pg
from random import random
from pygame import mixer

from components.Buttons import Button
from components.battery import Battery

# pygame setup


def main():
    # Your program's code goes here
    pg.init()
    screen = pg.display.set_mode((1280, 720))
    clock = pg.time.Clock()
    running = True
    dt = 0

    def PushButton():
        print('button pushed')

    def PushBattery():
        print('battery pushed')

    button = Button(680, 500, 140, 52, "Button 1", 32, (45, 45, 45), (100, 100, 100), (100, 100, 100), (0, 0, 0),PushButton)
    ngButton = Button(680, 580, 140, 52, "Button 2", 32, (45, 45, 45), (100, 100, 100), (100, 100, 100), (0, 0, 0), PushButton)
    battery = Battery(x=100, y=100, width=100, height=40, callback=PushBattery)
    hI = 0
    rollTime = 0

    while running:
        # button event
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            button.handle_event(event)
            ngButton.handle_event(event)
            battery.handle_event(event)


            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                True
                #STUFF HERE

        button.draw(screen)
        ngButton.draw(screen)
        battery.draw(screen)
        pg.display.flip()

if __name__ == "__main__":
    main()