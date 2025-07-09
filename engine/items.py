import pygame
import os
from config import TILE_SIZE
from enum import Enum, auto
class EntityPos(Enum):
    LEFT_POS = 1
    RIGHT_POS = 2
    TOP_POS = 3
    BOTTOM_POS = 4


class Sword:
    def __init__(self, x_pos, y_pos, sword_wid=20, sword_hei=7, damage=15):
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
        
        # Загрузка спрайта меча
        self.load_sword_sprite()
        self.current_sprite = self.sword_sprite
        self.current_angle = 0 
        self.flip_x = False
        self.flip_y = False
        self.sprite_offset_x = 0  # Смещение по X
        self.sprite_offset_y = 0  # Смещение по Y
        
        # Для разных направлений можно задать разные смещения
        self.offsets = {
            EntityPos.RIGHT_POS: (-26, -6),
            EntityPos.LEFT_POS: (-10, -6),  # Сильнее смещаем влево
            EntityPos.TOP_POS: (9, 15),
            EntityPos.BOTTOM_POS: (-2, -10)
        }
        
    def load_sword_sprite(self):
        """Загружает спрайт меча (замените путь на ваш)"""
        try:
            sprite_path = "images/scithersword.png"
            self.sword_sprite = pygame.image.load(sprite_path).convert_alpha()
            # Масштабируем спрайт к нужному размеру
            self.sword_sprite = pygame.transform.scale(self.sword_sprite, (self.swordXwid * 3, self.swordXhei * 3))
        except:
            # Создаем простой спрайт если загрузка не удалась
            self.sword_sprite = pygame.Surface((self.swordXwid, self.swordXhei), pygame.SRCALPHA)
            pygame.draw.rect(self.sword_sprite, (200, 200, 200), (0, 0, self.swordXwid, self.swordXhei))
    
    def draw(self, window):
        """Отрисовывает меч с учетом смещения"""
        # Применяем трансформации
        flipped_sprite = pygame.transform.flip(self.sword_sprite, self.flip_x, self.flip_y)
        rotated_sprite = pygame.transform.rotate(flipped_sprite, self.current_angle)
        
        # Рассчитываем позицию с учетом смещения
        draw_x = self.item_hitbox.x + self.sprite_offset_x
        draw_y = self.item_hitbox.y + self.sprite_offset_y
        
        # Для повернутых спрайтов может потребоваться дополнительная корректировка
        if self.current_angle in (90, 270):
            draw_x -= rotated_sprite.get_width() // 2 - self.item_hitbox.width // 2
            draw_y -= rotated_sprite.get_height() // 2 - self.item_hitbox.height // 2
        
        window.blit(rotated_sprite, (draw_x, draw_y))
    def set_new_koords_by_player(self, player):
        """Устанавливает позицию меча относительно игрока и угол поворота"""
        Pos = player.get_pos()

        self.sprite_offset_x, self.sprite_offset_y = self.offsets[Pos]
        if Pos == EntityPos.RIGHT_POS:
            self.item_hitbox.x = player.entity_hitbox.right
            self.item_hitbox.y = player.entity_hitbox.top + player.size / 2 - 4
            self.item_hitbox.width, self.item_hitbox.height = self.swordXwid, self.swordXhei
            self.current_angle = 0  # Горизонтально вправо
            self.flip_x = False
            self.flip_y = False
        elif Pos == EntityPos.LEFT_POS:
            self.item_hitbox.x = player.entity_hitbox.left - self.swordXwid
            self.item_hitbox.y = player.entity_hitbox.top + player.size / 2 - 4
            self.item_hitbox.width, self.item_hitbox.height = self.swordXwid, self.swordXhei
            self.current_angle = 180  # Горизонтально влево
            self.flip_x = False
            self.flip_y = True
        elif Pos == EntityPos.BOTTOM_POS:
            self.item_hitbox.x = player.entity_hitbox.left + player.size / 2 - 4
            self.item_hitbox.y = player.entity_hitbox.bottom
            self.item_hitbox.width, self.item_hitbox.height = self.swordYwid, self.swordYhei
            self.current_angle = 90  # Вертикально вниз
            self.flip_x = True
            self.flip_y = True
        elif Pos == EntityPos.TOP_POS:
            self.item_hitbox.x = player.entity_hitbox.left + player.size / 2 - 4
            self.item_hitbox.y = player.entity_hitbox.top - self.swordYhei
            self.item_hitbox.width, self.item_hitbox.height = self.swordYwid, self.swordYhei
            self.current_angle = 270
            self.flip_x = True
            self.flip_y = True  # Вертикально вверх

    def interact(self, Pos, player):
        """Начинает атаку мечом"""
        if self.coul_down == 0 and not self.is_attack:
            self.set_new_koords_by_player(player)
            self.is_attack = True
            
            # Определяем конечную точку атаки в зависимости от направления
            attack_distance = TILE_SIZE / 2
            if Pos == EntityPos.RIGHT_POS:
                self.attack_firstX, self.attack_firstY = self.item_hitbox.x, self.item_hitbox.y
                self.attack_endX = self.item_hitbox.x + attack_distance
                self.attack_endY = self.item_hitbox.y
            elif Pos == EntityPos.LEFT_POS:
                self.attack_firstX, self.attack_firstY = self.item_hitbox.x, self.item_hitbox.y
                self.attack_endX = self.item_hitbox.x - attack_distance
                self.attack_endY = self.item_hitbox.y
            elif Pos == EntityPos.TOP_POS:
                self.attack_firstX, self.attack_firstY = self.item_hitbox.x, self.item_hitbox.y
                self.attack_endX = self.item_hitbox.x
                self.attack_endY = self.item_hitbox.y - attack_distance
            elif Pos == EntityPos.BOTTOM_POS:
                self.attack_firstX, self.attack_firstY = self.item_hitbox.x, self.item_hitbox.y
                self.attack_endX = self.item_hitbox.x
                self.attack_endY = self.item_hitbox.y + attack_distance

    def update(self, player):
        """Обновляет состояние атаки меча"""
        if self.is_attack and not self.moving_back and self.part_move < self.moving_speed:
            self.part_move += 1
            t = self.part_move / self.moving_speed
            self.item_hitbox.x = self.attack_firstX + (self.attack_endX - self.attack_firstX) * t
            self.item_hitbox.y = self.attack_firstY + (self.attack_endY - self.attack_firstY) * t

            if self.part_move >= self.moving_speed:
                self.part_move = 0
                self.coul_down = 7
                self.moving_back = True

        if self.moving_back and self.part_move < self.moving_speed:
            self.part_move += 1
            t = self.part_move / self.moving_speed
            self.item_hitbox.x = self.attack_endX + (self.attack_firstX - self.attack_endX) * t
            self.item_hitbox.y = self.attack_endY + (self.attack_firstY - self.attack_endY) * t

            if self.part_move >= self.moving_speed:
                self.part_move = 0
                self.moving_back = False
                self.is_attack = False
                self.coul_down = 7
                player.set_interacting(False)
                self.one_attack = False

        if self.coul_down > 0:
            self.coul_down -= 1
        


