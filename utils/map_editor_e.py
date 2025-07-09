import pygame
import tkinter as tk
from tkinter import filedialog
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from engine.enviroment import TILE_SIZE
from engine.entities import PLAYER_HIT

pygame.init()

# Настройки окна
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Редактор матрицы мира")
clock = pygame.time.Clock()

# Инициализация мира
world = []
worldWid, worldHei = SCREEN_WIDTH // TILE_SIZE, SCREEN_HEIGHT // TILE_SIZE

for row in range(worldHei):
    line = []
    for col in range(worldWid):
        line.append(0)
    world.append(line)

# Функции для работы с файлами
def save_world():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        title="Сохранить мир",
        defaultextension=".world",
        filetypes=[("World files", "*.world"), ("Все файлы", "*.*")]
    )
    if file_path:
        with open(file_path, 'w') as f:
            for row in world:
                f.write(' '.join(map(str, row)) + '\n')
        print(f"Мир сохранён в {file_path}")

def load_world():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Загрузить мир",
        filetypes=[("World files", "*.world"), ("Все файлы", "*.*")]
    )
    if file_path:
        with open(file_path, 'r') as f:
            loaded_world = []
            for line in f:
                row = list(map(int, line.strip().split()))
                loaded_world.append(row)
            
            # Проверка на совместимость размеров
            if len(loaded_world) == worldHei and len(loaded_world[0]) == worldWid:
                for i in range(worldHei):
                    for j in range(worldWid):
                        world[i][j] = loaded_world[i][j]
                print(f"Мир загружен из {file_path}")
            else:
                print("Ошибка: несовместимые размеры мира")

# Шрифт для интерфейса
font = pygame.font.SysFont('Arial', 20)

# Кнопки
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False
    
    def draw(self, surface):
        color = (100, 100, 255) if self.is_hovered else (70, 70, 200)
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=5)
        
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
    
    def handle_event(self, event, pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pos) and self.action:
                self.action()

# Создание кнопок
save_button = Button(10, 10, 40, 40, "Save", save_world)
load_button = Button(60, 10, 40, 40, "Open", load_world)

# Основной цикл
play = True
while play:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        
        # Обработка кнопок
        save_button.handle_event(event, mouse_pos)
        load_button.handle_event(event, mouse_pos)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            mousePX, mousePY = pygame.mouse.get_pos()
            mouseRow, mouseCol = mousePY // TILE_SIZE, mousePX // TILE_SIZE
            if 0 <= mouseRow < worldHei and 0 <= mouseCol < worldWid:
                world[mouseRow][mouseCol] = 2
        elif keys[pygame.K_p]:
            mousePX, mousePY = pygame.mouse.get_pos()
            mouseRow, mouseCol = mousePY // TILE_SIZE, mousePX // TILE_SIZE
            if 0 <= mouseRow < worldHei and 0 <= mouseCol < worldWid:
                world[mouseRow][mouseCol] = 3
        elif keys[pygame.K_q]:
            mousePX, mousePY = pygame.mouse.get_pos()
            mouseRow, mouseCol = mousePY // TILE_SIZE, mousePX // TILE_SIZE
            if 0 <= mouseRow < worldHei and 0 <= mouseCol < worldWid:
                world[mouseRow][mouseCol] = 10
        elif keys[pygame.K_e]:
            mousePX, mousePY = pygame.mouse.get_pos()
            mouseRow, mouseCol = mousePY // TILE_SIZE, mousePX // TILE_SIZE
            if 0 <= mouseRow < worldHei and 0 <= mouseCol < worldWid:
                world[mouseRow][mouseCol] = 11
        elif keys[pygame.K_s]:
            mousePX, mousePY = pygame.mouse.get_pos()
            mouseRow, mouseCol = mousePY // TILE_SIZE, mousePX // TILE_SIZE
            if 0 <= mouseRow < worldHei and 0 <= mouseCol < worldWid:
                world[mouseRow][mouseCol] = 21
        
        # Редактирование мира
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:  # ЛКМ или ПКМ
                mousePX, mousePY = pygame.mouse.get_pos()
                mouseRow, mouseCol = mousePY // TILE_SIZE, mousePX // TILE_SIZE
                
                if 0 <= mouseRow < worldHei and 0 <= mouseCol < worldWid:
                    if pygame.mouse.get_pressed()[0]:  # ЛКМ - ставим блок
                        world[mouseRow][mouseCol] = 1
                    elif pygame.mouse.get_pressed()[2]:  # ПКМ - убираем блок
                        world[mouseRow][mouseCol] = 0
                    elif keys[pygame.K_SPACE]:
                        world[mouseRow][mouseCol] = 2

    # Проверка наведения на кнопки
    save_button.check_hover(mouse_pos)
    load_button.check_hover(mouse_pos)

    # Отрисовка
    window.fill(pygame.Color('black'))
    
    # Отрисовка мира
    for row in range(worldHei):
        for col in range(worldWid):
            x, y = col * TILE_SIZE, row * TILE_SIZE
            
            if world[row][col] == 1:
                pygame.draw.rect(window, pygame.Color('gray'), (x, y, TILE_SIZE, TILE_SIZE))
            elif world[row][col] == 0:
                pygame.draw.rect(window, pygame.Color('darkgray'), (x, y, TILE_SIZE, TILE_SIZE), 1)
            elif world[row][col] == 2:
                pygame.draw.rect(window, pygame.Color('green'), (x, y, TILE_SIZE, TILE_SIZE))
            elif world[row][col] == 3:
                pygame.draw.rect(window, pygame.Color('purple'), (x, y, TILE_SIZE, TILE_SIZE))
            elif world[row][col] == 10:
                pygame.draw.rect(window, pygame.Color('brown'), (x, y, TILE_SIZE, TILE_SIZE))
            elif world[row][col] == 11:
                pygame.draw.rect(window, pygame.Color('green'), (col * TILE_SIZE + (TILE_SIZE - PLAYER_HIT) // 2, row * TILE_SIZE + ((TILE_SIZE - PLAYER_HIT) // 2), PLAYER_HIT, PLAYER_HIT))
            elif world[row][col] == 21:
                x, y = col * TILE_SIZE + (TILE_SIZE - PLAYER_HIT) // 2 + PLAYER_HIT / 2, row * TILE_SIZE + (TILE_SIZE - PLAYER_HIT) // 2 + PLAYER_HIT / 2
                CELL_SIZE = 64

                # Создаем поверхность для ножа (прозрачную)
                knife_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)

                # Цвета
                HANDLE_COLOR = (101, 67, 33)  # Коричневый для рукояти
                BLADE_COLOR = (200, 200, 200)  # Серебристый для клинка
                EDGE_COLOR = (255, 255, 255)   # Белый для лезвия

                # Рисуем нож на поверхности:

                # Рукоять (8x16 пикселей)
                pygame.draw.rect(knife_surface, HANDLE_COLOR, (32, 24, 8, 16))

                # Гарда (перекрестие)
                pygame.draw.rect(knife_surface, BLADE_COLOR, (28, 32, 4, 4))
                pygame.draw.rect(knife_surface, BLADE_COLOR, (40, 32, 4, 4))

                # Клинок (треугольник)
                pygame.draw.polygon(knife_surface, BLADE_COLOR, [
                    (32, 24),  # Начало у рукояти
                    (32, 8),   # Верхняя точка
                    (48, 24)   # Конец клинка
                ])

                # Лезвие (белая линия)
                pygame.draw.line(knife_surface, EDGE_COLOR, (32, 24), (48, 24), 1)
                pygame.draw.line(knife_surface, EDGE_COLOR, (32, 24), (32, 8), 1)

                window.blit(knife_surface, (x - 32, y - 32))
    
    # Отрисовка кнопок
    save_button.draw(window)
    load_button.draw(window)
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()