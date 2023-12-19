from pygame.locals import *

from wall import Wall
from game_variables import *
from paddle import Paddle


pygame.init()

pygame.display.set_caption("Breakout")

wall = Wall()
wall.create_wall()
paddle = Paddle()

run = True
while run:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            run = False
    if pygame.key.get_pressed()[K_ESCAPE]:
        run = False

    screen.blit(background_image, (0, 100))
    wall.draw_wall()
    paddle.move()
    paddle.draw()

    pygame.display.update()


pygame.quit()
