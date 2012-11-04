import pygame
import colorsys
from folder import *
from random import randrange, uniform
import random


def colour_palette(n, rand=True):
    '''(int, bool) -> tuple
    Generates and yields n number of RGB tuples, if rand flag is True then
    random colours, if False then RGB tuples are different variations of a
    single colour.'''

    if n == 0:
        return
    if rand is True:
        for rgb in [(randrange(50, 200), randrange(50, 200), \
                     randrange(50, 200)) for x in range(n)]:
            yield rgb
    else:
        hue = uniform(0.0, 360.0) / n  # Selects random hue (colour).
        for hsv in [(hue, uniform(0.5, 1.0), uniform(0.5, 1.0)) \
                    for x in range(n)]:  # Creates list of variations.
            rgb = tuple([x * 255 for x in colorsys.hsv_to_rgb(*hsv)])
            yield rgb


def tile(t, x, y, width, height, screen, rand_colour=True, colour=None):
    '''(tree, int, int, int, int, Surface, bool, tuple) -> NoneType
    Displays a tile representation of a treemap of some given directory. If
    rand_colour flag is False, then all files of a directory are filled with
    variations of a single colour, else if True then random colours.'''

    if height == 0 or width == 0:
        return

    if t:
        t.cord = (x, y, x + width, y + height)

        if type(t) is File:
            pygame.draw.rect(screen, colour, (x, y, width, height))

        elif type(t) is Folder:
            area = width * height
            rect = (x, y, width, height)
            c = colour_palette(len(t.items), rand_colour)

            for item in t.items:
                scale = float(item.size) / t.size
                item_area = area * scale

                if width > height:
                    width_needed = item_area / height
                    tile(item, x, y, width_needed, height, screen, \
                         rand_colour, c.next())
                    x += width_needed
                    width -= width_needed
                else:
                    height_needed = item_area / width
                    tile(item, x, y, width, height_needed, screen, \
                         rand_colour, c.next())
                    y += height_needed
                    height -= height_needed

            pygame.draw.rect(screen, (255, 255, 255), rect, 1)


def square(t, width, height, screen, x=0, y=0):
    '''(tree, int, int, Surface, int, int) -> Surface
        Displays a squarified tile representation of a treemap of some given
        directory.'''
    scale = float(width * height) / t.size
    _w = width
    _h = height
    locked_items = []
    if t.items == []:
        pass
    else:
        ratio = 0
        for item in t.items:
            # Calculate the aspect_ratio of current item added to locked item.
            new_ratio = aspect_ratio(locked_items + [item], \
                                     min(width, height), scale)
            # If new ratio is closer to 1 than old ratio, check for next item.
            if ratio == 0 or ratio > new_ratio:
                ratio = new_ratio
                locked_items += [item]
                continue
            else:
                # If the best possible ratio is found, lock the items in list
                # locked_items onto the screen.
                _screen = lock_display(locked_items, width, height, scale)
                screen.blit(_screen, (x, y))
                # Calculate the remaining space available to be filled.
                if width > height:
                    width -= _screen.get_size()[0]
                    x += _screen.get_size()[0]
                else:
                    height -= _screen.get_size()[1]
                    y += _screen.get_size()[1]
                # Repeat the process, until no more items in the list.
                locked_items = [item]
                ratio = aspect_ratio(locked_items, min(width, height), scale)

        if locked_items != []:
            _screen = lock_display(locked_items, width, height, scale)
            screen.blit(_screen, (x, y))
            pygame.draw.rect(screen, (255, 255, 255), (0, 0, _w, _h), 1)
        return screen.copy()


def lock_display(locked_items, width, height, scale):
    '''(list, int, int, float) -> Surface
    Returns a new surface built with trees in locked_items'''
    if width == 0 or height == 0:
        return pygame.Surface((width, height))
    x, y = 0, 0
    if width > height:  # Checks whether available space is wide or long.
        width_needed = _total_size(locked_items, scale) / int(height)
        _screen = pygame.Surface((width_needed, height))
    else:
        height_needed = _total_size(locked_items, scale) / int(width)
        _screen = pygame.Surface((width, height_needed))

    if 0 in _screen.get_size():  # Checks if the dimensions are too small.
        return _screen
    # Go through each item in locked_items and fits them on the subscreen.
    for item in locked_items:
        if width > height:
            height_needed = int(item.size * scale) / width_needed
        else:
            width_needed = int(item.size * scale) / height_needed
        if item.items == []:
            pygame.draw.rect(_screen, rand_color(), (x, y, width_needed, \
                                                      height_needed))
        # if the item has children, squarify the item and get the surface
        # of the current item.
        else:
            _screen2 = pygame.Surface((width_needed, height_needed))
            _screen2 = square(item, width_needed, height_needed, _screen2)
            _screen.blit(_screen2, (x, y))
        item.cord = [x, y, x + width_needed, y + height_needed]
        if width > height:
            y += height_needed
        else:
            x += width_needed
    return _screen


def aspect_ratio(R, w, scale):
    '''(list, int, float) -> float
        Returns the aspect ratio of items in list R on the shortest side
        of the available space w.'''
    _R = []
    for i in R:  # Scale all the item in R.
        if i != None:
            _R += [i.size * scale]
    if R == []:
        return 0
    else:
        try:
            return max((w ** 2.0 * max(_R)) / (sum(_R) ** 2), \
                   (sum(_R) ** 2.0) / (w ** 2 * min(_R)))
        except Exception:
            return 0


def rand_color():
    '''(None) -> tuple
    Returns a random color in the form of a tuple.'''
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)


def _total_size(items, scale):
    '''(list, float) -> list
    Returns the scaled sum of all the items in list items.'''
    sum = 0
    for i in items:
        sum += i.size * scale
    return int(sum)
