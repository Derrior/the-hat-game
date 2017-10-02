import core
#settings = core.Settings(["a", "b"], 0, 6, 20)
settings = core.requestSettings()
game = core.Game(settings)
import visual

previous_time = 0
def refreshWindows(game):
    global previous_time
    if (game.is_active_turn):
        t = game.get_time_remaining()
        if (t < 4):
            if (t != previous_time and t == 0):
                visual.curses.flash()
            visual.writeWord(visual.time_screen, "00:0%d" % t, visual.curses.A_DIM, visual.red)
            previous_time = t
        else:
            visual.writeWord(visual.time_screen, "00:" + str(t).rjust(2, '0'))
    else:
        visual.writeWord(visual.time_screen, "      ")

def switchResults():
    global results_active
    if (not results_active):
        visual.showResults(game.get_results())
        results_active = True
    else:
        visual.hideResults()
        results_active = False


results_active = False
log = open("log.txt", "w")
core.time.sleep(1)
while (game.get_current_words_amount() > 0):
    pair_row = " -> ".join(game.get_pair_names())
    print(pair_row, file=log)
    visual.writeWord(visual.players_screen, pair_row)
    visual.writeWord(visual.word_screen, game.get_current_word())
    visual.writeWord(visual.time_screen, "      ")
    visual.buttons_screen.nodelay(0)
    character = -1
    turn_begins = False

    while (not turn_begins):
        character = visual.buttons_screen.getch()
        if (character == '\n'):
            turn_begins = True
        elif character == visual.curses.KEY_MOUSE:
            mouse_id, x, y, z, state = visual.curses.getmouse()
            if not results_active and visual.pointInBox((x, y), visual.word_screen):
                turn_begins = True
            elif visual.pointInBox((x, y), visual.buttons_screen):
                switchResults()
            elif visual.pointInBox((x, y), visual.exit_button):
                visual.close_curses()
                exit(0)


    visual.buttons_screen.nodelay(1)
    game.turn()
    visual.writeWord(visual.word_screen, game.get_current_word())
    while game.is_active_turn:
        refreshWindows(game)
        character = visual.buttons_screen.getch()

        if (character == ord('\n')):
            game.success_word()
            visual.writeWord(visual.word_screen, game.get_current_word())
        elif character == visual.curses.KEY_MOUSE:
            mouse_id, x, y, z, state = visual.curses.getmouse()
            if visual.pointInBox((x, y), visual.word_screen):
                game.success_word()
                visual.writeWord(visual.word_screen, game.get_current_word())
            elif visual.pointInBox((x, y), visual.exit_button):
                visual.close_curses()
                exit(0)

visual.showResults(game.get_results())

while True:
    character = visual.buttons_screen.getch()
    if character == visual.curses.KEY_MOUSE:
        mouse_id, x, y, z, state = visual.curses.getmouse()
        if visual.pointInBox((x, y), visual.exit_button) or \
                visual.pointInBox((x, y), visual.buttons_screen):
            visual.close_curses()
            exit(0)


