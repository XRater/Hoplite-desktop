import sys

from src.game_controller.game_controller import GameController

if __name__ == "__main__":
    controller = GameController()

    if len(sys.argv) == 2:
        filename = sys.argv[1]
        controller.start_game(sys.argv[1])
    elif len(sys.argv) == 1:
        filename = None
    else:
        print("Incorrect usage. Please provide only 1 optional argument with pickle field.")
        exit(0)

    controller.start_game(filename)
