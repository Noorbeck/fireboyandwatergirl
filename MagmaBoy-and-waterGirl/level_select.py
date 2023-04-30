import sys
import pygame
from pygame.locals import *


class LevelSelect():
    def __init__(self):
        self.load_images()

    def load_images(self):
        self.screen = pygame.image.load('data/screens/level_select_screen.png')
        self.titles = {
            1: pygame.image.load('data/screens/level1.png'),
            2: pygame.image.load('data/screens/level2.png'),
        }
        for title in self.titles.keys():
            self.titles[title].set_colorkey((255, 0, 255))

        self.indicator_image = pygame.image.load('data/screens/indicator.png')
        self.indicator_image.set_colorkey((255, 0, 255))

        big_player_size = (64, 128)
        self.left_player = pygame.image.load('data/player_images/hydrogirl.png')
        self.left_player = pygame.transform.scale(
            self.left_player, big_player_size)
        self.left_player.set_colorkey((255, 0, 255))
        self.right_player = pygame.image.load('data/player_images/magmaboy.png')
        self.right_player = pygame.transform.scale(
            self.right_player, big_player_size)
        self.right_player.set_colorkey((255, 0, 255))
