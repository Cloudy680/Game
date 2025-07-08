import pygame
import os

def show_menu():
    WIDTH = 400
    HEIGHT = 600
    FPS = 60

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    font_item = pygame.font.Font(None, 50)
    font_item_selected = pygame.font.Font(None, 65)

    try:
        menu_image = pygame.image.load("D:\Игра ПУ\images\menu_skeleton.png")
        menu_image_rect = menu_image.get_rect()
        menu_image_rect.center = (WIDTH // 2, 200)
    except:
        print("Не удалось загрузить изображение меню")
        menu_image = None

    items = ["Играть", "Настройки", "Выход"]
    select = -1
    item_rects = []

    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False

            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                for i, rect in enumerate(item_rects):
                    if rect.collidepoint(mouse_pos):
                        select = i

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for i, rect in enumerate(item_rects):
                    if rect.collidepoint(mouse_pos):
                        return items[i]

        window.fill("black")

        if menu_image:
            window.blit(menu_image, menu_image_rect)

        item_rects = []

        for i in range(len(items)):
            if i == select:
                text = font_item_selected.render(items[i], 1, "white")
            else:
                text = font_item.render(items[i], 1, "gray")

            rect = text.get_rect(center=(WIDTH // 2, 400 + 50 * i))
            item_rects.append(rect)
            window.blit(text, rect)

        pygame.display.update()
        clock.tick(FPS)
    return
