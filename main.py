import pygame as pg
from settings import *
from settings import TITLE, TILESIZE, BROWN, GREEN, LIGHTGREY, BGCOLOR, BLUE, BLACK
from random import randint
from sprites import *
from sprites import Wall, PowerUp, Mob2, Player, Hostage, DropPoint
import sys
from os import path

# initial game goals: death after mob collision, start screen, speed power up
# beta goal: player reflection across screens like in pacman
# final goal: player score + "save the hostage" game feature

# class definition for the game
class Game:
    def __init__(self):
        pg.init()  # initialize pygame
        # set up the game window with width and height defined in settings
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        # load and scale background image
        self.background_image = pg.image.load("pcbg.jpg")
        self.background_image = pg.transform.scale(self.background_image, (WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)  # name the game title
        self.clock = pg.time.Clock()  # create a clock object to manage frame rate
        self.load_data()  # load game data from files on surface
        self.carrying_hostage = False
        self.player_group = pg.sprite.Group()  # create a group for the player

    def load_data(self):
        # load map data from the map.txt text file
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)

    def new(self):
        # set up a new game, creating sprites and groups
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.hostages = pg.sprite.Group()
        self.drop_points = pg.sprite.Group()
        # parse the map data
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)  # place wall
                elif tile == 'P':
                    self.player = Player(self, col, row)  # create player
                    self.player_group.add(self.player)  # add player to player group
                elif tile == 'C':
                    PowerUp(self, col, row)  # place power-up
                elif tile == 'M':
                    Mob2(self, col, row)  # place mob
                elif tile == 'H':
                    Hostage(self, col, row)  # place hostage
                elif tile == 'D':
                    DropPoint(self, col, row)  # place drop point

    def show_end_screen(self):
        # Display the "You won!" screen
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "You won!", 48, BLUE, WIDTH / 3.5, HEIGHT / 2)  # draw "You won!" text
        self.draw_text(self.screen, "Press any key to play again", 22, BLACK, WIDTH / 4, HEIGHT * 3 / 4)  # draw play again text
        pg.display.flip()
        self.wait_for_key()

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000  # manage game time
            self.events()  # process game events
            self.update()  # update game
            self.draw()  # draw the game
        self.show_end_screen()  # show the end screen after the game loop ends

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update all sprites
        self.all_sprites.update()
        # check for collisions between the player and any mobs
        if pg.sprite.spritecollideany(self.player, self.mobs):
            self.playing = False  # end game on collision
        # hostage_pickup_hits = pg.sprite.spritecollide(self.player, self.hostages, False)
        # if hostage_pickup_hits and not self.player.carrying_hostage:
        #     self.player.pick_up_hostage()

    def events(self):
        # handle all events from the user and system
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

    def draw(self):
        # draw the background and all sprites
        self.screen.blit(self.background_image, (0, 0))
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()  # update the display

    def draw_grid(self):
        # draw a grid over the game window
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw_text(self, surface, text, size, color, x, y):
        # utility function to draw text on the screen
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_surface, text_rect)

    def show_start_screen(self):
        # display the start screen
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "Press any button to start game", 48, BLUE, WIDTH / 4.3, HEIGHT / 2.2)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        # wait for a key press to proceed
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

# main part of the program
screen = pg.display.set_mode((WIDTH, HEIGHT))
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
