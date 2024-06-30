import pygame
import components

win_height = 720
win_width = 550

window = pygame.display.set_mode((win_width, win_height), flags=pygame.SCALED, vsync=1)

# create componenets instances
ground = components.Ground(win_width)
pipes = []
