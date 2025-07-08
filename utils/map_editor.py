import pygame
pygame.init()


WIDTH = 840
HEIGHT = 720
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

cell_SIZE = 60
map = []
map_WIDTH = WIDTH // cell_SIZE
map_HEIGHT = HEIGHT // cell_SIZE


for i in range(map_HEIGHT):
    line = []
    for j in range(map_WIDTH):
        line.append(0)
    map.append(line)

plate_door = False
trap = False
key = False
plate = False
play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            file = open("../levels/Level_2_map.txt", "w")
            for i in range(map_HEIGHT):
                for j in range(map_WIDTH):
                    file.write(str(map[i][j]))
            file.close()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
            try:
                file = open("../levels/Level_2_map.txt", "r")
                i = 0
                j = 0
                for line in file:
                    for s in line:
                        map[i][j] = int(s)
                        j += 1
                        if j >= map_WIDTH:
                            j = 0
                            i += 1
                file.close()
            except:
                print("File opening error")
        if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
            trap = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
            key = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            plate = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            plate_door = True


    mouse_PX, mouse_PY = pygame.mouse.get_pos()
    b1, b2, b3 = pygame.mouse.get_pressed()

    mouse_row, mouse_col = mouse_PY // cell_SIZE, mouse_PX // cell_SIZE
    if b1:
        map[mouse_row][mouse_col] = 1
    elif b3:
        map[mouse_row][mouse_col] = 3
    elif b2:
        map[mouse_row][mouse_col] = 2
    elif trap:
        map[mouse_row][mouse_col] = 17
        trap = False
    elif key:
        map[mouse_row][mouse_col] = 18
        key = False
    elif plate:
        map[mouse_row][mouse_col] = 6
        plate = False
    elif plate_door:
        map[mouse_row][mouse_col] = 7
        plate_door = False

    window.fill(pygame.Color("black"))

    for i in range(map_HEIGHT):
        for j in range(map_WIDTH):
            x, y = j * cell_SIZE, i * cell_SIZE
            if map[i][j] == 1:
                pygame.draw.rect(window, pygame.Color("gray"), (x, y, cell_SIZE, cell_SIZE))
            elif map[i][j] == 2:
                pygame.draw.rect(window, pygame.Color("green"), (x, y, cell_SIZE, cell_SIZE))
            elif map[i][j] == 3:
                pygame.draw.rect(window, pygame.Color("blue"), (x, y, cell_SIZE, cell_SIZE))
            elif map[i][j] == 4:
                pygame.draw.rect(window, pygame.Color("red"), (x, y, cell_SIZE, cell_SIZE))
            elif map[i][j] == 5:
                pygame.draw.rect(window, pygame.Color("yellow"), (x, y, cell_SIZE, cell_SIZE))
            elif map[i][j] == 6:
                pygame.draw.rect(window, pygame.Color("orange"), (x, y, cell_SIZE, cell_SIZE))
            elif map[i][j] == 7:
                pygame.draw.rect(window, pygame.Color("brown"), (x, y, cell_SIZE, cell_SIZE))
            elif map[i][j] == 17:
                pygame.draw.rect(window, pygame.Color("pink"), (x, y, cell_SIZE, cell_SIZE))
            elif map[i][j] == 18:
                pygame.draw.rect(window, pygame.Color("violet"), (x, y, cell_SIZE, cell_SIZE))
            else:
                pygame.draw.rect(window, pygame.Color("gray"), (x, y, cell_SIZE, cell_SIZE), 1)

    pygame.display.update()
    clock.tick(FPS)


pygame.quit()
