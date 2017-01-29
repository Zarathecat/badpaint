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

# We use black and white alone a lot for outlines
WHITE = Color('white')
BLACK = Color('black')

# Background is white by default
fill_colour = WHITE

# Fill square outline
fill_outline = WHITE

# Paint is black by default
splodge_colour = BLACK

# Colour of button outlines
outline_colour = BLACK

# The square paint buttons that a user can select to change brush colour

def make_colours(colours_list):
    colours = []
    for i in colours_list:
        colour = Color(i)
        colours.append(colour)
    return colours

colours = make_colours(colour_names)

def make_paint_squares(colour_list):
    squares = []
    for i in range(len(colour_list)):
        colour = colour_list[i]  # the RGB value
        dimensions = 0, i * PAINTSIZE + i * GAPSIZE, PAINTSIZE, PAINTSIZE
        new_square = {"rect":pygame.Rect(dimensions), 'colour': colour}
        squares.append(new_square)
    return squares

squares = make_paint_squares(colours)


# The circles that the user can click to select brush size. These are below
# the paint-colour-select squares.
 
# Get last square's y coordinate, so we can put brushes relative to it.
last_square_y = squares[-1]['rect'][1]
brush_y = last_square_y + PAINTSIZE + GAPSIZE

# The brushes are offset from left relative to their size so they're lazily
# centered under each other. Their y coordinate is worked out relative
# to the previous brushes (and paint squares)

big_brush_y = brush_y
med_brush_y = brush_y + big_brush
small_brush_y = brush_y + big_brush + med_brush

big_brush_dimensions = 1, big_brush_y, big_brush, big_brush
med_brush_dimensions = 10, med_brush_y, med_brush, med_brush
small_brush_dimensions = 20, small_brush_y, small_brush, small_brush

big_brush_rect = {"rect":pygame.Rect(big_brush_dimensions), "size":big_brush}
med_brush_rect = {"rect":pygame.Rect(med_brush_dimensions), "size":med_brush}
small_brush_rect = {"rect":pygame.Rect(small_brush_dimensions), "size":small_brush}

brushes = [big_brush_rect, med_brush_rect, small_brush_rect]


window_surface.fill(fill_colour)

# As the user paints, paint splodges will be added to this array
splodges = []

stop_painting = True #don't paint until asked to paint

def remove_overlaps(paint, ui_elements):
    for splodge in paint[:]:
        for element in ui_elements[:]:
            if splodge["rect"].colliderect(element["rect"]):
                paint.remove(splodge)
                break

while True == True:
    pygame.display.update()

    # This is the square the user can click to change the background colour.
    # We put it here so its colour will change dynamically to match the
    # selected paint colour, so the user can see what colour they will fill
    # the background.
    fill_square_y = small_brush_y + small_brush + GAPSIZE
    fill_square_rect = pygame.Rect(0, fill_square_y, PAINTSIZE, PAINTSIZE)
    fill_square = {"rect":fill_square_rect, "colour":splodge_colour}

    # draw paint palette to screen
    for square in squares:

        # give squares an outline so that the one matching the background colour
        # doesn't 'disappear'
        square_left = square["rect"][0]
        square_top = square["rect"][1]
        square_size = PAINTSIZE+outline
        square_dimensions = square_left, square_top, square_size, square_size
        pygame.draw.rect(window_surface, outline_colour, (square_dimensions))

        #draw paint palette squares
        pygame.draw.rect(window_surface, square["colour"], square["rect"])

    # draw paint brushes to screen
    for brush in brushes:
        pygame.draw.ellipse(window_surface, outline_colour, brush["rect"], outline)

    # draw outline for square that fills the background to screen
    fill_left = fill_square["rect"][0] - 2 # -2 so it gets more of a border
    fill_top = fill_square["rect"][1] - 2 # same again
    fill_size = PAINTSIZE+outline
    fill_square_dimensions = fill_left, fill_top, fill_size, fill_size
    pygame.draw.rect(window_surface, fill_outline, (fill_square_dimensions))

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
            stop_painting = False  # toggling lets the user drag to paint

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

        # this makes the splodge top-left appear above and to the left of the
        # click, so the point is in the center of the splodge
        mouse_up = mousex-brush_size/2
        mouse_left = mousey-brush_size/2

        splodge_dimensions = (mouse_up, mouse_left, brush_size, brush_size)
        splodge_rect = pygame.Rect(splodge_dimensions)
        splodge = {"rect":splodge_rect, "colour": splodge_colour}
        splodges.append(splodge)

    
    # rather than blocking the user from painting in squares occupied by
    # buttons, it's easier to let them and then just delete those paint
    # splodges before drawing the picture to the screen

    # remove paint overlapping palette
    remove_overlaps(splodges, squares)

    # remove paint overlapping brushes
    remove_overlaps(splodges, brushes)

    # remove paint overlapping fill square
    for splodge in splodges[:]:
        if splodge["rect"].colliderect(fill_square["rect"]):
            splodges.remove(splodge)

    # draw picture-so-far to screen
    for splodge in splodges:
        pygame.draw.ellipse(window_surface, splodge["colour"], splodge["rect"])
