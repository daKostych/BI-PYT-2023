"""
Module representing the client side of the Breakout game.

Classes:
    Client: Represents the client instance for playing the Breakout game.

Functions:
    draw_message: Draws a message on the game screen.
    menu: Displays the menu to start the game.
"""

# pylint: disable=no-member
import sys
import pickle
import pygame
import pygame.locals
from game_variables import screen_width, screen_height, clock, fps
from network import Network

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout")


class Client:
    """
    Represents the client side of the Breakout game.

    Attributes:
        net (Network): An instance of the Network class for communication with the server.
        id (int): The ID assigned by the server.

    Methods:
        __init__: Initializes the Client object.
        run: Main loop for running the game on the client side.
        send_data: Sends mouse position data to the server and receives the updated game state.
        quit_check: Checks for quit events and handles accordingly.
        win: Display the win message and handle player input.
        loss: Display the loss message and handle player input.
    """

    def __init__(self, ip, port):
        """
        Initializes the Client object.

        Args:
            ip (str): The IP address of the server.
            port (int): The port number for communication.
        """
        self.net = Network(ip, port)
        self.id = self.net.id

    def run(self):
        """
        Main loop for running the game on the client side.
        """
        run = True
        flag = True

        while run:
            clock.tick(fps)

            # Get mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            game = self.send_data(mouse_x, mouse_y)

            if game.game_over == 0:
                if game.ready[0] and game.ready[1]:
                    game.illustrate_game(screen, int(self.id))
                else:
                    # Display waiting message
                    screen.fill((0, 0, 0))
                    font = pygame.font.SysFont("comicsans", 60)
                    text = font.render("Waiting for second player...", 1, (255, 0, 0))
                    screen.blit(text, (500, 400))
                    pygame.display.update()
            elif game.game_over == 1:
                # Display win message
                self.win(flag, game)
            else:
                # Display loss message
                self.loss(flag, game)

            for event in pygame.event.get():
                self.quit_check(game, event)

    def send_data(self, mouse_x, mouse_y):
        """
        Sends mouse position data to the server and receives the updated game state.

        Args:
            mouse_x (int): X-coordinate of the mouse.
            mouse_y (int): Y-coordinate of the mouse.

        Returns:
            Game: The updated Game object received from the server.
        """
        data = (mouse_x, mouse_y)
        reply = self.net.send(data)
        return reply

    def quit_check(self, game, event):
        """
        Checks for quit events and handles accordingly.

        Args:
            game (Game): The current Game object.
            event (pygame.event.Event): The Pygame event object.
        """
        if event.type in (pygame.QUIT, pygame.K_ESCAPE):
            game.ready[int(self.id)] = False
            pygame.quit()
            sys.exit()
        if pygame.key.get_pressed()[pygame.locals.K_ESCAPE]:
            game.ready[int(self.id)] = False
            pygame.quit()
            sys.exit()

    def win(self, flag, game):
        """
        Display the win message and handle player input.

        Args:
            flag (bool): Flag indicating whether to continue the loop.
            game (Game): The current Game object.
        """
        while flag:
            draw_message("You won!", "Click to restart!")
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    flag = False
                    self.net.client.send(str.encode("Ready"))
                self.quit_check(game, event)
            if flag:
                self.net.client.send(str.encode("Not Ready"))
            game = pickle.loads(self.net.client.recv(2048 * 12))

    def loss(self, flag, game):
        """
        Display the loss message and handle player input.

        Args:
            flag (bool): Flag indicating whether to continue the loop.
            game (Game): The current Game object.
        """
        while flag:
            draw_message("You Loose!", "Click to restart!")
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    flag = False
                    self.net.client.send(str.encode("Ready"))
                self.quit_check(game, event)
            if flag:
                self.net.client.send(str.encode("Not Ready"))
            game = pickle.loads(self.net.client.recv(2048 * 12))


def draw_message(message1, message2=None):
    """
    Draws a message on the game screen.

    Args:
        message1 (str): The main message.
        message2 (str): Additional message (default is None).
    """
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont("comicsans", 60)
    text1 = font.render(message1, 1, (255, 0, 0))
    text2 = font.render(message2, 1, (255, 0, 0))
    screen.blit(text1, (625, 400))
    screen.blit(text2, (585, 450))
    pygame.display.update()


def menu():
    """
    Displays the menu to start the game.
    """
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
        print('Rejected, the maximum number of connections has been reached')
        pygame.quit()
        sys.exit()
    else:
        client.run()


while True:
    menu()
