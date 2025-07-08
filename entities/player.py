import pygame

# Класс игрока

class Player_M:
    def __init__(self, START_X, START_Y, cell_SIZE, width, height):
        self.hitbox = pygame.Rect(START_X, START_Y, width, height)
        self.collision = False
        self.inv = ""
        self.moving = False

    # Движение персонажа по оси OX
    def X_move(self, timer : int, cell_SIZE, game_map, X_def, speed) -> int:
        timer -= 1
        if timer < 0:
            for i in range(len(game_map)):
                for j in range(len(game_map[0])):
                    if (game_map[i][j] == 1 or game_map[i][j] == 3 or game_map[i][j] == 4 or game_map[i][j] == 7 or game_map[i][j] == 10 or game_map[i][j] == 12 or game_map[i][j] == 14) and self.hitbox.colliderect(
                            pygame.Rect(j * cell_SIZE, i * cell_SIZE, cell_SIZE, cell_SIZE)):
                        self.collision = True
            if self.collision:
                self.hitbox.x -= speed
                if self.hitbox.x == X_def:
                    timer = -cell_SIZE // abs(speed)
                    self.collision = False
            else:
                self.hitbox.x += speed
        if timer == -cell_SIZE // abs(speed):
            timer = 0
        return timer

    # Движение персонажа по оси OY
    def Y_move(self, timer: int, cell_SIZE, game_map, Y_def, speed) -> int:
        timer -= 1
        if timer < 0:
            collision = False
            for i in range(len(game_map)):
                for j in range(len(game_map[0])):
                    if (game_map[i][j] == 1 or game_map[i][j] == 3 or game_map[i][j] == 4 or game_map[i][j] == 7 or game_map[i][j] == 10 or game_map[i][j] == 12 or game_map[i][j] == 14) and self.hitbox.colliderect(
                            pygame.Rect(j * cell_SIZE, i * cell_SIZE, cell_SIZE, cell_SIZE)):
                        self.collision = True
            if self.collision:
                self.hitbox.y -= speed
                if self.hitbox.y == Y_def:
                    timer = -cell_SIZE // abs(speed)
                    self.collision = False
            else:
                self.hitbox.y += speed
        if timer == -cell_SIZE // abs(speed):
            timer = 0
        return timer

    def Set_inv(self, inv):
        self.inv = inv
    def Get_inv(self):
        return self.inv
    def Is_moving(self):
        return self.moving
    def Change_moving(self, moving):
        self.moving = moving
