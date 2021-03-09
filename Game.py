import pygame
import os
from pygame import Color as color
import random
import HUD


class Game:
    def __init__(self, tiles, hud, sound_profile):
        self.turn = 1
        self.tiles_max = tiles
        self.cur_tile = 0
        self.first_points = 0
        self.second_points = 0
        self.hud = hud
        self.sound_profile = sound_profile
        self.blue_moved = False
        self.orange_moved = False
        self.forfeited = False
        self.won = False

    def get_turn(self):
        return self.turn

    def change_turn(self):
        if self.turn == 1:
            self.turn = 2
            print('ХОД ВТОРОГО ИГРОКА')
        else:
            self.turn = 1
            print('ХОД ПЕРВОГО ИГРОКА')

    def get_point(self, player):
        self.cur_tile += 1
        if player == 1:
            self.first_points += 1
        else:
            self.second_points += 1

    def check_end(self):
        end = False
        if self.tiles_max == self.cur_tile:
            end = True

        if end:
            if self.first_points > self.second_points:
                self.hud.ending(1)
            if self.first_points < self.second_points:
                self.hud.ending(2)
            if self.first_points == self.second_points:
                self.hud.ending(3)
            if not self.won:
                self.sound_profile.win()
                self.won = True
            return True
        elif self.forfeited:
            return True
        else:
            return False

    def forfeit(self, player):
        if player == 1:
            self.hud.ending(2)
        else:
            self.hud.ending(1)
        self.sound_profile.win()
        self.forfeited = True




