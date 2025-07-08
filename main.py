import pygame
from src.game_logic import run_game
from src.menu import show_menu
from some_game import run_game_e
from src.final_msg import show_final_msg

levels_amount = 3

def main():
    pygame.init()
    check = 1
    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
        choice = show_menu()
        if choice == "Играть":
            for i in range(levels_amount):
                if i <= 1:
                    if check == 1:
                        check = run_game(i + 1)
                    else:
                        pygame.quit()
                        return
                else:
                    run_game_e()
                    show_final_msg()
        elif choice == "Настройки":
            print("Настройки покане реализованы")
        elif choice == "Выход":
            pygame.quit()
            return
        play = False
    return

if __name__ == "__main__":
    main()