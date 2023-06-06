import pygame
from math import floor
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'


def Lerp(start, end, pct):
    pct = min(1, max(0, pct))
    return start + (end-start) * pct


def EaseIn(time):
    return time*time


def EaseOut(time):
    return Flip(EaseIn(Flip(time)))


def Flip(x):
    return 1 - x


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

BORDER_WIDTH = 10
BORDER_HEIGHT = 10
SHELF_SPACING = 50

font = None

BACKGROUND = (50, 50, 50)
TEXT = (200, 200, 200)
SHELF = (100, 100, 100)


def init():
    global font
    pygame.init()
    pygame.font.init()

    flags = pygame.RESIZABLE | pygame.DOUBLEBUF
    window = pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT), flags=flags)
    clock = pygame.time.Clock()
    font = pygame.font.Font('OpenSans-Light.ttf', 20)

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
    start_button.fill(BACKGROUND)
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

    return window, clock


def compute_sizes():
    window_width, window_height = pygame.display.get_window_size()

    max_shelves = window_height / (SHELF_SPACING+(BORDER_HEIGHT/2))
    shelf_width = window_width-(BORDER_WIDTH*2)

    return round(max_shelves)+1, shelf_width


def draw_bookshelf(window):
    window_size = pygame.display.get_window_size()
    shelf = pygame.Surface(pygame.display.get_window_size())
    max_shelves, shelf_width = compute_sizes()

    y_offset = SHELF_SPACING - floor(BORDER_HEIGHT/2)

    pygame.draw.line(shelf, SHELF, (0, y_offset),
                     (window_size[0], y_offset), BORDER_HEIGHT)

    for index in range(max_shelves):
        ypos = y_offset + (index*SHELF_SPACING)
        pygame.draw.line(shelf, SHELF, (0, ypos),
                         (window_size[0], ypos), BORDER_HEIGHT)

    window.blit(shelf, (0, 0))


if __name__ == '__main__':
    window, clock = init()

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
            if event.type == pygame.WINDOWRESIZED:
                print(compute_sizes())

        window.fill(BACKGROUND)

        draw_bookshelf(window)

        pygame.display.set_caption(str(int(clock.get_fps())))
        pygame.display.update()
