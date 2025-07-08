import pygame
from config import TILE_SIZE

class Wall:
    def __init__(self, x, y, width = TILE_SIZE, height = TILE_SIZE):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, window):
        pygame.draw.rect(window, pygame.Color('gray'), self.rect)

    def interact_with_player(self, player, world):
        if player.entity_hitbox.colliderect(self.rect):
            # Возвращаем игрока на предыдущую позицию
            player.move(player.start_X, player.start_Y, world)

class Wood_Wall:
    def __init__(self, x, y, HP = 45, width = TILE_SIZE, height = TILE_SIZE):
        self.rect = pygame.Rect(x, y, width, height)
        self.HP = HP

    

    def is_broken(self):
        if self.HP <= 0:
            return True
        return False

    def draw(self, window):
        if self.HP > 0:
            pygame.draw.rect(window, pygame.Color('brown'), self.rect)
        else:
            pygame.draw.rect(window, pygame.Color('brown'), self.rect, 1)

    def interact_with_player(self, player, world):
        print("efgb")
        haveitem = False
        if self.HP > 0:
            for item in player.inventory.get_items():
                if hasattr(item, 'damage'):
                    player.activeitem = item
                    haveitem = True
            if haveitem:
                if player.activeitem.item_hitbox.colliderect(self.rect) and player.activeitem.is_attack:
                    print("ferfg")
                    self.HP = 0
            else:
                player.move(player.start_X, player.start_Y, world)


