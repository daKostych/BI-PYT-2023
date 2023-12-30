"""
Module representing the ball in a Breakout game.

Classes:
    Ball: Represents the game ball.
"""

import pygame
from pygame.locals import Rect
from game_variables import screen_width, screen_height, ball_col


class Ball:
    """
    Class representing the ball in a Breakout game.

    Attributes:
        ball_rad (int): Radius of the ball.
        x (int): X-coordinate of the top-left corner of the ball.
        y (int): Y-coordinate of the top-left corner of the ball.
        rect (pygame.Rect): Pygame rectangle representing the ball.
        speed_x (int): Horizontal speed of the ball.
        speed_y (int): Vertical speed of the ball.
        game_over (int): Game over state (0 for ongoing, -1 for loss, 1 for win).

    Methods:
        __init__: Initializes the Ball object.
        move: Moves the ball and handles collisions with the paddle and wall.
        blocks_collision: Handles collisions with blocks in the wall.
        screen_collision: Handles collisions with the screen boundaries.
        paddle_collision: Handles collisions with the paddle.
        draw: Draws the ball on the game screen.
    """

    def __init__(self, x, y):
        """
        Initializes the Ball object.

        Args:
            x (int): Initial X-coordinate of the ball.
            y (int): Initial Y-coordinate of the ball.
        """
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = 4
        self.speed_y = -4
        self.game_over = 0

    def move(self, paddle, wall, turn):
        """
        Moves the ball and handles collisions with the paddle and wall.

        Args:
            paddle (Paddle): Paddle object representing the player's paddle.
            wall (Wall): Wall object representing the brick wall.
            turn (list): List representing the current turn in the game.

        Returns:
            int: Game over state (0 for ongoing, -1 for loss, 1 for win).
        """
        wall_destroyed = all(block[1] == 0 for block in wall.blocks)  # Check if all blocks in the wall are destroyed

        # Check if the wall is destroyed
        if wall_destroyed:
            self.game_over = 1

        threshold = 8
        self.blocks_collision(wall, threshold)
        self.screen_collision()
        self.paddle_collision(paddle, turn, threshold)

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over

    def blocks_collision(self, wall, threshold):
        """
        Handles collisions with blocks in the wall.

        Args:
            wall (Wall): Wall object representing the brick wall.
            threshold (int): Threshold for collision detection.
        """
        # Collision with blocks
        for block in wall.blocks:
            if self.rect.colliderect(block[0]):
                # Handle collisions from different directions
                if self.speed_y > 0 and abs(self.rect.bottom - block[0].top) < threshold:
                    self.speed_y *= -1
                elif self.speed_y < 0 and abs(self.rect.top - block[0].bottom) < threshold:
                    self.speed_y *= -1
                elif self.speed_x > 0 and abs(self.rect.right - block[0].left) < threshold:
                    self.speed_x *= -1
                elif self.speed_x < 0 and abs(self.rect.left - block[0].right) < threshold:
                    self.speed_x *= -1

                # Reduce block strength or destroy it
                if block[1] > 0:
                    block[1] -= 1
                else:
                    block[0] = (0, 0, 0, 0)

    def screen_collision(self):
        """
        Handles collisions with the screen boundaries.
        """
        # Collision with walls
        if self.rect.left < 1 or self.rect.right > screen_width - 1:
            self.speed_x *= -1

        # Collision with top and bottom of the screen
        if self.rect.top < 1:
            self.speed_y *= -1
        if self.rect.bottom > screen_height - 1:
            self.game_over = -1

    def paddle_collision(self, paddle, turn, threshold):
        """
        Handles collisions with the paddle.

        Args:
            paddle (Paddle): Paddle object representing the player's paddle.
            turn (list): List representing the current turn in the game.
            threshold (int): Threshold for collision detection.
        """
        # Collision with paddle
        if self.rect.colliderect(paddle):
            if self.speed_y > 0 and abs(self.rect.bottom - paddle.rect.top) < threshold:
                # Calculate the point of collision relative to the width of the paddle
                relative_collision_point = (self.rect.centerx - paddle.rect.centerx) / (paddle.rect.width / 2.0)

                # Adjust the speed based on the collision
                self.speed_x = int(relative_collision_point * 10)
                self.speed_y *= -1
            else:
                self.speed_x *= -1
            turn[0] += 1

    def draw(self, screen):
        """
        Draws the ball on the game screen.

        Args:
            screen (pygame.Surface): Pygame surface representing the game screen.
        """
        pygame.draw.circle(screen, ball_col, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
