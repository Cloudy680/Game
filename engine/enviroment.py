import pygame
from config import TILE_SIZE

class Wall:
    def __init__(self, x, y, width = TILE_SIZE, height = TILE_SIZE):
        self.rect = pygame.Rect(x, y, width, height)
        self.sprite = pygame.image.load('images/wall_up.png').convert_alpha()
        # Масштабируем под размер клетки
        self.sprite = pygame.transform.scale(self.sprite, (TILE_SIZE, TILE_SIZE))

    def draw(self, window):
        window.blit(self.sprite, self.rect)



    def interact_with_player(self, player, world):
        if player.entity_hitbox.colliderect(self.rect):
                player.move(player.start_X, player.start_Y, world)

class Wood_Wall(Wall):
    def __init__(self, x, y, HP=45):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.HP = HP
        self.max_HP = HP

        self.sounds = {
            'hit': pygame.mixer.Sound('sounds/wood_hit.mp3'),
            'break': pygame.mixer.Sound('sounds/woodbroken.mp3')
        }

        self.sounds['break'].set_volume(0.7)
        
        # Загрузка спрайтшита 39x13 (3 состояния по 13x13)
        try:
            self.sprite_sheet = pygame.image.load('images/wood_wall.png').convert_alpha()
            self.states = [
                pygame.Rect(0, 0, 37 / 3, 12),   # Полностью целая (100%-66% HP)
                pygame.Rect(12, 0, 37 / 3, 12),  # Поврежденная (65%-33% HP)
                pygame.Rect(24, 0, 37 / 3, 12)   # Сильно поврежденная (32%-1% HP)
            ]
            # Масштабируем каждый спрайт до размера тайла
            self.scaled_states = [
                pygame.transform.scale(
                    self.sprite_sheet.subsurface(rect), 
                    (TILE_SIZE, TILE_SIZE))
                for rect in self.states
            ]
        except:
            print("Не удалось загрузить спрайты стены, используется fallback-отрисовка")
            self.scaled_states = None

    def get_state_index(self):
        """Определяет текущее состояние стены"""
        health_percent = self.HP / self.max_HP
        if health_percent >= 0.7: return 0
        if health_percent >= 0.4: return 1
        if self.HP >= 0: return 2
        return None  # Разрушенная

    def is_broken(self):
        return self.HP <= 0

    def draw(self, window):
        if self.is_broken():
            # Рисуем контур разрушенной стены
            pygame.draw.rect(window, pygame.Color('brown'), self.rect, 1)
        elif self.scaled_states:
            # Рисуем текущее состояние спрайта
            state_idx = self.get_state_index()
            if state_idx is not None:
                window.blit(self.scaled_states[state_idx], self.rect)
        else:
            # Fallback: рисуем цветной прямоугольник
            pygame.draw.rect(window, pygame.Color('brown'), self.rect)

    def take_damage(self, damage, world):
        """Обработка получения урона с воспроизведением звуков"""
        if self.HP <= 0:
            return
            
        self.HP -= damage
        
        # Звук удара
        
        # Если стена разрушена
        if self.HP <= 0:
            self.sounds['break'].play()
            world[int(self.rect.y // TILE_SIZE)][int(self.rect.x // TILE_SIZE)] = 0
        else:
            self.sounds['hit'].play()

    def interact_with_player(self, player, world):
        if not self.is_broken():
            # Проверяем атаку игрока
            if (player.activeitem 
                and hasattr(player.activeitem, 'is_attack') 
                and player.activeitem.is_attack
                and player.activeitem.item_hitbox.colliderect(self.rect)
                and not player.activeitem.one_attack):
                
                self.take_damage(player.activeitem.damage, world)
                player.activeitem.one_attack = True

            elif player.entity_hitbox.colliderect(self.rect):
                # Блокируем движение
                player.move(player.start_X, player.start_Y, world)


