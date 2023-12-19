import random
from game_variables import *


# brick wall class
class Wall:
    def __init__(self):
        self.width = screen_width // cols + 10
        self.height = 40
        self.blocks = []

    def create_wall(self):
        for row in range(rows):
            for column in range(cols):
                block_x = (column * self.width) + ((column + 1 if column > 0 else 1) * 5)
                block_y = (row * self.height) + (5 * (row + 1 if row > 0 else 1))
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                strength = random.randint(0, 2)
                block_individual = [rect, strength]
                self.blocks.append(block_individual)

    def draw_wall(self):
        for block in self.blocks:
            pygame.draw.rect(screen, block_colour[block[1]], block[0])
