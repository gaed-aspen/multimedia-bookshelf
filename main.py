import os
import json
import random
from math import floor
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame



class Colours:
    # Basic greys
    BLACK_MONO = (0, 0, 0)
    GREY_MONO = (50, 50, 50)
    LIGHT_MONO = (87, 87, 87)
    WHITE_MONO = (200, 200, 200)

    # Solid Colours
    RED_SOLID = (255, 0, 0)
    GREEN_SOLID = (0, 255, 0)
    BLUE_SOLID = (0, 0, 255)

    # Pastels
    RED_PASTEL = (100, 50, 50)
    GREEN_PASTEL = (50, 100, 50)
    BLUE_PASTEL = (50, 50, 100)

    # Program-wide colours
    BACKGROUND = GREY_MONO

    # Collection of all colours
    all_colours = dict()
    solid = dict()
    pastel = dict()
    mono = dict()

    def __init__(self):
        # Find all defined colours, then sort them into the correct dict.
        # Colours that are declared first are matched first. E.g. red = solid red, not pastel red
        colours = dict()
        self.types = dict()
        for name in dir(Colours):
            obj = eval('Colours.'+name)
            if type(obj) == tuple:
                ctype = name.lower().split('_')[-1]
                if colours.get(ctype) != None:
                    colours[ctype].append((name, obj))
                else:
                    colours[ctype] = [(name, obj)]
            elif type(obj) == dict:
                self.types[name.lower()] = obj

        for name in colours.keys():
            for cname, colour in colours[name]:
                lcname = cname.lower()
                coltyp = lcname.replace('_', '')            # For 'red solid'
                typcol = ''.join(lcname.split('_')[::-1])   # For 'solid red'
                col = lcname.split('_')[0]                  # For 'red'
                self.all_colours[coltyp] = colour
                self.all_colours[typcol] = colour
                self.all_colours[col] = colour
                if name in self.types.keys():
                    self.types[name][coltyp] = colour
                    self.types[name][typcol] = colour
                    self.types[name][col] = colour

    def get_match(self, name, default):
        name = name.lower().replace('_', '').replace(' ', '')
        return self.all_colours.get(name, default)

    def get_all(self, ctype):
        ctype = self.types.get(ctype, self.all_colours)
        return list(ctype.values())


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

BORDER_WIDTH = 10
BORDER_HEIGHT = 10
SHELF_SPACING = 200

font = None

TEXT = (200, 200, 200)
SHELF = (100, 100, 100)


def Lerp(start, end, pct):
    pct = min(1, max(0, pct))
    return start + (end-start) * pct


def EaseIn(time):
    return time*time


def EaseOut(time):
    return Flip(EaseIn(Flip(time)))


def Flip(x):
    return 1 - x


def init():
    global font
    pygame.init()
    pygame.font.init()

    documents, items = load_documents(os.path.join(os.getcwd(), 'assets'))

    flags = pygame.RESIZABLE | pygame.DOUBLEBUF
    window = pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT), flags=flags)
    clock = pygame.time.Clock()
    font = pygame.font.Font('assets/fonts/OpenSans-Light.ttf', 20)

    # Setup start objects
    info_text = font.render(
        "Please full screen program on the display of choice, then press start", True, (200, 200, 200))
    start_text = font.render("Start", True, (200, 200, 200))

    sb_width = start_text.get_width()*2
    sb_height = start_text.get_height()*1.75
    sb_foreground_width = sb_width-4
    sb_foreground_height = sb_height-4
    start_button = pygame.Surface(
        (start_text.get_width()*2, start_text.get_height()*1.75))
    start_button.fill(Colours.BACKGROUND)
    pygame.draw.rect(start_button, (10, 10, 10), pygame.Rect(
        0, 0, sb_width, sb_height), border_radius=5)
    pygame.draw.rect(start_button, (50, 50, 50), pygame.Rect(
        2, 2, sb_foreground_width, sb_foreground_height), border_radius=5)

    tx = int((WINDOW_WIDTH / 2)-(info_text.get_width() / 2))
    ty = int((WINDOW_HEIGHT / 2)-(info_text.get_height() / 2))
    bx = int((WINDOW_WIDTH / 2)-(start_button.get_width() / 2))
    by = int((WINDOW_HEIGHT / 2)-(start_button.get_height() / 2))
    btx = int((WINDOW_WIDTH / 2)-(start_text.get_width() / 2))
    bty = int((WINDOW_HEIGHT / 2)-(start_text.get_height() / 2))

    text_start = tx, ty
    text_end = tx, ty - 75
    bt_start = btx, bty
    bt_end = btx, bty + 75
    bs_start = bx, by
    bs_end = bx, by + 75

    animation_duration = 500  # ms
    lerp_function = EaseOut

    start_time = pygame.time.get_ticks()
    current_time = 1
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                button_rect = bs_end[0], bs_end[0] + \
                    sb_width, bs_end[1], bs_end[1] + sb_height
                if button_rect[0] < position[0] and position[0] < button_rect[1]:
                    if button_rect[2] < position[1] and position[1] < button_rect[3]:
                        running = False
                        continue

        current_time = max(pygame.time.get_ticks() - start_time, 1)

        pct = min(1 / (animation_duration / current_time), 1)

        text_pos = Lerp(text_start[0], text_end[0], lerp_function(pct)), Lerp(
            text_start[1], text_end[1], lerp_function(pct))
        bt_pos = Lerp(bt_start[0], bt_end[0], lerp_function(pct)), Lerp(
            bt_start[1], bt_end[1], lerp_function(pct))
        bs_pos = Lerp(bs_start[0], bs_end[0], lerp_function(pct)), Lerp(
            bs_start[1], bs_end[1], lerp_function(pct))

        opacity = int(Lerp(0, 255, EaseIn(pct)))

        # Update and render
        window.fill((50, 50, 50))

        info_text.set_alpha(opacity)
        start_text.set_alpha(opacity)

        window.blit(info_text, text_pos)
        window.blit(start_button, bs_pos)
        window.blit(start_text, bt_pos)

        pygame.display.update()

    return window, clock, documents, items


def load_documents(source_directory):
    if not os.path.exists(source_directory):
        print('Files not found')
        return
    cwd = os.path.abspath(source_directory)

    documents = list()
    items = []

    for item in os.listdir(cwd):
        if not os.path.isfile(os.path.join(cwd, item)):
            continue

        documents.append(os.path.join(cwd, item))

    for document in documents:
        loaded_doc = json.load(open(document))
        loaded_doc['assets'] = dict()

        files = loaded_doc.get('files')
        embeds = loaded_doc.get('embeds', dict())

        assets = dict()
        assets['main'] = files.get('main')
        for file in embeds:
            assets[file] = embeds.get(file)

        for file in assets:
            ftype, location = assets.get(file)
            path = os.path.join(cwd, location)
            if os.path.isfile(path):
                loaded_doc['assets'][file] = (ftype, path)
            else:
                print(
                    f'{path} does not exist. Please check that the file was linked correctly in {document}')

        items.append(loaded_doc)

    return documents, items


def compute_sizes():
    window_width, window_height = pygame.display.get_window_size()

    max_shelves = window_height / (SHELF_SPACING+(BORDER_HEIGHT/2))
    shelf_width = window_width-(BORDER_WIDTH*2)

    return round(max_shelves)+1, shelf_width


def draw_bookshelf(window):
    window_size = pygame.display.get_window_size()
    shelf = pygame.Surface(pygame.display.get_window_size())
    max_shelves, shelf_width = compute_sizes()

    y_offset = SHELF_SPACING + floor(BORDER_HEIGHT/2)

    pygame.draw.line(shelf, SHELF, (0, y_offset),
                     (window_size[0], y_offset), BORDER_HEIGHT)

    for index in range(max_shelves):
        ypos = y_offset + (index*SHELF_SPACING)
        pygame.draw.line(shelf, SHELF, (0, ypos),
                         (window_size[0], ypos), BORDER_HEIGHT)

    window.blit(shelf, (0, 0))


def draw_book(metadata, width=-1, height=-1):
    '''
    ## Render an item to the given surface.

    ---

    ### Parameters:
    surface : pygame.Surface - The surface to render the item.
    metadata : dict - The metadata of the item. Must at least include the name of the item.
    width : int - The width of the item. If -1, calculates the width given the name provided, with random padding.
    height : int - The height of the item. If -1, calculates the height given the name provided, with random padding.
    '''

    name = metadata.get('name')
    # author = metadata.get('author', None)
    author = None

    if metadata.get('padx') == None:
        metadata['padx'] = random.randint(1, 5) * 2
    if metadata.get('pady') == None:
        metadata['pady'] = random.randint(1, 10) * 2
    if metadata.get('colour') == None:
        metadata['colour'] = random.choice(Colours().get_all('pastel'))
    padx = metadata.get('padx')
    pady = metadata.get('pady')
    colour = metadata.get('colour')

    if type(colour) == str:
        colour = Colours.get_match(colour, Colours.GREY)

    tname = font.render(str(name), True, TEXT)
    if author != None:
        tauthor = font.render(str(author), True, TEXT)
    else:
        tauthor = pygame.Surface((0, 0))

    if width == -1:
        width = tname.get_height() + tauthor.get_height() + 2 + padx

    if height == -1:
        height = max(tname.get_width(), tauthor.get_width()) + pady

    tname_pos = (pady/2), (padx/2) + 2
    tauthor_pos = (pady/2), (padx/2) + tname.get_height()

    # Height and width are swapped because the item will be rotated 90 degrees
    item_surface = pygame.Surface((height, width))
    pygame.draw.rect(item_surface, metadata.get(
        'colour', (50, 100, 50)), pygame.Rect(0, 0, height, width))
    item_surface.blit(tname, tname_pos)
    item_surface.blit(tauthor, tauthor_pos)

    return pygame.transform.rotate(item_surface, 90)


if __name__ == '__main__':
    window, clock, documents, items = init()

    _, shelf_width = compute_sizes()

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
            elif event.type == pygame.WINDOWRESIZED:
                print(compute_sizes())
                _, shelf_width = compute_sizes()
            elif event.type == pygame.MOUSEWHEEL:
                print(event.x, event.y)

        window.fill(Colours.BACKGROUND)

        draw_bookshelf(window)

        spacing_multiplier = 1
        offset = SHELF_SPACING
        position = 0, offset
        for index, item in enumerate(items):
            item_surface = draw_book(item)
            if position[0] + item_surface.get_width() >= shelf_width:
                spacing_multiplier += 1
                offset = SHELF_SPACING * spacing_multiplier
                position = 0, offset
            position = position[0], position[1] - item_surface.get_height()
            window.blit(draw_book(item), position)
            position = position[0] + item_surface.get_width() + 2, offset

        pygame.display.set_caption(str(int(clock.get_fps())))
        pygame.display.flip()
