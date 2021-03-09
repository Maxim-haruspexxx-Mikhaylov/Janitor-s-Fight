import pygame
import os
from pygame import Color as color
import random
import Tiles
import Player


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 130
        self.top = 130
        self.cell_size = 80
        self.tile_sprites = pygame.sprite.Group()
        self.players_sprites = pygame.sprite.Group()
        self.tiles = ['leaves2.png', 'snow2.png']
        self.no_tiles = True

    def render(self, screen):
        left = self.left
        top = self.top
        self.max_width = len(self.board[0])
        self.max_height = len(self.board)
        for y in range(self.max_height):
            for x in range(self.max_width):
                if (x != self.max_width - 1 or y != 0) and (x != 0 or y != self.max_height - 1) and self.no_tiles:
                    Tiles.Tile(left, top, self.tile_sprites)
                pygame.draw.rect(screen, color('brown'), (left, top, self.cell_size, self.cell_size), 1)
                left += self.cell_size
            top += self.cell_size
            left = self.left
        pygame.draw.rect(screen, color('brown'), (self.left, self.top,
                                                  self.cell_size * self.width, self.cell_size * self.height), 2)
        self.no_tiles = False

    def set_players(self):
        self.player1 = Player.Player(self.left + 2, (self.max_height - 1) * self.cell_size + self.top + 2,
                                     1, self.players_sprites)
        self.player2 = Player.Player((self.max_width - 1) * self.cell_size + self.left + 2, self.top + 2,
                                     2, self.players_sprites)

    def update(self, screen):
        self.tile_sprites.draw(screen)
        self.players_sprites.draw(screen)
        for tile in self.tile_sprites:
            for player in self.players_sprites:
                if pygame.sprite.collide_mask(tile, player):
                    if player.number() == 2:
                        tile.paint(color('orange'))
                    else:
                        tile.paint(color('aquamarine'))

    def moving(self):
        self.player2.update('down')
        self.player1.update('up')
