import pygame
from pygame import Color as color
import Main
from random import randint


class Tile(pygame.sprite.Sprite):
    def __init__(self, left, top, *group):
        super().__init__(*group)
        self.tiles = ['leaves.png', 'snow.png']
        self.tile_name = self.tiles[randint(0, 1)]
        self.image = Main.GetImage(self.tile_name, (80, 80)).load_image()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = left + 1
        self.rect.y = top + 1

    def paint(self, colour):
        if colour == 'aquamarine3':
            self.tile_name = 'blue'
        else:
            self.tile_name = 'orange'
        self.image = pygame.Surface((80, 80))
        self.image.fill(color(colour))

    def get_name(self):
        return self.tile_name

    def update(self):
        pass
