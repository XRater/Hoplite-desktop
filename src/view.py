import curses


class View(object):
    QUIT_BUTTON = 'q'

    def __init__(self, model):
        self.model = model

    def _start_game(self, stdscr):
        command = 0
        stdscr.clear()
        stdscr.refresh()

        while command != ord(self.QUIT_BUTTON):
            stdscr.clear()
            self.height, self.width = stdscr.getmaxyx()

            if command == curses.KEY_RIGHT:
                pass
            if command == curses.KEY_LEFT:
                pass
            if command == curses.KEY_UP:
                pass
            if command == curses.KEY_DOWN:
                pass

            self.draw_game(stdscr)

            self._print_footer(stdscr)
            stdscr.refresh()
            command = stdscr.getch()

    def _print_footer(self, stdscr):
        footer = "Press {} to exit".format(self.QUIT_BUTTON)
        stdscr.addstr(self.height - 1, 0, footer)
        stdscr.addstr(self.height - 1, len(footer), " " * (self.width - len(footer) - 1))

    def _draw_menu(self, stdscr):
        command = 0

        stdscr.clear()
        stdscr.refresh()

        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

        while command != ord(self.QUIT_BUTTON):
            stdscr.clear()
            self.height, self.width = stdscr.getmaxyx()

            if command == ord(' '):
                self._start_game(stdscr)
                break

            # Declaration of strings
            title = "Hi there! Check out our best game!"
            subtitle = "Press SPACE to start game"

            start_x_title = self.width // 2 - len(title) // 2 - len(title) % 2
            start_x_subtitle = self.width // 2 - len(subtitle) // 2 - len(subtitle) % 2
            start_y = self.height // 2 - 2

            stdscr.attron(curses.color_pair(1))
            stdscr.attron(curses.A_BOLD)

            stdscr.addstr(start_y, start_x_title, title)
            stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)

            stdscr.attroff(curses.color_pair(1))
            stdscr.attroff(curses.A_BOLD)

            self._print_footer(stdscr)

            stdscr.refresh()
            command = stdscr.getch()

        self._process_exit()

    def start(self):
        curses.wrapper(self._draw_menu)

    def _process_exit(self):
        pass

    def draw_game(self, stdscr):
        field = [['#'] * self.model.width] * self.model.height

        for (cell, _) in self.model.rooms:
            field[cell.row][cell.column] = '.'

        for (cell, _) in self.model.doors:
            field[cell.row][cell.column] = 'o'

        for (cell, _) in self.model.game_objects:
            field[cell.row][cell.column] = '@'

        for i in range(min(self.model.height, self.height)):
            for j in range(min(self.model.width, self.width)):
                stdscr.addstr(i, j, field[i][j])
