import curses


def print_with_custom_color(console, y, x, text, color):
    console.attron(curses.color_pair(color))
    console.attron(curses.A_BOLD)
    console.addstr(y, x, text)
    console.attroff(curses.color_pair(color))
    console.attroff(curses.A_BOLD)


def print_footer(console, height, width):
    from src.view.console_view import ConsoleView
    footer = f'Press {ConsoleView.QUIT_BUTTON} to exit'
    console.addstr(height - 1, 0, footer)
    console.addstr(height - 1, len(footer), ' ' * (width - len(footer) - 1))


def print_in_the_middle(console, y, width, text, color):
    start_x_title = width // 2 - len(text) // 2 - len(text) % 2
    print_with_custom_color(console, y, start_x_title, text, color)
