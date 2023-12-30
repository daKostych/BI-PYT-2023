"""
Module representing the brick wall in a Breakout game.

Classes:
    Wall: Represents the brick wall.
"""

import random
import pygame
from game_variables import screen_width, cols, rows, block_colour


class Wall:
    """
    Class representing the brick wall in a Breakout game.

    Attributes:
        width (int): Width of each brick block.
        height (int): Height of each brick block.
        blocks (list): List of brick blocks, each represented by a rectangle and strength.

    Methods:
        __init__: Initializes the Wall object.
        create_wall: Creates the initial configuration of the brick wall.
        draw_wall: Draws the brick wall on the game screen.
    """

    def __init__(self):
        """
        Initializes the Wall object.

        Sets the width, height, and blocks attributes.
        """
        self.width = screen_width // cols + 10
        self.height = 40
        self.blocks = []

    def create_wall(self):
        """
        Creates the initial configuration of the brick wall.

        Generates a grid of brick blocks with random strength.
        """
        for row in range(rows):
            for column in range(cols):
                block_x = (column * self.width) + ((column + 1 if column > 0 else 1) * 5)
                block_y = (row * self.height) + (5 * (row + 1 if row > 0 else 1))
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                strength = random.randint(0, 2)
                block_individual = [rect, strength]
                self.blocks.append(block_individual)

    def draw_wall(self, screen):
        """
        Draws the brick wall on the game screen.

        Args:
            screen (pygame.Surface): Pygame surface representing the game screen.

        Draws each brick block on the screen using the corresponding color.
        """
        for block in self.blocks:
            pygame.draw.rect(screen, block_colour[block[1]], block[0])
