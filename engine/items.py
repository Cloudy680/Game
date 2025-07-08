import pygame
from config import TILE_SIZE
from enum import Enum, auto
class EntityPos(Enum):
    LEFT_POS = 1
    RIGHT_POS = 2
    TOP_POS = 3
    BOTTOM_POS = 4


class Sword:
    def __init__ (self, x_pos, y_pos, sword_wid = 20, sword_hei = 7, damage = 15):
        self.item_hitbox = pygame.Rect(x_pos, y_pos, sword_wid, sword_hei)
        self.damage = damage
        self.swordYwid, self.swordYhei = sword_hei, sword_wid
        self.swordXwid, self.swordXhei = sword_wid, sword_hei
        self.attack_firstX, self.attack_firstY = self.item_hitbox.x, self.item_hitbox.y
        self.attack_endX, self.attack_endY = self.item_hitbox.x, self.item_hitbox.y
        self.coul_down = 0
        self.name = "Меч"
        self.is_attack = False
        self.one_attack = False
        self.moving_back = False
        self.moving_speed = 10
        self.part_move = 0

    def draw(self, window):
        pygame.draw.rect(window, pygame.Color('white'), self.item_hitbox)

    def draw_on_map(self, window):
        """Рисует меч лежащим в клетке на карте"""
        # Размеры элементов меча (подогнаны под клетку 64x64)
        handle_width = 10  # Ширина рукояти
        handle_height = 30 # Длина рукояти
        guard_width = 16   # Ширина гарды
        guard_height = 6   # Толщина гарды
        blade_height = 30  # Длина клинка
    
        # Позиция основания меча (центр нижней части клетки)
        base_x = self.item_hitbox.x + self.item_hitbox.width // 2
        base_y = self.item_hitbox.y + self.item_hitbox.height - 10
    
        # Рукоять (вертикальный прямоугольник)
        pygame.draw.rect(
            window,
            (101, 67, 33),  # Коричневый цвет
            (base_x - handle_width//2, base_y - handle_height, handle_width, handle_height)
        )
    
        # Гарда (горизонтальный прямоугольник)
        pygame.draw.rect(
            window,
            (150, 150, 150),  # Серый металл
            (base_x - guard_width//2, base_y - handle_height - guard_height//2, guard_width, guard_height)
        )
    
        # Клинок (треугольник)
        pygame.draw.polygon(
            window,
            (200, 200, 200),  # Серебристый
            [
                (base_x, base_y - handle_height - blade_height),  # Острие
                (base_x - 8, base_y - handle_height),             # Основание слева
                (base_x + 8, base_y - handle_height)              # Основание справа
            ]
        )
    
        # Лезвие (белые линии)
        pygame.draw.line(
            window,
            (255, 255, 255),
            (base_x, base_y - handle_height - blade_height),
            (base_x - 6, base_y - handle_height),
            1
        )
        pygame.draw.line(
            window,
            (255, 255, 255),
            (base_x, base_y - handle_height - blade_height),
            (base_x + 6, base_y - handle_height),
            1
        )

    def set_new_koords_by_player(self, player):
        XMove = False
        Pos = player.get_pos()
        if Pos == EntityPos.RIGHT_POS:
            self.item_hitbox.x, self.item_hitbox.y = player.entity_hitbox.right, player.entity_hitbox.top + player.size / 2 - 4
            XMove = True
        elif Pos == EntityPos.LEFT_POS:
            self.item_hitbox.x, self.item_hitbox.y = player.entity_hitbox.left - player.size, player.entity_hitbox.top + player.size / 2 - 4
            XMove = True
        
        if Pos == EntityPos.BOTTOM_POS:
            self.item_hitbox.x, self.item_hitbox.y = player.entity_hitbox.left + player.size / 2 - 4, player.entity_hitbox.bottom
        elif Pos == EntityPos.TOP_POS:
            self.item_hitbox.x, self.item_hitbox.y = player.entity_hitbox.left + player.size / 2 - 4, player.entity_hitbox.top - player.size

        if XMove:
            self.item_hitbox.width, self.item_hitbox.height = self.swordXwid, self.swordXhei
        else:
            self.item_hitbox.width, self.item_hitbox.height = self.swordYwid, self.swordYhei

    def interact(self, Pos, player):
        if self.coul_down == 0 and not self.is_attack:
            self.set_new_koords_by_player(player)
            self.is_attack = True
            if Pos == EntityPos.RIGHT_POS:
                self.attack_firstX, self.attack_firstY = self.item_hitbox.x, self.item_hitbox.y
                self.attack_endX, self.attack_endY = self.item_hitbox.x + TILE_SIZE / 2, self.item_hitbox.y
            elif Pos == EntityPos.LEFT_POS:
                self.attack_firstX, self.attack_firstY = self.item_hitbox.x, self.item_hitbox.y
                self.attack_endX, self.attack_endY = self.item_hitbox.x - TILE_SIZE / 2, self.item_hitbox.y
            elif Pos == EntityPos.TOP_POS:
                self.attack_firstX, self.attack_firstY = self.item_hitbox.x, self.item_hitbox.y
                self.attack_endX, self.attack_endY = self.item_hitbox.x, self.item_hitbox.y - TILE_SIZE / 2
            elif Pos == EntityPos.BOTTOM_POS:
                self.attack_firstX, self.attack_firstY = self.item_hitbox.x, self.item_hitbox.y
                self.attack_endX, self.attack_endY = self.item_hitbox.x, self.item_hitbox.y + TILE_SIZE / 2
            self.one_attack = True
            

    def update(self, player):
        if self.is_attack and not self.moving_back and self.part_move < self.moving_speed:
            self.part_move += 1
            t = self.part_move / self.moving_speed
            self.item_hitbox.x, self.item_hitbox.y = self.attack_firstX + (self.attack_endX - self.attack_firstX) * t, self.attack_firstY + (self.attack_endY - self.attack_firstY) * t

            if self.part_move >= self.moving_speed:
                self.part_move = 0
                self.coul_down = 3
                self.moving_back = True

        if self.moving_back and self.part_move < self.moving_speed:
            self.part_move += 1
            t = self.part_move / self.moving_speed
            self.item_hitbox.x, self.item_hitbox.y = self.attack_endX + (self.attack_firstX - self.attack_endX) * t, self.attack_endY + (self.attack_firstY - self.attack_endY) * t

            if self.part_move >= self.moving_speed:
                self.part_move = 0
                self.moving_back = False
                self.is_attack = False
                self.coul_down = 3
                player.set_interacting(False)
                self.one_attack = False

        if self.coul_down > 0:
            self.coul_down -= 1
        


