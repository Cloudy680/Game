import pygame
import os

def show_loading_screen():
    WIDTH = 840
    HEIGHT = 720
    FPS = 60

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    timer = 120
    load_timer = 30
    selected = 0

    font_l = pygame.font.Font(None, 30)

    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
                return

        window.fill("black")

        if timer != 0:
            text = font_l.render("Loading", 1, "white")
            rect = text.get_rect(center=(WIDTH - 80, HEIGHT - 30))
            window.blit(text, rect)
        else:
            return

        timer -= 1
        load_timer -= 1
        pygame.display.update()
        clock.tick(FPS)
    return