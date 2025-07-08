import pygame
import os

def show_final_msg():
    WIDTH = 700
    HEIGHT = 600
    FPS = 60

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    font_item_selected = pygame.font.Font(None, 65)

    try:
        menu_image = pygame.image.load("D:\Игра ПУ\images\menu_skeleton.png")
        menu_image_rect = menu_image.get_rect()
        menu_image_rect.center = (WIDTH // 2, 200)
    except:
        print("Не удалось загрузить изображение меню")
        menu_image = None

    items = ["Спасибо за игру", "Продолжение следует"]
    item_rects = []

    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
                return

        window.fill("black")

        if menu_image:
            window.blit(menu_image, menu_image_rect)

        item_rects = []

        for i in range(len(items)):
            text = font_item_selected.render(items[i], 1, "white")
            rect = text.get_rect(center=(WIDTH // 2, 450 + 50 * i))
            item_rects.append(rect)
            window.blit(text, rect)

        pygame.display.update()
        clock.tick(FPS)
    return
