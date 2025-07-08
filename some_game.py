import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, Player_Save
from random import randint
from engine.entities import Player, PLAYER_HIT, SmartEnemy, Condition
from engine.enviroment import Wall, Wood_Wall, TILE_SIZE
from states.gameplay import initialization, game_loop
import pickle
import os
def run_game_e():

    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    player = Player((TILE_SIZE - PLAYER_HIT) // 2, (TILE_SIZE - PLAYER_HIT) // 2)
    world = []
    wall_list = []
    enemy = []
    item_list = []
    state = 'initialization'
    timer = 0
    EXIT_X, EXIT_Y = 0, 0
    initial_timer = 0



    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False

        if state == 'initialization':
            world, wall_list, item_list, enemy, player, state = initialization()

        elif state == 'playing':

            timer, initial_timer, state = game_loop(
                window, player, world, wall_list, item_list, enemy,
                EXIT_X, EXIT_Y, timer, initial_timer, state
            )



        pygame.display.update()
        clock.tick(FPS)

    return