"""
Module representing the paddle in a Breakout game.

Classes:
    Paddle: Represents the player's paddle.
"""

import pygame
from pygame.locals import Rect
from .game_variables import screen_width, screen_height, paddle_col


class Paddle:
    """
    Class representing the paddle in a Breakout game.

    Attributes:
        width (int): Width of the paddle.
        height (int): Height of the paddle.
        x (int): X-coordinate of the top-left corner of the paddle.
        y (int): Y-coordinate of the top-left corner of the paddle.
        rect (pygame.Rect): Pygame rectangle representing the paddle.

    Methods:
        __init__: Initializes the Paddle object.
        move: Moves the paddle based on the mouse position.
        draw: Draws the paddle on the game screen.
    """

    def __init__(self):
        """
        Initializes the Paddle object.

        Sets the width, height, x, y, and rect attributes.
        """
        self.width = 124
        self.height = 15
        self.x = int((screen_width / 2) - self.width // 2)
        self.y = screen_height - self.height - 8
        self.rect = Rect(self.x, self.y, self.width, self.height)

    def move(self, mouse_x):
        """
        Moves the paddle based on the mouse position.

        Args:
            mouse_x (int): X-coordinate of the mouse position.

        Restricts the paddle's movement within the game screen.
        """
        half_width = self.width // 2
        condition1 = mouse_x > half_width
        condition2 = mouse_x < (screen_width - half_width)
        if condition1 is True and condition2 is True:
            self.x = mouse_x - self.width // 2
            self.rect = Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        """
        Draws the paddle on the game screen.

        Args:
            screen (pygame.Surface): Pygame surface representing the game screen.
        """
        pygame.draw.rect(screen, paddle_col, self.rect)
