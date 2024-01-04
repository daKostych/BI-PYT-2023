"""
Module representing a Breakout game.

Classes:
    Game: Represents the game and its components.
"""

import pygame
from wall import Wall
from game_variables import background_image
from paddle import Paddle
from ball import Ball


class Game:
    """
    Class representing the Breakout game.

    Attributes:
        wall (Wall): Wall object representing the blocks in the game.
        paddle (Paddle): Paddle object representing the player's paddle.
        ball (Ball): Ball object representing the game ball.
        turn (list): List representing the current turn in the game.
        ready (list): List indicating if players are ready to start the game.
        game_over (int): Integer representing the game state (0 for ongoing, -1 for loss, 1 for win).

    Methods:
        __init__: Initializes the Game object.
        update_game: Updates the game state based on the mouse position.
        illustrate_game: Draws the current game state on the screen.
        reset: Resets the game to its initial state.
    """

    def __init__(self):
        """
        Initializes the Game object.

        Creates instances of Wall, Paddle, and Ball. Initializes turn, ready, and game_over attributes.
        """
        self.wall = Wall()
        self.paddle = Paddle()
        self.ball = Ball(self.paddle.x + (self.paddle.width // 2), self.paddle.y - self.paddle.height - 5)
        self.turn = [0]
        self.ready = [False, False]
        self.game_over = 0

    def update_game(self, mouse_pos):
        """
        Updates the game state based on the mouse position.

        Args:
            mouse_pos (tuple): Tuple representing the mouse position (x, y).

        Returns:
            int: Game over state (0 for ongoing, -1 for loss, 1 for win).
        """
        self.paddle.move(mouse_pos[0])
        self.game_over = self.ball.move(self.paddle, self.wall, self.turn)

    def illustrate_game(self, screen, player):
        """
        Draws the current game state on the screen.

        Args:
            screen (pygame.Surface): Pygame surface representing the game screen.
            player (int): Player identifier (0 or 1).

        Draws the wall, paddle, ball, and turn information on the screen.
        """
        screen.blit(background_image, (0, 0))
        self.wall.draw_wall(screen)
        self.paddle.draw(screen)
        self.ball.draw(screen)
        font = pygame.font.SysFont("comicsans", 25)
        if self.turn[0] % 2 == player:
            text = font.render("Your turn!", 1, (255, 255, 255))
        else:
            text = font.render("Mate's turn!", 1, (255, 255, 255))
        screen.blit(text, (705, 500))
        pygame.display.update()

    def reset(self):
        """
        Resets the game to its initial state.

        Creates new instances of Wall, Paddle, and Ball. Resets turn, ready, and game_over attributes.
        """
        self.wall = Wall()
        self.paddle = Paddle()
        self.ball = Ball(self.paddle.x + (self.paddle.width // 2), self.paddle.y - self.paddle.height - 5)
        self.turn = [0]
        self.wall.create_wall()
        self.game_over = 0
        self.ready = [False, False]
