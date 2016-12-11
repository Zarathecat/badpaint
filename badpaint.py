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

window_surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))


PAINTSIZE = 50 #size of paint buttons, not brush

RED = Color('red')
YELLOW = Color('orange')
GREEN = Color('green')
BLUE = Color('blue')
BLACK = Color('black')
WHITE = Color('white')


# The square paint buttons that a user can select to change brush colour

red_square = {"rect":pygame.Rect(0, 0, PAINTSIZE, PAINTSIZE), "colour":RED}

yellow_square = {"rect":pygame.Rect(0, 51, PAINTSIZE, PAINTSIZE), "colour":YELLOW}

green_square = {"rect":pygame.Rect(0, 102, PAINTSIZE, PAINTSIZE), "colour":GREEN}

blue_square = {"rect":pygame.Rect(0, 153, PAINTSIZE, PAINTSIZE), "colour":BLUE}

black_square = {"rect":pygame.Rect(0, 204, PAINTSIZE, PAINTSIZE), "colour":BLACK}

white_square = {"rect":pygame.Rect(0, 255, PAINTSIZE, PAINTSIZE), "colour": WHITE}

squares = [red_square, yellow_square, green_square, blue_square, black_square, white_square]


big_brush = 80
med_brush = 40
small_brush = 20

# The circles that the user can click to select brush size. These are below
# the paint-colour-select squares.

big_brush_rect = {"rect":pygame.Rect(1, 260 + big_brush, big_brush, big_brush), "size":big_brush}

med_brush_rect = {"rect":pygame.Rect(10, 260 + big_brush + big_brush, med_brush, med_brush), "size":med_brush}

small_brush_rect = {"rect":pygame.Rect(20, 260+big_brush+big_brush+med_brush, small_brush, small_brush), "size":small_brush}

brushes = [big_brush_rect, med_brush_rect, small_brush_rect]


# Background is white by default

fill_colour = WHITE

window_surface.fill(fill_colour)

# Paint is black by default
splodge_colour = BLACK

# As the user paints, paint splodges will be added to this array
splodges = []

brush_size = med_brush #default

stop_painting = True #don't paint until asked to paint

while True == True:
    pygame.display.update()

    # This is the square the user can click to change the background colour.
    # We put it here so its colour will change dynamically to match the
    # selected paint colour, so the user can see what colour they will fill
    # the background.
    fill_square = {"rect":pygame.Rect(0, 500, PAINTSIZE, PAINTSIZE), "colour":splodge_colour}

    # draw paint palette to screen
    for square in squares:

        # give squares an outline so that the one matching the background colour
        # doesn't 'disappear'
        pygame.draw.rect(window_surface, BLACK, (square["rect"][0], square["rect"][1], PAINTSIZE+5, PAINTSIZE+5))

        #draw paint palette squares
        pygame.draw.rect(window_surface, square["colour"], square["rect"])

    # draw paint brushes to screen
    for brush in brushes:
        pygame.draw.ellipse(window_surface, BLACK, brush["rect"], 5)

    # draw outline for square that fills the background to screen
    pygame.draw.rect(window_surface, WHITE, (fill_square["rect"][0]-2, fill_square["rect"][1]-2, PAINTSIZE+5, PAINTSIZE+5))

    # draw fill square itself
    pygame.draw.rect(window_surface, fill_square["colour"], fill_square["rect"])

    # main event loop
    for event in pygame.event.get():
        if event.type == QUIT:

            # savefile is defined in config
            print 'Saving your masterpiece to %s!' % SAVEFILE

            # when the user is finished, we redraw the background so that the
            # paint palette does not appear in the final saved image
            window_surface.fill(fill_colour)

            # then we redraw the paint so they don't save a blank screen...
            for splodge in splodges:
                pygame.draw.ellipse(window_surface, splodge["colour"], splodge["rect"])
            pygame.image.save(window_surface, SAVEFILE)
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN:
            stop_painting = False #toggling lets the user drag to paint

            # get mouse position
            mousex, mousey = pygame.mouse.get_pos()

            # set paint colour if user clicks paint
            for square in squares:
                if square["rect"].collidepoint((mousex, mousey)):
                    splodge_colour = square["colour"]

            # set brush size if user clicks brush
            for brush in brushes:
                if brush["rect"].collidepoint((mousex, mousey)):
                    brush_size = brush["size"]

            # fill background if user clicks fill
            if fill_square["rect"].collidepoint((mousex, mousey)):
                fill_colour = splodge_colour
                window_surface.fill(fill_colour)
              

        # stop painting when user stops dragging the mouse
        if event.type == MOUSEBUTTONUP:
            stop_painting = True

    # add to list of paint to be drawn to screen while user drags mouse
    if stop_painting == False:
        mousex, mousey = pygame.mouse.get_pos()
        splodge = {"rect":pygame.Rect(mousex-brush_size/2, mousey-brush_size/2, brush_size, brush_size), "colour": splodge_colour}
        splodges.append(splodge)

    
    # rather than blocking the user from painting in squares occupied by
    # buttons, it's easier to let them and then just delete those paint
    # splodges before drawing the picture to the screen

    # remove paint overlapping palette
    for splodge in splodges[:]:
        for square in squares[:]:
            if splodge["rect"].colliderect(square["rect"]):
                splodges.remove(splodge)
                print "removing..."
                break

    # remove paint overlapping brushes
    for splodge in splodges[:]:
        for brush in brushes[:]:
            if splodge["rect"].colliderect(brush["rect"]):
                print splodge["rect"], brush["rect"]
                splodges.remove(splodge)
                print splodges
                break

    # remove paint overlapping fill square
    for splodge in splodges[:]:
        if splodge["rect"].colliderect(fill_square["rect"]):
            splodges.remove(splodge)

    # draw picture-so-far to screen
    for splodge in splodges:
        pygame.draw.ellipse(window_surface, splodge["colour"], splodge["rect"])
