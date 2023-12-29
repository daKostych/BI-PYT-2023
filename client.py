from pygame.locals import *
from game_variables import *
from network import Network
import pickle
import sys

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout")


class Client:

    def __init__(self, ip, port):
        self.net = Network(ip, port)
        self.id = self.net.id

    def run(self):
        run = True
        flag1, flag2 = True, True
        while run:
            clock.tick(fps)

            mouse_x, mouse_y = pygame.mouse.get_pos()
            game = self.send_data(mouse_x, mouse_y)

            if game.game_over == 0:
                if game.ready[0] and game.ready[1]:
                    game.illustrate_game(screen)
                else:
                    screen.fill((0, 0, 0))
                    font = pygame.font.SysFont("comicsans", 60)
                    text = font.render("Waiting for second player...", 1, (255, 0, 0))
                    screen.blit(text, (500, 400))
                    pygame.display.update()
            elif game.game_over == 1:
                while flag1:
                    draw_message("You won!", "Click to restart!")
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            flag1 = False
                            self.net.client.send(str.encode("Ready"))
                        self.quit_check(game, event)
                    if flag1:
                        self.net.client.send(str.encode("Not Ready"))
                    game = pickle.loads(self.net.client.recv(2048*12))
            else:
                while flag2:
                    draw_message("You Loose!", "Click to restart!")
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            flag2 = False
                            self.net.client.send(str.encode("Ready"))
                        self.quit_check(game, event)
                    if flag2:
                        self.net.client.send(str.encode("Not Ready"))
                    game = pickle.loads(self.net.client.recv(2048*12))

            for event in pygame.event.get():
                self.quit_check(game, event)

            flag1, flag2 = True, True

    def send_data(self, mouse_x, mouse_y):
        data = (mouse_x, mouse_y)
        reply = self.net.send(data)
        return reply

    def quit_check(self, game, event):
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            game.ready[int(self.id)] = False
            pygame.quit()
            sys.exit()
        if pygame.key.get_pressed()[K_ESCAPE]:
            game.ready[int(self.id)] = False
            pygame.quit()
            sys.exit()


def draw_message(message1, message2=None):
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont("comicsans", 60)
    text1 = font.render(message1, 1, (255, 0, 0))
    text2 = font.render(message2, 1, (255, 0, 0))
    screen.blit(text1, (625, 400))
    screen.blit(text2, (585, 450))
    pygame.display.update()


def menu():
    run = True

    while run:
        clock.tick(fps)
        draw_message("Click to play!")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    client = Client(sys.argv[1], int(sys.argv[2]))

    if client.id == "Rejected":
        print(f'Rejected, the maximum number of connections has been reached')
        pygame.quit()
        sys.exit()
    else:
        client.run()


while True:
    menu()
