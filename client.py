from pygame.locals import *
from game_variables import *
from network import Network
import pickle

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout")


class Client:

    def __init__(self):
        self.net = Network()
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
                    if flag2:
                        self.net.client.send(str.encode("Not Ready"))
                    game = pickle.loads(self.net.client.recv(2048*12))

            if self.quit_check():
                run = False
                game.ready[int(self.id)] = False
                pygame.quit()

            flag1, flag2 = True, True

    def send_data(self, mouse_x, mouse_y):
        data = (mouse_x, mouse_y)
        reply = self.net.send(data)
        return reply

    def quit_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                return True
            if pygame.key.get_pressed()[K_ESCAPE]:
                return True
        return False


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
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    client = Client()
    client.run()


while True:
    menu()
