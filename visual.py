import core
import time
import curses

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
curses.curs_set(False)
curses.start_color()

curses.use_default_colors()
curses.init_pair(1, curses.COLOR_RED, -1)
curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
red = 1
stdscr.refresh()

def close_curses():
    stdscr.keypad(False)
    curses.nocbreak()
    curses.echo()
    curses.endwin()

def create_players_screen():
    begin_x = 5
    begin_y = 25
    height = 3
    width = 60
    win = curses.newwin(height, width, begin_x, begin_y)
    return win

def create_time_screen():
    begin_x = 15
    begin_y = 45
    height = 3
    width = 20
    win = curses.newwin(height, width, begin_x, begin_y)
    return win

def create_word_screen():
    begin_x = 11
    begin_y = 35
    height = 3
    width = 40
    win = curses.newwin(height, width, begin_x, begin_y)
    win.border()
    return win

def create_buttons_screen():
    begin_x = 20
    begin_y = 45
    height = 3
    width = 20
    win = curses.newwin(height, width, begin_x, begin_y)
    writeWord(win, "Show Results")
    win.border()
    begin_x = 3
    begin_y = 100
    height = 3
    width = 3
    exit = curses.newwin(height, width, begin_x, begin_y)
    exit.border()
    writeWord(exit, '᰽')
    return (win, exit)

def create_results_screen():
    begin_x = 9
    begin_y = 20
    height = 40
    width = 70
    win = curses.newwin(height, width, begin_x, begin_y)
    return win

def writeWord(word_screen, word, attr=0, color_pair=0):
    width = word_screen.getmaxyx()[1]
    word_screen.addstr(1, 1, ' ' * (width - 2))
    start_word = width // 2 - len(word) // 2
    word_screen.addstr(1, start_word, word, attr ^ curses.color_pair(color_pair))
    word_screen.refresh()


def hideResults():
    writeWord(buttons_screen, "Show Results")
    results_screen.clear()
    players_screen.redrawwin()
    time_screen.redrawwin()
    word_screen.redrawwin()
    buttons_screen.redrawwin()

    results_screen.refresh()
    players_screen.refresh()
    time_screen.refresh()
    word_screen.refresh()
    buttons_screen.refresh()

def pointInBox(point, screen):
    up, left = screen.getbegyx()
    height, width = screen.getmaxyx()
    return (0 <= point[1] - up <= height and 0 <= point[0] - left <= width)

def showResults(rows):
    width = results_screen.getmaxyx()[1]
    for i in range(len(rows)):
        row = rows[i]
        start_word = width // 2 - len(row) // 2
        results_screen.addstr(i, start_word, row)
    results_screen.redrawwin()
    results_screen.refresh()
    writeWord(buttons_screen, "Hide Results")
    buttons_screen.redrawwin()
    buttons_screen.refresh()


players_screen = create_players_screen()
time_screen = create_time_screen()
word_screen = create_word_screen()
buttons_screen, exit_button = create_buttons_screen()
buttons_screen.keypad(True)
curses.mousemask(True)
results_screen = create_results_screen()

