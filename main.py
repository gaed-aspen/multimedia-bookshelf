import pygame

if __name__ == '__main__':
    window = pygame.display.set_mode((800, 600))

    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
        
        window.fill((0, 0, 0))

        pygame.display.set_caption(str(int(clock.get)))
        pygame.display.update()
