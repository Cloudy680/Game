import pygame
import copy
from entities.player import Player_M
from entities.bullet import Bullet, bullets
from utils.help_functions import find_plate_pos, check_direction, load_game_map, get_start_coordinats

def run_game(level_number):
    WIDTH = 840
    HEIGHT = 720
    FPS = 60
    FONT = pygame.font.SysFont(None, 45)
    cell_SIZE = 60

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    try:
        img_key = pygame.image.load("D:\Игра ПУ\images\key.png")
        img_key_door = pygame.image.load("D:\Игра ПУ\images\key_door.png")
        img_floor = pygame.image.load("D:\Игра ПУ\images\_another_floor.png")
        img_plate_act = pygame.image.load("D:\Игра ПУ\images\_another_floor1.png")
        img_player = pygame.image.load("D:\Игра ПУ\images\player.gif")
        img_wall_up = pygame.image.load("D:\Игра ПУ\images\wall_up.png")
    except:
        print("Не удалось загрузить изображение")

    img_key = pygame.transform.scale(img_key, (cell_SIZE // 2, cell_SIZE // 2))
    img_player = pygame.transform.scale(img_player, (cell_SIZE // 2, cell_SIZE // 2))
    img_key_door = pygame.transform.scale(img_key_door, (cell_SIZE, cell_SIZE))
    img_wall_up = pygame.transform.scale(img_wall_up, (cell_SIZE, cell_SIZE))
    img_floor = pygame.transform.scale(img_floor, (cell_SIZE, cell_SIZE))
    img_plate_act = pygame.transform.scale(img_plate_act, (cell_SIZE, cell_SIZE))

    #Вычислние размеров карты относительно окна приложения

    game_map = []
    game_map_WIDTH = WIDTH // cell_SIZE
    game_map_HEIGHT = HEIGHT // cell_SIZE

    for i in range(game_map_HEIGHT):
        line = []
        for j in range(game_map_WIDTH):
            line.append(0)
        game_map.append(line)
        

    # Загрузка карты
    map_restart = []
    game_map, game_map_restart = load_game_map(game_map, level_number, game_map_WIDTH)


    # Получние координат старта
    START_X, START_Y = 0, 0
    START_X, START_Y = get_start_coordinats(game_map, cell_SIZE)

    # Создание игрока
    PLAYER_SPEED = 2
    player = Player_M(START_X, START_Y, cell_SIZE, 30, 30)


    # Флаги и таймеры
    timer = 0
    DELAY = 0

    key_left_pressed = False
    key_right_pressed = False
    key_up_pressed = False
    key_down_pressed = False

    door_plate = False
    use = False
    trap_1 = False
    trap_2 = False
    trap_3 = False

    BULLET_SPEED = PLAYER_SPEED
    BULLET_CD = 120
    trap_1_timer = 0
    trap_2_timer = 0
    trap_3_timer = 0

    state = "start"

    # Промежуточное меню
    for i in range(100):
        print()
    print("Добро пожаловать в игру")
    print("Ваша цель - дойти до выхода(фиолетовая платформа)")
    print("Нажмите ПРОБЕЛ или WASD чтобы начать")

    # Основной игровой цикл
    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
                play = False
                return 0

            # Реализация движения персонажа
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a and player.Is_moving() == False:
                timer = 0
                X_def = player.hitbox.x
                key_left_pressed = True
                timer = DELAY
                player.Change_moving(True)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d and player.Is_moving() == False:
                timer = 0
                X_def = player.hitbox.x
                key_right_pressed = True
                timer = DELAY
                player.Change_moving(True)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w and player.Is_moving() == False:
                timer = 0
                Y_def = player.hitbox.y
                key_up_pressed = True
                timer = DELAY
                player.Change_moving(True)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s and player.Is_moving() == False:
                timer = 0
                Y_def = player.hitbox.y
                key_down_pressed = True
                timer = DELAY
                player.Change_moving(True)

        window.fill(pygame.Color("black"))

        # Проверка состояний игры
        keys = pygame.key.get_pressed()
        click = keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_SPACE]
        if state == "start":
            state = "play"

        elif state == "dead":
            player.Change_moving(False)
            state = "play"

        elif state == "win":
            return 1

        elif state == "play":
            if key_left_pressed:
                timer = player.X_move(timer, cell_SIZE, game_map, X_def, -PLAYER_SPEED)
                if timer == 0:
                    key_left_pressed = False
                    player.Change_moving(False)
            if key_right_pressed:
                timer = player.X_move(timer, cell_SIZE, game_map, X_def, PLAYER_SPEED)
                if timer == 0:
                    key_right_pressed = False
                    player.Change_moving(False)
            if key_up_pressed:
                timer = player.Y_move(timer, cell_SIZE, game_map, Y_def, -PLAYER_SPEED)
                if timer == 0:
                    key_up_pressed = False
                    player.Change_moving(False)
            if key_down_pressed:
                timer = player.Y_move(timer, cell_SIZE, game_map, Y_def, PLAYER_SPEED)
                if timer == 0:
                    key_down_pressed = False
                    player.Change_moving(False)

        # Отрисовка карты и работоспособность особых ячеек
        for i in range(game_map_HEIGHT):
            for j in range(game_map_WIDTH):
                x, y = j * cell_SIZE, i * cell_SIZE
                if game_map[i][j] == 1:
                    # pygame.draw.rect(window, pygame.Color("gray"), (x, y, cell_SIZE, cell_SIZE))
                    window.blit(img_wall_up, (x, y, cell_SIZE, cell_SIZE))
                # elif game_map[i][j] == 2:
                #     pygame.draw.rect(window, pygame.Color("green"), (x, y, cell_SIZE, cell_SIZE))
                elif game_map[i][j] == 3:
                    door = pygame.Rect(j * cell_SIZE, i * cell_SIZE, cell_SIZE, cell_SIZE)
                    if player.hitbox.colliderect(door) and player.Get_inv() == "Ключ":
                        print("Вы открыли дверь")
                        print(f"{player.Get_inv()} был израсходован")
                        player.Set_inv("")
                        game_map[i][j] = 9
                    # pygame.draw.rect(window, pygame.Color("brown"), (x, y, cell_SIZE, cell_SIZE))
                    window.blit(img_key_door, (x, y, cell_SIZE, cell_SIZE))
                elif game_map[i][j] == 10:
                    if trap_1 and trap_1_timer == 0:
                        plate_row, plate_col = find_plate_pos(game_map, 10)
                        direction = check_direction(i, j, plate_row, plate_col)
                        Bullet(x + cell_SIZE // 2, y + cell_SIZE // 2, 10, direction, BULLET_SPEED)
                        trap_1 = False
                        trap_1_timer = BULLET_CD
                    # pygame.draw.rect(window, pygame.Color("red"), (x, y, cell_SIZE, cell_SIZE))
                    window.blit(img_wall_up, (x, y, cell_SIZE, cell_SIZE))
                elif game_map[i][j] == 12:
                    if trap_2 and trap_2_timer == 0:
                        plate_row, plate_col = find_plate_pos(game_map, 12)
                        direction = check_direction(i, j, plate_row, plate_col)
                        Bullet(x + cell_SIZE // 2, y + cell_SIZE // 2, 10, direction, BULLET_SPEED)
                        trap_2 = False
                        trap_2_timer = BULLET_CD
                    # pygame.draw.rect(window, pygame.Color("red"), (x, y, cell_SIZE, cell_SIZE))
                    window.blit(img_wall_up, (x, y, cell_SIZE, cell_SIZE))
                elif game_map[i][j] == 14:
                    if trap_3 and trap_3_timer == 0:
                        plate_row, plate_col = find_plate_pos(game_map, 14)
                        direction = check_direction(i, j, plate_row, plate_col)
                        Bullet(x + cell_SIZE // 2, y + cell_SIZE // 2, 10, direction, BULLET_SPEED)
                        trap_3 = False
                        trap_3_timer = BULLET_CD
                    # pygame.draw.rect(window, pygame.Color("red"), (x, y, cell_SIZE, cell_SIZE))
                    window.blit(img_wall_up, (x, y, cell_SIZE, cell_SIZE))
                elif game_map[i][j] == 5:
                    key_h = pygame.Rect(x + cell_SIZE // 4, y + cell_SIZE // 4, cell_SIZE // 2, cell_SIZE // 2)
                    if player.hitbox.colliderect(key_h):
                        player.Set_inv("Ключ")
                        print(f"Вы подобрали {player.Get_inv()}")
                        game_map[i][j] = 0
                    # pygame.draw.rect(window, pygame.Color("yellow"), (x + cell_SIZE // 4, y + cell_SIZE // 4, cell_SIZE // 2, cell_SIZE // 2))
                    # window.blit(img_floor, (x, y, cell_SIZE, cell_SIZE))
                    window.blit(img_key, (x + cell_SIZE // 4, y + cell_SIZE // 4, cell_SIZE // 2, cell_SIZE // 2))
                elif game_map[i][j] == 6 or game_map[i][j] == 11 or game_map[i][j] == 13 or game_map[i][j] == 15:
                    plate = pygame.Rect(x, y, cell_SIZE, cell_SIZE)
                    if player.hitbox.colliderect(plate) and game_map[i][j] == 6:
                        pygame.draw.rect(window, pygame.Color("khaki"), (x, y, cell_SIZE, cell_SIZE))
                        # window.blit(img_plate_act, (x, y, cell_SIZE, cell_SIZE))
                        door_plate = True
                    elif player.hitbox.colliderect(plate) and game_map[i][j] == 11:
                        trap_1 = True
                        pygame.draw.rect(window, pygame.Color("khaki"), (x, y, cell_SIZE, cell_SIZE))
                        # window.blit(img_plate_act, (x, y, cell_SIZE, cell_SIZE))
                    elif player.hitbox.colliderect(plate) and game_map[i][j] == 13:
                        trap_2 = True
                        pygame.draw.rect(window, pygame.Color("khaki"), (x, y, cell_SIZE, cell_SIZE))
                        # window.blit(img_plate_act, (x, y, cell_SIZE, cell_SIZE))
                    elif player.hitbox.colliderect(plate) and game_map[i][j] == 15:
                        trap_3 = True
                        pygame.draw.rect(window, pygame.Color("khaki"), (x, y, cell_SIZE, cell_SIZE))
                        # window.blit(img_plate_act, (x, y, cell_SIZE, cell_SIZE))
                    else:
                        # window.blit(img_floor, (x, y, cell_SIZE, cell_SIZE))
                        pygame.draw.rect(window, pygame.Color("orange"), (x, y, cell_SIZE, cell_SIZE))
                elif game_map[i][j] == 7:
                    if door_plate:
                        game_map[i][j] = 8
                    else:
                        pygame.draw.rect(window, pygame.Color("brown"), (x, y, cell_SIZE, cell_SIZE))
                # elif game_map[i][j] == 8:
                #     pygame.draw.rect(window, pygame.Color("darkgreen"), (x, y, cell_SIZE, cell_SIZE))
                # elif game_map[i][j] == 9:
                    # pygame.draw.rect(window, pygame.Color("darkgreen"), (x, y, cell_SIZE, cell_SIZE))
                    # window.blit(img_floor, (x, y, cell_SIZE, cell_SIZE))
                elif game_map[i][j] == 16:
                    pygame.draw.rect(window, pygame.Color("purple"), (x, y, cell_SIZE, cell_SIZE))
                    exit = pygame.Rect(x + cell_SIZE // 4, y + cell_SIZE // 4, cell_SIZE // 2, cell_SIZE // 2)
                    if player.hitbox.colliderect(exit):
                        state = "win"
                elif game_map[i][j] == 17:
                    pygame.draw.rect(window, pygame.Color("pink"), (x, y, cell_SIZE, cell_SIZE))
                elif game_map[i][j] == 18:
                    pygame.draw.rect(window, pygame.Color("violet"), (x, y, cell_SIZE, cell_SIZE))
                # else:
                #     window.blit(img_floor, (x, y, cell_SIZE, cell_SIZE))
                # else:
                #     pygame.draw.rect(window, pygame.Color("gray"), (x, y, cell_SIZE, cell_SIZE), 1)

        for bullet in bullets:
            bullet.update(WIDTH, HEIGHT, game_map, cell_SIZE)
            if player.hitbox.collidepoint(bullet.x, bullet.y):
                print("Игрок поражен пулей!")
                state = "dead"
                game_map = copy.deepcopy(game_map_restart)
                key_left_pressed = False
                key_right_pressed = False
                key_up_pressed = False
                key_down_pressed = False
                player.Change_moving(True)
                door_plate = False
                trap_1 = False
                trap_2 = False
                trap_3 = False
                trap_1_timer = 0
                trap_2_timer = 0
                trap_3_timer = 0
                bullets.clear()
                inv = ""
                player.hitbox.x = START_X
                player.hitbox.y = START_Y
        for bullet in bullets:
            bullet.draw(window)


        pygame.draw.rect(window, (255, 0, 0), player.hitbox)
        window.blit(img_player, player.hitbox)

        if trap_1_timer > 0:
            trap_1_timer -= 1
            trap_1 = False
        if trap_2_timer > 0:
            trap_2_timer -= 1
            trap_2 = False
        if trap_3_timer > 0:
            trap_3_timer -= 1
            trap_3 = False

        # Отображение инвентаря
        level = FONT.render(f"Уровень: " + str(level_number), True, (255, 255, 255), 1)
        inventory = FONT.render(f"Инвентарь: " + player.Get_inv(), True, (255, 255, 255), 1)
        window.blit(level, (30, 20))
        window.blit(inventory, (30, 680))

        pygame.display.update()
        clock.tick(FPS)

    return 1