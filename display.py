import pygame
from gui import *

BACKGROUND = (28, 28, 28)


def reset_colours(arr, colour=None, hard_reset=False):
    for val in arr:
        if not val.is_correct() or hard_reset:
            if not colour:
                val.reset()
            else:
                val.colour = colour


def get_positions(arr):
    for val in arr:
        val.calculate_positions(len(arr))


def update_display(screen, height, arr, delay=0, gui=None):
    screen.fill(BACKGROUND)

    for index, num in enumerate(arr):
        num.height = (num.value * num.height_interval) + num.height_interval
        pygame.draw.line(screen, num.colour, ((index+1.45)*(num.gap), height),
                         ((index+1.45)*(num.gap), height - num.height), num.gap - 2)

    if gui:
        ui_manager = UIManager(gui)
        ui_manager.draw_elements(screen)

    pygame.display.update()
    pygame.time.wait(delay)
