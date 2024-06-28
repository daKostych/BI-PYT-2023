"""
Module for defining game variables and colors in a Breakout game.
"""

import pygame

screen_width = 1500
screen_height = 844

# paddle and ball colours
paddle_col = (255, 255, 255)
ball_col = (255, 255, 255)
# block colours
block_purple = (114, 41, 178)
block_orange = (253, 135, 0)
block_beige = (218, 198, 122)
# block colours list
block_colour = [block_beige, block_orange, block_purple]

background_image = pygame.image.load(".images/bg.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# game variables
cols = 15
rows = 6
clock = pygame.time.Clock()
fps = 60
