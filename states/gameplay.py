import sys
from pathlib import Path

# Добавляем корень проекта в путь
sys.path.append(str(Path(__file__).parent.parent))

from config import Player_Save, TILE_SIZE
from engine.enviroment import Wall, Wood_Wall
from engine.entities import Player, SmartEnemy, Condition
from engine.items import Sword
import os
import pickle
import pygame
PLAYER_HIT = 20

def load_worlde(file_path):
    if file_path:
        with open(file_path, 'r') as f:
            loaded_world = []
            for line in f:
                row = list(map(int, line.strip().split()))
                loaded_world.append(row)
            
            # Проверка на совместимость размеров

            print(f"Мир загружен из {file_path}")
    return loaded_world

def initialization():
    wall_list = []
    item_list = []
    have_player = False
    if os.path.exists(Player_Save):
        player_file = open(Player_Save, 'rb')
        player = pickle.load(player_file)
        player_file.close()
        have_player = True
    if have_player:
        world_path = f'assets\world_{player.player_level}.world'
    else:
        world_path = f'assets\world_1.world'
    if not os.path.exists(world_path):
        player.player_level -= 1
        world_path = f'assets\world_{player.player_level}.world'
        if not os.path.exists(world_path):
            world_path = f'assets\world_1.world'
    world = load_worlde(world_path)
    spawn_x, spawn_y = 0, 0
    enemy = []
    for row in range(len(world)):
        for col in range(len(world[0])):
            if world[row][col] == 1:
                wall_list.append(Wall(col * TILE_SIZE, row * TILE_SIZE))
            elif world[row][col] == 10:
                wall_list.append(Wood_Wall(col * TILE_SIZE, row * TILE_SIZE))
            elif world[row][col] == 2:
                spawn_x, spawn_y = col * TILE_SIZE + (TILE_SIZE - PLAYER_HIT) // 2, row * TILE_SIZE + (TILE_SIZE - PLAYER_HIT) // 2
            elif world[row][col] == 3:
                EXIT_X, EXIT_Y = col * TILE_SIZE + (TILE_SIZE - PLAYER_HIT) // 2, row * TILE_SIZE + (TILE_SIZE - PLAYER_HIT) // 2
            elif world[row][col] == 11:
                enemy.append(SmartEnemy(col * TILE_SIZE + (TILE_SIZE - PLAYER_HIT) // 2, row * TILE_SIZE + (TILE_SIZE - PLAYER_HIT) // 2))
            elif world[row][col] == 21:
                item_list.append(Sword(col * TILE_SIZE + (TILE_SIZE - PLAYER_HIT) // 2, row * TILE_SIZE + (TILE_SIZE - PLAYER_HIT) // 2))
    if not have_player:
        print("dff")
        player = Player(spawn_x, spawn_y)
        
    print(player.inventory.get_items())
    state = 'playing'

    return world, wall_list, item_list, enemy, player, state, EXIT_X, EXIT_Y






def draw_world(world, window):
    for row in range(len(world)):
        for col in range(len(world[0])):
            x, y = col * TILE_SIZE, row * TILE_SIZE

            if world[row][col] == 2:
                pygame.draw.rect(window, pygame.Color('green'), (x, y, TILE_SIZE, TILE_SIZE))
            elif world[row][col] == 3:
                pygame.draw.rect(window, pygame.Color('purple'), (x, y, TILE_SIZE, TILE_SIZE))

def render_scene(window, world, walls, item_list, enemies, player):
    window.fill(pygame.Color('black'))
    draw_world(world, window)
    for wall in walls:
        wall.draw(window)
    for enemy in enemies:
        enemy.draw(window)
    for item in item_list:
        item.draw(window)
    player.draw(window)
    FONT = pygame.font.SysFont(None, 45)
    level = FONT.render(f"Уровень: " + str(player.player_level + 2), True, (255, 255, 255), 1)
    window.blit(level, (30, 20))

def move_right(who, world):
    who.move(who.x + TILE_SIZE, who.y, world)

def move_left(who, world):
    who.move(who.x - TILE_SIZE, who.y, world)

def move_up(who, world):
    who.move(who.x, who.y - TILE_SIZE, world)

def move_down(who, world):
    who.move(who.x, who.y + TILE_SIZE, world)

def handle_wall_collisions(player, wall_list, world):
    for wall in wall_list:
            wall.interact_with_player(player, world)


def handle_enemy_collisions(player, enemies, world):
    for enemy in enemies:
        if player.entity_hitbox.colliderect(enemy.entity_hitbox):
            if not enemy.dying and enemy.condition == Condition.Alive:
                player.condition = Condition.Dead
                return True  # Игра окончена
        if player.activeitem:
            if (player.activeitem.is_attack 
                    and player.activeitem.item_hitbox.colliderect(enemy.entity_hitbox)):
                enemy.dying = True
    return False

def handle_item_collisions(player, item_list, world):
    for item in item_list:
        if player.entity_hitbox.colliderect(item.item_hitbox):
            player.inventory.add_item(item)
            item_list.remove(item)
            player.activeitem = item
            break


def game_loop(window, player, world, wall_list, item_list, enemy, EXIT_X, EXIT_Y, timer, initial_timer, state):
    keys = pygame.key.get_pressed()

    # Обработка ввода
    if timer > 0:
        timer -= 1

    

    # Обновление состояний
    player.update()
    for enem in enemy:
        enem.update(player, world)

    

    # Отрисовка
    render_scene(window, world, wall_list, item_list, enemy, player)
    
    
    handle_wall_collisions(player, wall_list, world)
    if handle_enemy_collisions(player, enemy, world):
        player.condition = Condition.Dead
    handle_item_collisions(player, item_list, world)
    
    if keys[pygame.K_RIGHT] and timer == 0:
        move_right(player, world)
        timer = 30
    elif keys[pygame.K_LEFT] and timer == 0:
        move_left(player, world)
        timer = 30
    elif keys[pygame.K_UP] and timer == 0:
        move_up(player, world)
        timer = 30
    elif keys[pygame.K_DOWN] and timer == 0:
        move_down(player, world)
        timer = 30


    # Проверка условий завершения уровня
    if EXIT_X == player.x and EXIT_Y == player.y:
        state = 'stop'
        initial_timer = 5
        wall_list.clear()
    elif player.condition == Condition.Dead:
        state = 'initialization'
        initial_timer = 10

    # Обработка начального таймера
    if initial_timer > 0:
        window.fill(pygame.Color('black'))
        initial_timer -= 1

    return timer, initial_timer, state

