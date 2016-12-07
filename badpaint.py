# Copyright 2016 Zara Zaimeche

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This exists because it shouldn't exist.

import sys, pygame
from pygame.locals import *
from sampleconfig import *

WINDOWWIDTH = WIDTH
WINDOWHEIGHT = HEIGHT

COLUMNS = WINDOWWIDTH /10
ROWS = WINDOWHEIGHT /10

PAINTSIZE = 50

RED = Color('red')
YELLOW = Color('orange')
GREEN = Color('green')
BLUE = Color('blue')
BLACK = Color('black')
WHITE = Color('white')

palette_x = COLUMNS - PAINTSIZE

window_surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

red_square = {"rect":pygame.Rect(palette_x, 0, PAINTSIZE, PAINTSIZE), "colour":RED}
yellow_square = {"rect":pygame.Rect(palette_x, 51, PAINTSIZE, PAINTSIZE), "colour":YELLOW}

green_square = {"rect":pygame.Rect(palette_x, 102, PAINTSIZE, PAINTSIZE), "colour":GREEN}

blue_square = {"rect":pygame.Rect(palette_x, 153, PAINTSIZE, PAINTSIZE), "colour":BLUE}

black_square = {"rect":pygame.Rect(palette_x, 204, PAINTSIZE, PAINTSIZE), "colour":BLACK}

white_square = {"rect":pygame.Rect(palette_x, 255, PAINTSIZE, PAINTSIZE), "colour": WHITE}

squares = [red_square, yellow_square, green_square, blue_square, black_square, white_square]

window_surface.fill(WHITE)

splodge_colour = BLACK
splodges = []

while True == True:
    for square in squares:
        pygame.draw.rect(window_surface, square["colour"], square["rect"])

    for event in pygame.event.get():
        if event.type == QUIT:
            print 'Saving your masterpiece to %s!' % SAVEFILE
            pygame.image.save(window_surface, SAVEFILE)
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN:
            no_paint = False
            mousex, mousey = pygame.mouse.get_pos()
            for square in squares:
                if square["rect"].collidepoint((mousex, mousey)):
                    splodge_colour = square["colour"]
                    no_paint = True
              
            if no_paint == False:
                splodge = {"rect":pygame.Rect(mousex, mousey, PAINTSIZE, PAINTSIZE), "colour": splodge_colour}
                splodges.append(splodge)

        for splodge in splodges:
            pygame.draw.ellipse(window_surface, splodge["colour"], splodge["rect"])
        pygame.display.update()
