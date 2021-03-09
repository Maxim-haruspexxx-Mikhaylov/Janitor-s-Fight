import pygame
import os
from pygame import Color as color
import random
import Game
import Tiles
import Players
import HUD
from Sounds import Sounds
from Splash import Splash


class GetImage:
    def __init__(self, name, size=None, colorkey=None):
        self.name = name
        self.colorkey = colorkey
        self.size = size

    def load_image(self):
        fullname = os.path.join('Resources', self.name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if self.colorkey is not None:
            image = image.convert()
            if self.colorkey == -1:
                self.colorkey = image.get_at((0, 0))
            image.set_colorkey(self.colorkey)
        else:
            image = image.convert_alpha()
        if self.size:
            image = pygame.transform.scale(image, self.size)
        return image


class Board:
    def __init__(self, width, height, size):
        self.cell_size = 80
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = (size[0] - self.width * self.cell_size) // 2
        self.top = (size[1] - self.height * self.cell_size) // 2
        self.tile_sprites = pygame.sprite.Group()
        self.players_sprites = pygame.sprite.Group()
        self.tiles = ['leaves2.png', 'snow2.png']
        self.no_tiles = True
        self.flag1 = 2
        self.flag2 = 2

    def render(self, screen):
        left = self.left
        top = self.top
        self.max_width = len(self.board[0])
        self.max_height = len(self.board)
        for y in range(self.max_height):
            for x in range(self.max_width):
                if (x != self.max_width - 1 or y != 0) and (x != 0 or y != self.max_height - 1) and self.no_tiles:
                    Tiles.Tile(left, top, self.tile_sprites)
                elif x == self.max_width - 1 and y == 0:
                    pygame.draw.rect(screen, color('orange'), (left, top, self.cell_size, self.cell_size), 0)
                    if not game.orange_moved:
                        screen.blit(GetImage("janitor_orange1.png", (76, 76), colorkey=-1).load_image(), (left, top))
                elif x == 0 and y == self.max_height - 1:
                    pygame.draw.rect(screen, color('aquamarine3'), (left, top, self.cell_size, self.cell_size), 0)
                    if not game.blue_moved:
                        screen.blit(GetImage("janitor_blue1.png", (76, 76), colorkey=-1).load_image(), (left, top))
                pygame.draw.rect(screen, color('brown'), (left, top, self.cell_size, self.cell_size), 1)
                left += self.cell_size
            top += self.cell_size
            left = self.left
        pygame.draw.rect(screen, color('brown'), (self.left, self.top,
                                                  self.cell_size * self.width, self.cell_size * self.height), 2)
        self.no_tiles = False

    def set_players(self):
        self.player1 = Players.Player(self.left + 2, (self.max_height - 1) * self.cell_size + self.top + 2,
                                      1, self.players_sprites)
        self.player2 = Players.Player((self.max_width - 1) * self.cell_size + self.left + 2, self.top + 2,
                                      2, self.players_sprites)

    def update(self, screen):
        self.tile_sprites.draw(screen)
        self.players_sprites.draw(screen)
        for tile in self.tile_sprites:
            for player in self.players_sprites:
                if pygame.sprite.collide_mask(tile, player):
                    if player.number() == 2:
                        tile.paint('orange')
                    else:
                        tile.paint('aquamarine3')

    def get_tiles(self):
        return self.tile_sprites


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Битва дворников')
    size = (1200, 900)
    screen = pygame.display.set_mode(size)
    sound_profile = Sounds()
    Splash().start_screen(screen, GetImage('Rules.png').load_image())

    motion_events_1 = [26, 4, 22, 7]
    motion_events_2 = [82, 80, 81, 79]
    change_event_1 = 44
    change_event_2 = 229
    forfeit_event_1 = 9
    forfeit_event_2 = 228

    board_width = 7
    board_height = 7

    board = Board(board_width, board_height, size)
    hud = HUD.Hud(size, board_width * board.cell_size, screen)
    game = Game.Game(board_width * board_height - 2, hud, sound_profile)

    running = True
    screen.fill((255, 255, 255))
    board.render(screen)
    board.set_players()
    pygame.display.flip()

    while running:
        if game.won or game.check_end():
            pass
        else:
            board.update(screen)
            board.render(screen)
            hud.draw(game, board.player1, board.player2)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.scancode in motion_events_1:
                    if game.get_turn() == 1:
                        board.player1.check(event, board.cell_size, board.tile_sprites, game)
                if event.type == pygame.KEYDOWN and event.scancode in motion_events_2:
                    if game.get_turn() == 2:
                        board.player2.check(event, board.cell_size, board.tile_sprites, game)
                if event.type == pygame.KEYDOWN and event.scancode == change_event_1:
                    if game.get_turn() == 1:
                        board.player1.check(event, board.cell_size, board.tile_sprites, game)
                if event.type == pygame.KEYDOWN and event.scancode == change_event_2:
                    if game.get_turn() == 2:
                        board.player2.check(event, board.cell_size, board.tile_sprites, game)
                if event.type == pygame.KEYDOWN and event.scancode == 16:
                    sound_profile.pause()
                if event.type == pygame.KEYDOWN and event.scancode == forfeit_event_1:
                    game.forfeit(1)
                if event.type == pygame.KEYDOWN and event.scancode == forfeit_event_2:
                    game.forfeit(2)
                if event.type == pygame.QUIT:
                    running = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.scancode == 16:
                sound_profile.pause()
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
    pygame.quit()
