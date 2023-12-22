from pygame.locals import *
from game_variables import *


# ball class
class Ball:
    def __init__(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = 6
        self.speed_y = -6
        self.game_over = 0

    def move(self, paddle, wall, turn):
        wall_destroyed = 1
        collision_threshold = 8
        # collision with blocks
        for block in wall.blocks:
            if self.rect.colliderect(block[0]):
                # from above
                if abs(self.rect.bottom - block[0].top) < collision_threshold and self.speed_y > 0:
                    self.speed_y *= -1
                # from below
                if abs(self.rect.top - block[0].bottom) < collision_threshold and self.speed_y < 0:
                    self.speed_y *= -1
                # from left
                if abs(self.rect.right - block[0].left) < collision_threshold and self.speed_x > 0:
                    self.speed_x *= -1
                # from right
                if abs(self.rect.left - block[0].right) < collision_threshold and self.speed_x < 0:
                    self.speed_x *= -1

                # reducing the block strength
                if block[1] > 0:
                    block[1] -= 1
                else:
                    block[0] = (0, 0, 0, 0)

            # check if the block is not destroyed
            if block[0] != (0, 0, 0, 0):
                wall_destroyed = 0

        # check if the wall is destroyed
        if wall_destroyed == 1:
            self.game_over = 1

        # collision with walls
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1

        # collision with top and bottom of the screen
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > screen_height:
            self.game_over = -1

        # collision with paddle
        if self.rect.colliderect(paddle):
            # if colliding from the top
            if abs(self.rect.bottom - paddle.rect.top) < collision_threshold and self.speed_y > 0:
                # calculate the point of collision relative to the width of the paddle
                relative_collision_point = (self.rect.centerx - paddle.rect.centerx) / (paddle.rect.width / 2.0)

                # adjust the speed based on the collision
                self.speed_x = int(relative_collision_point * 10)
                self.speed_y *= -1
            else:
                self.speed_x *= -1
            turn[0] += 1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over

    def draw(self, screen):
        pygame.draw.circle(screen, ball_col, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
