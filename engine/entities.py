from code import interact
import pygame
from enum import Enum, auto
import math
from .items import Sword, EntityPos
from random import choice
from config import TILE_SIZE, PLAYER_HIT, enemy_hit

class Condition(Enum):
    Alive = 1
    Dead = 2

class Entity:
    def __init__(self, x, y, size, hp, attack):
        self.x = x
        self.y = y
        self.hp = hp
        self.attack = attack
        self.entity_hitbox = pygame.Rect(self.x, self.y, size, size)
        self.size = size
        self.condition = Condition.Alive
        self.sprite = None  # Pygame 

class Inventory:
    def __init__(self):
        self.inventory = []

    def add_item(self, item):
        self.inventory.append(item)
    
    def draw(self, window):
        inventory_x = 30  # Позиция X
        inventory_y = 680  # Позиция Y
        item_spacing = 40  # Расстояние между предметами
    
        # Фон инвентаря (опционально)
    
        # Текст "Инвентарь"
        font = pygame.font.SysFont(None, 45)
        text = font.render(f"Инвентарь:", True, (255, 255, 255), 1)
        window.blit(text, (inventory_x, inventory_y))
    
        # Отрисовка всех предметов
        for i, item in enumerate(self.inventory):
            item_text = font.render(f"{item.name}", True, pygame.Color('white'))
            window.blit(item_text, (inventory_x + 200 + i * item_spacing, inventory_y))
        
            # Если у предмета есть иконка (например, в отдельном классе)
            if hasattr(item, 'icon'):
                window.blit(item.icon, (inventory_x + 150, inventory_y + 30 + i * item_spacing))

    def get_item(self, ind):
        if 0 <= ind < len(self.inventory):
            return self.inventory[ind]

    def get_items(self):
        return self.inventory

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, size = PLAYER_HIT, hp=100, attack=15)
        self.inventory = Inventory()
        self.activeitem = None
        self.moving = False
        self.start_X = 0
        self.start_Y = 0
        self.where_X = x
        self.where_Y = y
        self.moving_speed = 25
        self.part_move = 0
        self.player_level = 1
        self.interacting = False

        self.animations = self._load_animations()

    def _load_animations(self):
        animations = {
            EntityPos.RIGHT_POS: self._load_animation_frames('right'),
            EntityPos.LEFT_POS: self._load_animation_frames('left'),
            EntityPos.TOP_POS: self._load_animation_frames('up'),
            EntityPos.BOTTOM_POS: self._load_animation_frames('down')
        }
        return animations

    def _load_animation_frames(self, direction):
        try:
            sprite_sheet = pygame.image.load(f'images/player_{direction}.png').convert_alpha()
            frame_height = sprite_sheet.get_height() // 3
            frame_width = sprite_sheet.get_width()
            
            frames = []
            for i in range(3):
                frame = sprite_sheet.subsurface(
                    pygame.Rect(0, i * frame_height, frame_width, frame_height)
                )
                scaled_frame = pygame.transform.scale(frame, (28, 48 ))
                frames.append(scaled_frame)
            return frames
        except Exception as e:
            print(f"Error loading {direction} animation: {e}")
            return None

    def move(self, new_XP, new_YP, world, speed = 25):
        self.moving_speed = speed
        self.where_X, self.where_Y = new_XP, new_YP
        self.start_X, self.start_Y = self.x, self.y

        next_posx, next_posy = int(self.where_X // TILE_SIZE), int(self.where_Y // TILE_SIZE)
        if world[next_posy][next_posx] >= 10 and world[next_posy][next_posx] <= 20:
            have_item = False
            for item in self.inventory.get_items():
                if hasattr(item, 'damage'):
                    self.activeitem = item
                    self.interacting = True
                    have_item = True
            if not have_item:
                self.moving = True
        else:
            self.moving = True

    def update(self):
        if self.interacting:
            self.interact_subject()
            self.activeitem.update(self)
        elif self.moving and self.part_move < self.moving_speed:
            self.part_move += 1
            t = self.part_move / self.moving_speed
            self.set_new_koord(self.start_X + (self.where_X - self.start_X) * t, self.start_Y + (self.where_Y - self.start_Y) * t)

            if self.part_move >= self.moving_speed:
                self.part_move = 0
                self.moving = False

    def set_interacting(self, bol):
         self.interacting = bol

    def draw(self, window):
        if self.moving:
            window.blit(self.animations[self.get_pos()][1], self.entity_hitbox)
        else:
            window.blit(self.animations[self.get_pos()][0], self.entity_hitbox)
        if self.activeitem:
            self.activeitem.draw(window)
        self.inventory.draw(window)

        


    def get_pos(self):
        if self.start_X < self.where_X:
            return EntityPos.RIGHT_POS
        elif self.start_X > self.where_X:
            return EntityPos.LEFT_POS
        elif self.start_Y > self.where_Y:
            return EntityPos.TOP_POS
        return EntityPos.BOTTOM_POS

    def interact_subject(self):
        self.activeitem.interact(self.get_pos(), self)
        

    def set_new_koord(self, X, Y):
        self.x, self.y = X, Y
        self.entity_hitbox.x, self.entity_hitbox.y = X, Y
        if self.activeitem:
            self.activeitem.set_new_koords_by_player(self)



class SmartEnemy(Entity):
    def __init__(self, x, y, max_dis = 5):
        super().__init__(x, y, size=enemy_hit, hp=30, attack=5)
        self.moving_speed = 35
        self.where_X = x
        self.where_Y = y
        self.start_X = x
        self.start_Y = y
        self.part_move = 0
        self.moving = False
        self.move_delay = 0
        self.attacking = False
        self.dying = False
        self.attacking_couldown = 60
        self.max_distance = max_dis
        self.path = []  # Список клеток пути [(col1, row1), (col2, row2), ...]
        self.one_dying = False

        self.predying_sprite = pygame.image.load(f'images/goblin_predied.png').convert_alpha()
        self.predying_sprite = pygame.transform.scale(self.predying_sprite, (self.size * 1.1, self.size * 1.1))
        self.dead_sprite = pygame.image.load(f'images/goblin_died.png').convert_alpha()
        self.dead_sprite = pygame.transform.scale(self.dead_sprite, (self.size * 1.1, self.size * 1.1))

        self.animations = self._load_animations()
        
        self.sounds = {
            'death': pygame.mixer.Sound('sounds/goblin_hit.mp3')
        }

    def _load_animations(self):
        animations = {
            EntityPos.RIGHT_POS: self._load_animation_frames('right'),
            EntityPos.LEFT_POS: self._load_animation_frames('left'),
            EntityPos.TOP_POS: self._load_animation_frames('up'),
            EntityPos.BOTTOM_POS: self._load_animation_frames('down')
        }
        return animations

    def _load_animation_frames(self, direction):
        try:
            stay_sprite = pygame.image.load(f'images/goblin_{direction}.png').convert_alpha()
            stay_sprite = pygame.transform.scale(stay_sprite, (self.size * 1.1, self.size * 1.1))
            walk_sprite = pygame.image.load(f'images/goblin_{direction}_walk.png').convert_alpha()
            walk_sprite = pygame.transform.scale(walk_sprite, (self.size * 1.1, self.size * 1.1))
            
            frames = []
            frames.append(stay_sprite)
            frames.append(walk_sprite)
            return frames
        except Exception as e:
            print(f"Error loading {direction} animation: {e}")
            return None

    def move(self, new_XP, new_YP, speed = 25):
        self.moving_speed = speed
        self.moving = True
        self.where_X, self.where_Y = new_XP, new_YP
        self.start_X, self.start_Y = self.x, self.y

    def update(self, player, world):
        if self.condition != Condition.Dead:
            if self.attacking:
                if self.attacking_couldown == 0:
                    self.moving_speed = 15
                    self.attacking = False
                    self.moving = True
                    self.attacking_couldown = 60
                elif self.attacking_couldown > 0:
                    self.attacking_couldown -= 1
            elif self.dying:
                if not self.one_dying:
                    self.sounds['death'].play()
                    self.one_dying = True
                if self.attacking_couldown <= 0:
                    self.condition = Condition.Dead
                    world[int(self.y // TILE_SIZE)][int(self.x // TILE_SIZE)] = 0
                else:
                    self.attacking_couldown -= 1
                
            elif self.moving and self.move_delay == 0:
                if self.x // TILE_SIZE == self.where_X // TILE_SIZE and self.y // TILE_SIZE == self.where_Y // TILE_SIZE:
                    world[self.where_Y // TILE_SIZE][self.where_X // TILE_SIZE], world[self.start_Y // TILE_SIZE][self.start_X // TILE_SIZE] = 11, 0
                # Продолжаем текущее движение
                self.part_move += 1
                t = self.part_move / self.moving_speed
                self.x, self.entity_hitbox.x = self.start_X + (self.where_X - self.start_X) * t, self.start_X + (self.where_X - self.start_X) * t
                self.y, self.entity_hitbox.y = self.start_Y + (self.where_Y - self.start_Y) * t, self.start_Y + (self.where_Y - self.start_Y) * t

                if self.part_move >= self.moving_speed:
                    self.part_move = 0
                    self.moving = False
                    self.x, self.y = self.where_X, self.where_Y  # Точное позиционирование
                    self.move_delay = 45
                    self.moving_speed = 35# Короткая пауза после движения
            elif self.move_delay > 0:
                self.move_delay -= 1
            else:
                # Пересчитываем путь только когда стоим на месте
                if not self.path or self.is_player_moved(player):
                    self.calculate_path(player, world)

                if len(self.path) == 1:
                    self.attacking = True
        
                if self.path:
                    next_col, next_row = self.path.pop(0)
                    self.where_X = next_col * TILE_SIZE + (TILE_SIZE - self.size) // 2
                    self.where_Y = next_row * TILE_SIZE + (TILE_SIZE - self.size) // 2
                    self.start_X, self.start_Y = self.x, self.y
                    self.moving = True
                    world[next_row][next_col] == 11
                
        else:
            world[self.where_Y // TILE_SIZE][self.where_X // TILE_SIZE] = 0
            
    
    def get_pos(self):
        if self.start_X < self.where_X:
            return EntityPos.RIGHT_POS
        elif self.start_X > self.where_X:
            return EntityPos.LEFT_POS
        elif self.start_Y > self.where_Y:
            return EntityPos.TOP_POS
        return EntityPos.BOTTOM_POS

    def is_player_moved(self, player):
        if not self.path:
            return True
        # Просто проверяем, находится ли игрок в последней клетке пути
        last_col, last_row = self.path[-1]
        player_col = int(player.x // TILE_SIZE)
        player_row = int(player.y // TILE_SIZE)
        return (player_col, player_row) != (last_col, last_row)
    
    def calculate_path(self, player, world):
        start_col = int(self.x // TILE_SIZE)
        start_row = int(self.y // TILE_SIZE)
        player_col = int(player.x // TILE_SIZE)
        player_row = int(player.y // TILE_SIZE)
    
        # Ограничиваем максимальную дистанцию поиска
        if abs(start_col - player_col) + abs(start_row - player_row) > self.max_distance:
            return
        
        self.path = self.a_star_search(start_col, start_row, player_col, player_row, world)
    
    def a_star_search(self, start_col, start_row, goal_col, goal_row, world):
        self.start_X, self.start_Y = self.x, self.y
        """Реализация алгоритма A* для поиска пути."""
        def heuristic(col, row):
            # Манхэттенское расстояние
            return abs(col - goal_col) + abs(row - goal_row)
        
        def is_valid_cell(col, row):
            return (
                0 <= row < len(world) and 
                0 <= col < len(world[0]) and 
                world[row][col] == 0  # 0 — проходимая клетка
            )
        
        # Направления движения (вверх, вниз, влево, вправо)
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        
        open_set = [(start_col, start_row)]
        came_from = {}
        g_score = {(start_col, start_row): 0}
        f_score = {(start_col, start_row): heuristic(start_col, start_row)}
        
        while open_set:
            current = min(open_set, key=lambda pos: f_score.get(pos, float('inf')))
            if current == (goal_col, goal_row):
                # Восстанавливаем путь
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path
            
            open_set.remove(current)
            
            for dx, dy in directions:
                neighbor = (current[0] + dx, current[1] + dy)
                if not is_valid_cell(*neighbor):
                    continue
                
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(*neighbor)
                    if neighbor not in open_set:
                        open_set.append(neighbor)
        
        return []  # Путь не найден
    
    def draw(self, window):
        if self.condition == Condition.Dead:
            window.blit(self.dead_sprite, self.entity_hitbox)
            
        elif self.dying:
            window.blit(self.predying_sprite, self.entity_hitbox)
            pygame.draw.circle(window, pygame.Color('red'), (self.entity_hitbox.x + enemy_hit / 2, self.entity_hitbox.y + enemy_hit / 2), 3)
        
        elif self.moving:
            window.blit(self.animations[self.get_pos()][1], self.entity_hitbox)
        else:
            window.blit(self.animations[self.get_pos()][0], self.entity_hitbox)
        