import pygame
from random import random
from pygame import mixer

# pygame setup


def main():
    # Your program's code goes here
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    while running:

        # button event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

if __name__ == "__main__":
    main()