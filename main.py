import math
import sys
import time
import random

import pygame

from gui import TextBox, Slider
from display import get_positions, update_display, reset_colours
from algorithms import run_check, quick, merge, heap, bitonic, comb, pigeonhole, bubble, bogo

# Initialise pygame module
pygame.init()

# Screen dimensions and other variables
WIDTH = 1500
HEIGHT = 800
arr_size = 10
start_sorting = False
sorting_algorithms = None
delay = None

# Initialise pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sorting Visualiser')

# Colour constants
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
TURQUOISE = (64, 224, 208)


class Value:
    def __init__(self, val: int):
        """Initialize a Value object.

        Args:
            val (int): The value of the object.
        """
        self.value = val
        self.colour = WHITE

    def calculate_positions(self, arr_size: int) -> None:
        """Calculate the positions of the Value object within the display.

        Args:
            arr_size (int): The size of the array being visualized.
        """
        self.height_interval = (HEIGHT // (arr_size + 1))
        self.gap = math.ceil((WIDTH / (arr_size + 1)))
        self.height = (self.value * self.height_interval) + \
            self.height_interval

    def make_correct(self):
        self.colour = GREEN

    def orange(self):
        self.colour = ORANGE

    def purple(self):
        self.colour = PURPLE

    def red(self):
        self.colour = RED

    def turquoise(self):
        self.colour = TURQUOISE

    def reset(self):
        self.colour = WHITE

    def is_correct(self):
        return self.colour == GREEN

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __eq__(self, other):
        return self.value == other.value


# Create an initial array of Value objects
array = [Value(i) for i in random.sample(range(1, arr_size + 1), arr_size)]

# Function to get sorting algorithm parameters
def get_params(arr_len: int):
    """Get a list of sorting algorithms along with their parameters.

    Args:
        arr_len (int): The length of the array.

    Returns:
        List[Tuple[callable, Tuple]]: A list of tuples containing the sorting algorithm and its parameters.
    """
    sorting_algorithms = [
        (quick, (0, arr_len - 1)),
        (merge, (0, arr_len - 1)),
        (heap, ()),
        (bitonic, (0, arr_len, 1)),
        (comb, ()),
        (pigeonhole, ()),
        (bubble, ()),
        (bogo, ())
    ]

    return sorting_algorithms


gui_elements = [
    selected_algorithm := TextBox("Selected Algorithm: NONE", (10, 0), font_size=40),
    arr_slider := Slider((10, 40), 512, min_value=10),
    delay_slider := Slider((10, 75), 1000, extra_text="ms"),
    elapsed_time := TextBox("Elapsed time:", (10, 100)),
    bitonic_warning := TextBox("Please only choose powers of 2 or else the algorithm will not sort.",
                               (350, 100), colour="red"),
    TextBox("R - Shuffle bars", (1125, 0), target_word="R"),
    TextBox("Space - Sort bars", (1125, 25), target_word="Space"),
    TextBox("C - Change sorting algorithm", (1125, 50), target_word="C")
]

current_algorithm_index = 0
bitonic_warning.visible = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start_sorting = True
                current_algorithm, algorithm_params = sorting_algorithms[current_algorithm_index]
                start_time = time.time()
                current_algorithm(screen, HEIGHT, array,
                                  delay, *algorithm_params)
                end_time = time.time()
                if int(delay_slider.current_value) == 0:
                    elapsed_time.text = f"Elapsed time: {(end_time - start_time):.3f}s"
                    elapsed_time.target_word = f"{(end_time - start_time):.3f}s"
                else:
                    elapsed_time.text = "REMOVE DELAY FOR ELAPSED TIME"
                run_check(screen, HEIGHT, array)
                start_sorting = False
            if event.key == pygame.K_c:
                current_algorithm_index = (
                    current_algorithm_index + 1) % len(sorting_algorithms)
            if event.key == pygame.K_r:
                reset_colours(array, hard_reset=True)
                random.shuffle(array)

    if not start_sorting:
        delay = int(delay_slider.current_value)
        sorting_algorithms = get_params(len(array))
        selected_algorithm_name = sorting_algorithms[current_algorithm_index][0].__name__
        selected_algorithm.text = f"Selected Algorithm: {selected_algorithm_name} sort"
        selected_algorithm.target_word = f"{selected_algorithm_name}"
        bitonic_warning.visible = selected_algorithm_name == "bitonic"
        if arr_slider.pressed:
            arr_size = int(arr_slider.current_value)
            array = [Value(i) for i in random.sample(
                range(1, arr_size + 1), arr_size)]
        get_positions(array)
        update_display(screen, HEIGHT, array, gui=gui_elements)
