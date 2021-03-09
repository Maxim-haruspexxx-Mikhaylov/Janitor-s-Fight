import pygame
from pygame import Color as color
import random
import Main
import Tiles
import Game
from Image import GetImage
from Sounds import Sounds


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, number, *group):
        super().__init__(*group)
        self.images = [Main.GetImage("janitor_blue1.png", (76, 76), colorkey=-1).load_image(),
                       Main.GetImage("janitor_blue2.png", (76, 76), colorkey=-1).load_image(),
                       Main.GetImage("janitor_orange1.png", (76, 76), colorkey=-1).load_image(),
                       Main.GetImage("janitor_orange2.png", (76, 76), colorkey=-1).load_image()]
        self.num = number
        if self.num == 1:
            self.images_ori = [self.images[0], self.images[1]]
        else:
            self.images_ori = [self.images[2], self.images[3]]

        if self.num == 2:
            self.image = pygame.transform.rotate(self.images_ori[0], 180)
        else:
            self.image = self.images_ori[0]

        self.mask = pygame.mask.from_surface(self.images_ori[0])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tool = 1
        self.dir = 'up'

    def update(self, game, x=None, y=None):
        if x and y:
            self.change_orient()
            self.rect = self.rect.move((x - self.rect.x, y - self.rect.y))
        game.change_turn()

    def number(self):
        return self.num

    def check(self, event, cell_size, tiles, game):
        check_sprites = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite(check_sprites)
        sprite.image = Main.GetImage("blue.png", (76, 76)).load_image()
        sprite.rect = sprite.image.get_rect()
        check_sprites.add(sprite)
        sprite.rect.x = self.rect.x
        sprite.rect.y = self.rect.y
        sprite.mask = pygame.mask.from_surface(sprite.image)
        if event.scancode in [26, 82]:
            sprite.rect.y -= cell_size
            self.dir = 'up'
        elif event.scancode in [22, 81]:
            sprite.rect.y += cell_size
            self.dir = 'down'
        elif event.scancode in [4, 80]:
            sprite.rect.x -= cell_size
            self.dir = 'left'
        elif event.scancode in [7, 79]:
            sprite.rect.x += cell_size
            self.dir = 'right'
        if event.scancode in [44, 229]:
            self.change_tool(game)
        else:
            checked_right = False
            for tile in tiles:
                if not pygame.sprite.collide_mask(sprite, tile):
                    pass
                elif tile.get_name() == 'blue' and self.num == 2 or tile.get_name() == 'orange' and self.num == 1:
                    pass
                elif tile.get_name() == 'leaves.png' and self.tool == 2 or tile.get_name() == 'snow.png' and self.tool == 1:
                    pass
                else:
                    self.update(game, x=sprite.rect.x, y=sprite.rect.y)
                    if self.num == 1:
                        game.blue_moved = True
                    else:
                        game.orange_moved = True
                    checked_right = True
                    if tile.get_name() == 'leaves.png':
                        game.sound_profile.clean('leaves')
                    else:
                        game.sound_profile.clean('snow')
                    if tile.get_name() != 'blue' and tile.get_name() != 'orange' and event.scancode not in [44, 229]:
                        game.get_point(self.num)
            if not checked_right:
                game.sound_profile.mistake()

    def change_tool(self, game):
        if self.tool == 1:
            self.tool = 2
            if self.num == 1:
                self.image = self.images_ori[0]
            else:
                self.image = self.images_ori[1]
        else:
            self.tool = 1
            if self.num == 1:
                self.image = self.images_ori[0]
            else:
                self.image = self.images_ori[1]
        self.change_orient()
        self.update(game)

    def change_orient(self):
        if self.dir == 'up':
            rotation = 0
        elif self.dir == 'down':
            rotation = 180
        elif self.dir == 'left':
            rotation = 90
        else:
            rotation = 270
        if self.tool == 1:
            self.image = pygame.transform.rotate(self.images_ori[0], rotation)
        else:
            self.image = pygame.transform.rotate(self.images_ori[1], rotation)





