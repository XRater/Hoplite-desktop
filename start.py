import sys

from src.game_controller.app_controller import AppController

if __name__ == "__main__":
    controller = AppController()

    field_file = None
    if len(sys.argv) == 2:
        field_file = sys.argv[1]
        controller.start()
    elif len(sys.argv) != 1:
        print("Incorrect usage. Please provide only 1 optional argument with pickle field.")
        exit(0)

    controller.start()
