import curses
import logging

class View(object):
    QUIT_BUTTON = 'q'
    WELCOME_STRING = "Hi there! Check out our best game!"
    INSTRUCTION_STRING = "Press SPACE to start game"

    def __init__(self, controller, model):
        self.controller = controller
        self.model = model

    def start(self):
        curses.wrapper(self._draw_menu)

    def _start_game(self, console):
        command = 0
        console.clear()
        console.refresh()

        while command != ord(self.QUIT_BUTTON):
            console.clear()
            self.height, self.width = console.getmaxyx()

            if command == curses.KEY_RIGHT:
                self.controller.pressed_right()
            if command == curses.KEY_LEFT:
                self.controller.pressed_left()
            if command == curses.KEY_UP:
                self.controller.pressed_up()
            if command == curses.KEY_DOWN:
                self.controller.pressed_down()

            self._draw_game(console)

            self._print_footer(console)
            console.refresh()
            command = console.getch()

    def _print_footer(self, console):
        footer = "Press {} to exit".format(self.QUIT_BUTTON)
        console.addstr(self.height - 1, 0, footer)
        console.addstr(self.height - 1, len(footer), " " * (self.width - len(footer) - 1))

    def _draw_menu(self, console):
        command = 0

        console.clear()
        console.refresh()

        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

        while command != ord(self.QUIT_BUTTON):
            console.clear()
            self.height, self.width = console.getmaxyx()

            if command == ord(' '):
                self._start_game(console)
                break

            start_x_title = self.width // 2 - len(self.WELCOME_STRING) // 2 - len(self.WELCOME_STRING) % 2
            start_x_subtitle = self.width // 2 - len(self.INSTRUCTION_STRING) // 2 - len(self.INSTRUCTION_STRING) % 2
            start_y = self.height // 2 - 2

            console.attron(curses.color_pair(1))
            console.attron(curses.A_BOLD)

            console.addstr(start_y, start_x_title, self.WELCOME_STRING)
            console.addstr(start_y + 1, start_x_subtitle, self.INSTRUCTION_STRING)

            console.attroff(curses.color_pair(1))
            console.attroff(curses.A_BOLD)

            self._print_footer(console)

            console.refresh()
            command = console.getch()

        self._process_exit()

    def _process_exit(self):
        pass

    def _draw_game(self, stdscr):
        field = [['#'] * self.model.width] * self.model.height
        logging.info("Drawing field")
        for (cell, _) in self.model.rooms:
            field[cell.row][cell.column] = '.'

        for (cell, _) in self.model.doors:
            field[cell.row][cell.column] = 'o'

        for (cell, _) in self.model.game_objects:
            field[cell.row][cell.column] = '@'

        for i in range(min(self.model.height, self.height)):
            for j in range(min(self.model.width, self.width)):
                stdscr.addstr(i, j, field[i][j])
