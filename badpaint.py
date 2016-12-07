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

fill_colour = WHITE
stop_painting = True
palette_x = 0

window_surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

red_square = {"rect":pygame.Rect(palette_x, 0, PAINTSIZE, PAINTSIZE), "colour":RED}
yellow_square = {"rect":pygame.Rect(palette_x, 51, PAINTSIZE, PAINTSIZE), "colour":YELLOW}

green_square = {"rect":pygame.Rect(palette_x, 102, PAINTSIZE, PAINTSIZE), "colour":GREEN}

blue_square = {"rect":pygame.Rect(palette_x, 153, PAINTSIZE, PAINTSIZE), "colour":BLUE}

black_square = {"rect":pygame.Rect(palette_x, 204, PAINTSIZE, PAINTSIZE), "colour":BLACK}

white_square = {"rect":pygame.Rect(palette_x, 255, PAINTSIZE, PAINTSIZE), "colour": WHITE}


big_brush = 80
med_brush = 40
small_brush = 20

big_brush_rect = {"rect":pygame.Rect(palette_x + 1, 260 + big_brush, big_brush, big_brush), "size":big_brush}
med_brush_rect = {"rect":pygame.Rect(palette_x + 10, 260 + big_brush + big_brush, med_brush, med_brush), "size":med_brush}
small_brush_rect = {"rect":pygame.Rect(palette_x + 20, 260+big_brush+big_brush+med_brush, small_brush, small_brush), "size":small_brush}

brushes = [big_brush_rect, med_brush_rect, small_brush_rect]

squares = [red_square, yellow_square, green_square, blue_square, black_square, white_square]

window_surface.fill(fill_colour)

splodge_colour = BLACK
splodges = []

brush_size = 50 #default

while True == True:
    pygame.display.update()

    fill_square = {"rect":pygame.Rect(palette_x, 500, PAINTSIZE, PAINTSIZE), "colour":splodge_colour}


    for square in squares:
        pygame.draw.rect(window_surface, BLACK, (square["rect"][0], square["rect"][1], PAINTSIZE+5, PAINTSIZE+5))
        pygame.draw.rect(window_surface, square["colour"], square["rect"])
    for brush in brushes:
        pygame.draw.ellipse(window_surface, BLACK, brush["rect"], 5)
    pygame.draw.rect(window_surface, fill_square["colour"], fill_square["rect"])

    for event in pygame.event.get():
        if event.type == QUIT:
            print 'Saving your masterpiece to %s!' % SAVEFILE
            window_surface.fill(fill_colour)
            for splodge in splodges:
                pygame.draw.ellipse(window_surface, splodge["colour"], splodge["rect"])
            pygame.image.save(window_surface, SAVEFILE)
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN:
            no_paint = False
            stop_painting = False
            mousex, mousey = pygame.mouse.get_pos()
            for square in squares:
                if square["rect"].collidepoint((mousex, mousey)):
                    splodge_colour = square["colour"]
                    no_paint = True

            for brush in brushes:
                if brush["rect"].collidepoint((mousex, mousey)):
                    brush_size = brush["size"]
                    no_paint = True

            if fill_square["rect"].collidepoint((mousex, mousey)):
                fill_colour = splodge_colour
                no_paint = True
                window_surface.fill(fill_colour)
              
            if no_paint == False:
                splodge = {"rect":pygame.Rect(mousex-brush_size/2, mousey-brush_size/2, brush_size, brush_size), "colour": splodge_colour}
                splodges.append(splodge)

            for splodge in splodges:
                pygame.draw.ellipse(window_surface, splodge["colour"], splodge["rect"])
        if event.type == MOUSEBUTTONUP:
            stop_painting = True
    if stop_painting == False:
        mousex, mousey = pygame.mouse.get_pos()
        splodge = {"rect":pygame.Rect(mousex-brush_size/2, mousey-brush_size/2, brush_size, brush_size), "colour": splodge_colour}
        splodges.append(splodge)

        for splodge in splodges[:]:
            for square in squares[:]:
                if splodge["rect"].colliderect(square["rect"]):
                    splodges.remove(splodge)
                    break

        for splodge in splodges[:]:
            for brush in brushes[:]:
                if splodge["rect"].colliderect(brush["rect"]):
                    splodges.remove(splodge)
                    break

        if splodge["rect"].colliderect(fill_square["rect"]):
            splodges.remove(splodge)

        for splodge in splodges:
            pygame.draw.ellipse(window_surface, splodge["colour"], splodge["rect"])
