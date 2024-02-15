# This file was created by Jude Hammers

# import modules
import pygame as pg
from settings import *
from settings import TITLE
from settings import TILESIZE
from settings import BROWN
from settings import GREEN
from settings import LIGHTGREY
from settings import BGCOLOR
from settings import BLUE
from settings import BLACK
from random import randint
from sprites import *
from sprites import Wall
import sys
from os import path

# creating the game blueprint
class Game:
    # Initializer -- info about the game
    def __init__(self):
        # initializes pygame
        pg.init()
        # settings
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # Setting up pygame clock
        self.clock = pg.time.Clock()
        self.load_data()
    def load_data(self):
         game_folder = path.dirname(__file__)
         self.map_data = []
         '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
         with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
    # Game loop -- runs our game
                
    def new(self):
            print("create new game...")
            self.all_sprites = pg.sprite.Group()
            self.walls = pg.sprite.Group()
            # self.player1 = Player(self, 1, 1)
            # for x in range(10, 20):
            #     Wall(self, x, 5)
            for row, tiles in enumerate(self.map_data):
                print(row)
                for col, tile in enumerate(tiles):
                    print(col)
                    if tile == '1':
                        print("a wall at", row, col)
                        Wall(self, col, row)
                    if tile == 'P':
                        self.player = Player(self, col, row)


    def run(self):
            # game loop - set self.playing = False to end the game
            self.playing = True
            while self.playing:
                self.dt = self.clock.tick(FPS) / 1000
                self.events()
                self.update()
                self.draw()
    def quit(self):
            pg.quit()
            sys.exit()

    def update(self):
            # update portion of the game loop
            self.all_sprites.update()
        
    def draw_grid(self):
            for x in range(0, WIDTH, TILESIZE):
                pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, TILESIZE):
                pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
            self.screen.fill(BGCOLOR)
            self.draw_grid()
            self.all_sprites.draw(self.screen)
            # self.draw_text(self.screen, "Hello world", 42, BLACK, 2, 2)
            self.draw_text(self.screen, str(self.dt), 42, BLACK, 1, 1)
            pg.display.flip()

    def events(self):
            # catch all events here
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_A:
                #           self.player.move(dx=-1)
                #     if event.key == pg.K_D:
                #           self.player.move(dx=1)
                #     if event.key == pg.K_W:
                #           self.player.move(dy=-1)
                #     if event.key == pg.K_S:
                #           self.player.move(dy=1)
                #     if event.key == pg.K_ESCAPE:
                #         self.quit()

    def draw_text(self, surface, text, size, color, x, y):
            font_name = pg.font.match_font('arial')
            font = pg.font.Font(font_name, size)
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.topleft = (x*TILESIZE,y*TILESIZE)
            surface.blit(text_surface, text_rect)

    #>>>>>>>>>>>>>>>>>>>>>OUTPUT<<<<<<<<<<<<<<<<<<<<
    
g = Game()
# g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen