import pygame
bullets = []

class Bullet:
    def __init__(self, x, y, r, direction, speed):
        self.x = x
        self.y = y
        self.r = r
        self.speed = speed
        self.direction = direction
        bullets.append(self)

    def update(self, WIDTH, HEIGHT, game_map, cell_SIZE):
        for i in range(len(game_map)):
            for j in range(len(game_map[0])):
                if game_map[i][j] == 1:
                    rect = pygame.Rect(j * cell_SIZE, i * cell_SIZE, cell_SIZE, cell_SIZE)
                    if rect.collidepoint(self.x, self.y):
                        bullets.remove(self)
                        return
        if self.direction == "LEFT":
            self.x -= self.speed
        elif self.direction == "RIGHT":
            self.x += self.speed
        elif self.direction == "UP":
            self.y -= self.speed
        elif self.direction == "DOWN":
            self.y += self.speed

    def draw(self, window):
        pygame.draw.circle(window, pygame.Color("white"), (int(self.x), int(self.y)), self.r)