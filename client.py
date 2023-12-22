from pygame.locals import *
from game_variables import *
from network import Network

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout")


class Client:

    def __init__(self):
        self.net = Network()
        self.id = self.net.id

    def run(self):
        run = True
        while run:
            clock.tick(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                    run = False
            if pygame.key.get_pressed()[K_ESCAPE]:
                run = False

            mouse_x, mouse_y = pygame.mouse.get_pos()
            game = self.send_data(mouse_x, mouse_y)
            game.illustrate_game(screen)

        pygame.quit()

    def send_data(self, mouse_x, mouse_y):
        data = (mouse_x, mouse_y)
        reply = self.net.send(data)
        return reply


client = Client()
client.run()


"""
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
"""