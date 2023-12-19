from pygame.locals import *

from wall import Wall
from game_variables import *
from paddle import Paddle
from ball import Ball


pygame.init()

pygame.display.set_caption("Breakout")

wall = Wall()
wall.create_wall()
paddle = Paddle()
ball = Ball(paddle.x + (paddle.width // 2), paddle.y - paddle.height - 5)

run = True
while run:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            run = False
    if pygame.key.get_pressed()[K_ESCAPE]:
        run = False

    screen.blit(background_image, (0, 0))
    wall.draw_wall()
    paddle.move()
    paddle.draw()
    ball.draw()
    ball.move(paddle, wall)

    pygame.display.update()


pygame.quit()
