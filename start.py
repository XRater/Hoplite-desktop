import sys

from src.controller.controller import Controller

if __name__ == "__main__":
    if len(sys.argv) == 2:
        controller = Controller(sys.argv[1])
    elif len(sys.argv) == 1:
        controller = Controller()
    else:
        print("Incorrect usage. Please provide only 1 optional argument with pickle field.")
        exit(0)

    controller.start()
