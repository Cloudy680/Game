import copy

def find_plate_pos(game_map, trap_n):
    for i in range(len(game_map)):
        for j in range(len(game_map[0])):
            if game_map[i][j] == trap_n + 1:
                return i, j
    return None


def check_direction(trap_row, trap_col, plate_row, plate_col):
    if trap_row == plate_row and trap_col < plate_col:
        return "RIGHT"
    elif trap_row == plate_row and trap_col > plate_col:
        return "LEFT"
    elif trap_col == plate_col and trap_row > plate_row:
        return "UP"
    elif trap_col == plate_col and trap_row < plate_row:
        return "DOWN"


def load_game_map(game_map, level_number, game_map_WIDTH):
    try:
        file = open(f"assets/Level_{level_number}_map.txt", "r")
        i = 0
        j = 0
        for line in file:
            words = line.split()
            for s in words:
                game_map[i][j] = int(s)
                j += 1
                if j >= game_map_WIDTH:
                    j = 0
                    i += 1
        file.close()
    except:
        print("File opening error")
    game_map_restart = copy.deepcopy(game_map)
    return game_map, game_map_restart

def get_start_coordinats(game_map, cell_SIZE):
    START_X, START_Y = 0, 0
    for i in range(len(game_map)):
        for j in range(len(game_map[0])):
            if int(game_map[i][j]) == 2:
                START_X, START_Y = j, i
    START_X = START_X * cell_SIZE + cell_SIZE / 4
    START_Y = START_Y * cell_SIZE + cell_SIZE / 4
    return START_X, START_Y