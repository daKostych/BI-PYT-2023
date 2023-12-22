from pygame.locals import *
from game_variables import *


# paddle class
class Paddle:
    def __init__(self):
        self.width = 124
        self.height = 15
        self.x = int((screen_width / 2) - self.width // 2)
        self.y = screen_height - self.height - 8
        # self.speed = 10
        self.rect = Rect(self.x, self.y, self.width, self.height)

    def move(self, mouse_x):
        # mouse_x, mouse_y = pygame.mouse.get_pos()
        if (mouse_x > self.width // 2) and (mouse_x < screen_width - self.width // 2):
            self.x = mouse_x - self.width // 2

    def draw(self, screen):
        self.rect = Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, paddle_col, self.rect)
