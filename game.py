from wall import Wall
from game_variables import *
from paddle import Paddle
from ball import Ball


class Game:

    def __init__(self):
        self.wall = Wall()
        self.paddle = Paddle()
        self.ball = Ball(self.paddle.x + (self.paddle.width // 2), self.paddle.y - self.paddle.height - 5)
        self.turn = [0]
        self.ready = [False, False]
        self.game_over = 0

    def update_game(self, mouse_pos):
        self.paddle.move(mouse_pos[0])
        self.game_over = self.ball.move(self.paddle, self.wall, self.turn)

    def illustrate_game(self, screen):
        screen.blit(background_image, (0, 0))
        self.wall.draw_wall(screen)
        self.paddle.draw(screen)
        self.ball.draw(screen)
        pygame.display.update()

    def reset(self):
        self.wall = Wall()
        self.paddle = Paddle()
        self.ball = Ball(self.paddle.x + (self.paddle.width // 2), self.paddle.y - self.paddle.height - 5)
        self.turn = [0]
        self.wall.create_wall()
        self.game_over = 0
        self.ready = [False, False]
