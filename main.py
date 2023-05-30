import pygame
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
font = None

BACKGROUND = (50, 50, 50)
TEXT = (200, 200, 200)


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
    start_text = font.render(
        "Please full screen program on the display of choice, then press start", True, (200, 200, 200))

    start_button = font.render("Start", True, (200, 200, 200))

    tx = int((WINDOW_WIDTH / 2)-(start_text.get_width() / 2))
    ty = int((WINDOW_HEIGHT / 2)-(start_text.get_height() / 2))
    bx = int((WINDOW_WIDTH / 2)-(start_button.get_width() / 2))
    by = int((WINDOW_HEIGHT / 2)-(start_button.get_height() / 2))
    text_start = tx, ty
    text_end = tx, ty - 75
    button_start = bx, by
    button_end = bx, by + 50

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

        current_time = max(pygame.time.get_ticks() - start_time, 1)

        pct = min(1 / (animation_duration / current_time), 1)

        text_pos = Lerp(text_start[0], text_end[0], lerp_function(pct)), Lerp(
            text_start[1], text_end[1], lerp_function(pct))
        button_pos = Lerp(button_start[0], button_end[0], pct), Lerp(
            button_start[1], button_end[1], lerp_function(pct))

        opacity = int(Lerp(0, 255, EaseIn(pct)))

        # Update and render
        window.fill((50, 50, 50))

        start_text.set_alpha(opacity)
        start_button.set_alpha(opacity)

        window.blit(start_text, text_pos)
        window.blit(start_button, button_pos)

        pygame.display.update()

    pygame.quit()
    quit()

    return window


def draw_bookshelf(window):
    pass


if __name__ == '__main__':
    window = init()

    running = True
    while running:
        # clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

        window.fill((0, 0, 0))

        # pygame.display.set_caption(str(int(clock.get_fps())))
        pygame.display.update()
