# This file was created by: Jude Hammers
# This code was inspired by Zelda and informed by Chris Bradfield

import pygame as pg
from settings import *
from settings import TILESIZE
from settings import GREEN
from settings import BROWN
from settings import PLAYER_SPEED
# allows us to use pygame
# imports game settings

# player class
class Player:
    # creates the blueprint for the player
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        # initializes the player class
        pg.sprite.Sprite.__init__(self, self.groups)
        # init super class
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # setting player dimensions
        self.image.fill(GREEN)
        # setting player color
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0,0
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a:]:
            self.vx =PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED  
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED  
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
    
    # def move(self, dx=0, dy=0):
    #     if not self.collide_with_walls(dx, dy):
    #         self.x += dx
    #         self.y += dy

    # def collide_with_walls(self, dx=0, dy=0):
    #     for wall in self.game.walls:
    #         if wall.x == self.x + dx and wall.y == self.y + dy:
    #             return True
    #     return False
    
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
    # placeholder for later code

# wall class

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # add wall to groups via the Sprite class parameter
        self.groups = game.all_sprites, game.walls
        # init superclass
        pg.sprite.Sprite.__init__(self, self.groups)
        # add game to properties of wall class
        self.game = game
        # setup image in pygame using Surface class
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # fill the image
        self.image.fill(BLUE)
        # get the rectangular dimensions and locations using the get_rect method
        self.rect = self.image.get_rect()
        # create the x and y coordinate properties for use below
        self.x = x
        self.y = y
        # set the x and y coordinate properties using the rect from get_rect
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
