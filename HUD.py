import pygame
from pygame import Color as color
import random
import Main
import Tiles
from Image import GetImage


class Hud:
    def __init__(self, size, board, screen):
        self.color1 = 'aquamarine3'
        self.color2 = 'orange'
        self.line_height = 600
        self.line_top = size[1] / 3 - self.line_height / 2
        self.line_width = size[0]
        self.font = pygame.font.Font(None, 50)
        self.larger_font = pygame.font.Font(None, 65)
        self.large_font = pygame.font.Font(None, 110)
        self.size = size
        self.board = board
        self.screen = screen

        self.first_text = 'Синий'
        self.second_text = 'Оранжевый'

        self.text_1 = self.larger_font.render(self.first_text, True, color(self.color1))
        self.text_2 = self.larger_font.render(self.second_text, True, color(self.color2))

        self.first_text_coords = ((self.size[0] - self.board) / 4 - self.text_1.get_width() / 2, 100)
        self.second_text_coords = (self.size[0] - (self.size[0] - self.board) / 4 - self.text_2.get_width() / 2, 100)
        self.broom_image = Main.GetImage('broom2.png').load_image()
        self.shovel_image = Main.GetImage('shovel2.png').load_image()

        self.turn_marker = self.larger_font.render('ВАШ ХОД', True, color('brown'))
        self.turn_marker_1_coords = ((self.size[0] - self.board) / 4 - self.turn_marker.get_width() / 2, 200)
        self.turn_marker_2_coords = (self.size[0] - (self.size[0] - self.board) / 4 - self.turn_marker.get_width() / 2, 200)

    def draw(self,  game, player_1, player_2):
        self.screen.blit(self.text_1, self.first_text_coords)
        self.screen.blit(self.text_2, self.second_text_coords)

        self.draw_points(game)

        self.draw_turns(game)

        self.draw_tools(player_1, player_2)

    def draw_points(self, game):
        points_1 = self.font.render(str(game.first_points), True, color(self.color1))
        points_2 = self.font.render(str(game.second_points), True, color(self.color2))

        first_points_coords = ((self.size[0] - self.board) / 4 - points_1.get_width() / 2, 150)
        second_points_coords = (self.size[0] - (self.size[0] - self.board) / 4 - points_2.get_width() / 2, 150)

        pygame.draw.rect(self.screen, color('white'), first_points_coords + (points_1.get_width(), points_1.get_height()))
        self.screen.blit(points_1, first_points_coords)
        pygame.draw.rect(self.screen, color('white'), second_points_coords + (points_2.get_width(), points_2.get_height()))
        self.screen.blit(points_2, second_points_coords)

    def draw_turns(self, game):
        if game.get_turn() == 1:
            self.screen.blit(self.turn_marker, self.turn_marker_1_coords)
            pygame.draw.rect(self.screen, color('white'), self.turn_marker_2_coords +
                             (self.turn_marker.get_width(), self.turn_marker.get_height()))
        else:
            self.screen.blit(self.turn_marker, self.turn_marker_2_coords)
            pygame.draw.rect(self.screen, color('white'), self.turn_marker_1_coords +
                             (self.turn_marker.get_width(), self.turn_marker.get_height()))

    def draw_tools(self, player_1, player_2):
        if player_1.tool == 1:
            self.screen.blit(self.broom_image, ((self.size[0] - self.board) / 4 - 150 / 2, 250))
        else:
            self.screen.blit(self.shovel_image, ((self.size[0] - self.board) / 4 - 150 / 2, 250))

        if player_2.tool == 1:
            self.screen.blit(self.broom_image, (self.size[0] - (self.size[0] - self.board) / 4 - 150 / 2, 250))
        else:
            self.screen.blit(self.shovel_image, (self.size[0] - (self.size[0] - self.board) / 4 - 150 / 2, 250))

    def draw_ending_screen(self, win):
        if win == 3:
            pygame.draw.rect(self.screen, self.color1, (0, self.size[1] / 3 * 2, self.size[0], self.size[1] / 4), 0)
            pygame.draw.rect(self.screen, self.color2, (self.size[0] / 2, self.size[1] / 3 * 2, self.size[0], self.size[1] / 4), 0)

            win_word = self.large_font.render('НИЧЬЯ', True, color('brown'))
            win_word_coords = (self.size[0] / 2 - win_word.get_width() / 2, self.size[1] / 3 * 2 + self.size[1] / 10)
            self.screen.blit(win_word, win_word_coords)
        elif win == 1:
            pygame.draw.rect(self.screen, self.color1, (0, self.size[1] / 3 * 2, self.size[0], self.size[1] / 4), 0)

            win_word = self.large_font.render('ПОБЕДИЛ СИНИЙ', True, color('brown'))
            win_word_coords = (self.size[0] / 2 - win_word.get_width() / 2, self.size[1] / 3 * 2 + self.size[1] / 10 - win_word.get_height() / 2)
            self.screen.blit(win_word, win_word_coords)
        elif win == 2:
            pygame.draw.rect(self.screen, self.color2, (0, self.size[1] / 3 * 2, self.size[0], self.size[1] / 4), 0)

            win_word = self.large_font.render('ПОБЕДИЛ ОРАНЖЕВЫЙ', True, color('brown'))
            win_word_coords = (self.size[0] / 2 - win_word.get_width() / 2, self.size[1] / 3 * 2 + self.size[1] / 10 - win_word.get_height() / 2)
            self.screen.blit(win_word, win_word_coords)

    def ending(self, winner):
        if winner == 3:
            self.draw_ending_screen(3)
        elif winner == 1:
            self.draw_ending_screen(1)
        elif winner == 2:
            self.draw_ending_screen(2)




