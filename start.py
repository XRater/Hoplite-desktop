import sys

from src.game_controller.game_controller import GameController

if __name__ == "__main__":
    controller = GameController()

    field_file = None
    if len(sys.argv) == 2:
        field_file = sys.argv[1]
        controller.start_game(sys.argv[1])
    elif len(sys.argv) != 1:
        print("Incorrect usage. Please provide only 1 optional argument with pickle field.")
        exit(0)

    controller.start_game(field_file)
