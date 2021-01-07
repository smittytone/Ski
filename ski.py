#!/usr/bin/env python3
# You may need to change the above line for your system

"""
Ski 2.0.2
=========

Copyright 2021, Tony Smith (@smittytone)
License: MIT (terms attached to this repo)

About Ski
---------

VERY crude text-screen game derived from something I hacked up from a pal's
original Basic code back in 1983.

Curses info: https://docs.python.org/3/howto/curses.html

"""


##########################################################################
# Program library imports                                                #
##########################################################################

import curses
import curses.ascii
import random
import time


##########################################################################
# Application globals                                                    #
##########################################################################

x = 80
y = 8
delta = 1
metres = 0
gap_count = 0
level = 0
high_score = 100
high_score_table = []
high_score_table.append({"score": 100, "name" : "AMD"})
speed = 0.06
ghost = False


##########################################################################
# Functions                                                              #
##########################################################################

def setup():
    """
    Set up curses
    """

    # Create a window
    screen = curses.initscr()

    # Set up curses' colours
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_WHITE)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(7, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
    curses.init_pair(8, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Set the background of the window to be white
    screen.bkgd(curses.ascii.SP, curses.color_pair(6))

    # Configure curses
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

    return screen


def end(screen):
    """
    Tear down curses before quitting
    """

    screen.nodelay(False)
    curses.nocbreak()
    curses.echo()
    curses.curs_set(1)
    curses.endwin()


def crash(screen):
    """
    Tear down curses before quitting
    """

    _, width = screen.getmaxyx()
    crash_animation(screen)
    screen.nodelay(False)
    distance = (level - 1) * 1000 + metres
    text = "YOU CRASHED! YOU TRAVELLED {} METRES".format(distance)
    screen.addstr(13, int((width - len(text)) / 2), text, curses.color_pair(4))
    check_score(distance, screen)


def print_high_table(screen):
    """
    Print out the high score table first
    """

    _, width = screen.getmaxyx()
    screen.addstr(21, int((width - 24) / 2), "+-- HIGH SCORE TABLE --+", curses.color_pair(4))
    count = 1
    for result in high_score_table:
        text = str(result["score"])
        if result["score"] < 100: text = "000" + text
        if result["score"] < 1000: text = "00" + text
        if result["score"] < 10000: text = "0" + text
        text = "|   " + str(count) + ".  " + result["name"] + " - " + text + "   |"
        screen.addstr(21 + count, int((width - 24) / 2), text, curses.color_pair(4))
        count += 1
    screen.addstr(21 + count, int((width - 24) / 2), "+----------------------+", curses.color_pair(4))


def check_score(score, screen):
    """
    See if the player's score makes the high-score table
    """

    global high_score_table, high_score

    _, width = screen.getmaxyx()
    new_entry = {"score": score, "name" : "???"}

    if high_score_table:
        print_high_table(screen)

        # Now see if the input 'score' is on the table
        index = 0
        for result in high_score_table:
            if score > result["score"]: break
            index += 1

        if index >= 0:
            text = "YOU GOT ON THE HIGHSCORE TABLE!!"
            screen.addstr(14, int((width - 32) / 2), text, curses.color_pair(4))
            high_score_table.insert(index, new_entry)
            if len(high_score_table) > 5: 
                high_score_table.pop()
                print(index)
            get_initials(high_score_table[index], screen)
        elif score >= 0:
            if len(high_score_table) < 5:
                high_score_table.append(new_entry)
                get_initials(high_score_table[len(high_score_table) - 1], screen)
    else:
        high_score_table.append(new_entry)
        high_score = score
        get_initials(high_score_table[0], screen)

    # Finally, set the displayed high score
    for result in high_score_table:
        if result["score"] > high_score: high_score = result["score"]


def get_initials(entry, screen):
    """
    Get the player's initials
    """
    curses.flushinp()
    _, width = screen.getmaxyx()
    text = "PLEASE ENTER YOUR THREE INITIALS: "
    screen.addstr(15, int((width - 34) / 2), text, curses.color_pair(4))
    text = ""
    while len(text) < 3:
        key = screen.getch()
        text += chr(key).upper()
        screen.addstr(16, int((width - len(text)) / 2), text, curses.color_pair(4))
    entry["name"] = text


def crash_animation(screen):
    """
    Display a crash animation
    """

    _, width = screen.getmaxyx()
    screen.addstr(y - 1, x - 1, " o ", curses.color_pair(8))
    y_pos = y - 1
    x_right = x + 1
    x_left = x - 1

    for i in range(1, 9):
        x_right = x + i
        x_left = x - i
        if x_right < width: screen.addstr(y_pos, x_right, "|", curses.color_pair(8))
        if x_left > -1: screen.addstr(y_pos, x_left, "|", curses.color_pair(8))
        screen.refresh()
        time.sleep(0.1)
        screen.addstr(y_pos, x_right, " ", curses.color_pair(8))
        screen.addstr(y_pos, x_left, " ", curses.color_pair(8))
        screen.refresh()
        time.sleep(0.05)
        y_pos += 1

    screen.addstr(y - 1, x - 1, "RIP", curses.color_pair(8))


def play_again(screen):
    """
    Ask the player if they want another go
    """

    _, width = screen.getmaxyx()
    screen.nodelay(True)
    text = "PLAY AGAIN?  (Y/N)"
    screen.addstr(17, int((width - 18) / 2), text, curses.color_pair(4))
    done = False
    replay = None
    while done is False:
        key = screen.getch()
        if key == ord("y"):
            replay = True
            done = True
            init_game(screen)
        if key == ord("n"):
            replay = False
            done = True
    return replay


def init_game(screen):
    """
    Initialize a game's key variables (globals)
    """

    global x, delta, metres, level, speed, ghost

    screen.clear()
    _, width = screen.getmaxyx()
    x = int(width / 2)
    delta = 1
    metres = 0
    level = 1
    speed = 0.06
    ghost = False


def main(a_screen):
    """
    Main game operational section, handling the key game loops.

    Args:
        a_screen (curses.window): The window object supplied by curses.
    """

    global x, delta, metres, level, gap_count, high_score, ghost, speed

    # Set the window
    height, width = a_screen.getmaxyx()
    a_screen.nodelay(True)
    a_screen.scrollok(True)

    pause = False
    play = True
    ghost_count = 0
    prize_off_screen = 0

    while play is True:
        # Play loop
        # Initialize the game
        init_game(a_screen)

        while True:
            # Game loop
            if pause is False:
                # Scroll if the game is not paused
                a_screen.scroll(1)

            # Display the status bar at the top
            text = "Distance: {}".format((level - 1) * 1000 + metres)
            a_screen.addstr(0, 0, text, curses.color_pair(7))
            text = "High Score: {}".format(high_score)
            a_screen.addstr(0, int((width - len(text)) / 2), text, curses.color_pair(7))
            text = "Level: {}".format(level)
            a_screen.addstr(0, (width - len(text)), text, curses.color_pair(7))

            # Crash?
            peek = a_screen.instr(y + 1, x - 1, 3)
            if peek[0] == 88 or peek[1] == 88 or peek[2] == 88:
                if ghost is False:
                    crash(a_screen)
                    break
            if peek[0] == 42 or peek[1] == 42 or peek[2] == 42:
                ghost = True
                ghost_count = 0

            # Preserve previous positioning values
            x_old = x
            delta_old = delta

            # Check for a key press
            key = a_screen.getch()
            if key == ord("q"):
                print_high_table(a_screen)
                break
            if key == ord("p"): pause = not pause
            if key == ord(" "): delta *= -1
            if key == ord("z"): ghost = True

            if pause is False:
                x += delta

                # Bounce off the edges
                if x < 2:
                    x = 2
                    delta = 1
                if x > width - 2:
                    x = width - 3
                    delta = -1

                # Draw the skier's tracks
                if delta_old == 1:
                    a_screen.addstr(y - 1, x_old - 1, "\\ \\", curses.color_pair(5))
                else:
                    a_screen.addstr(y - 1, x_old - 1, "/ /", curses.color_pair(5))

                colour = curses.color_pair(2)
                if ghost is True:
                    colour = curses.color_pair(5)
                    if ghost_count > 150 and ghost_count % 8 == 0: colour = curses.color_pair(2)

                # Draw the skier
                if delta == 1:
                    a_screen.addstr(y, x - 1, "\\o\\", colour)
                else:
                    a_screen.addstr(y, x - 1, "/o/", colour)

                # Every 1000 metres show the level-up banner
                if metres == (1000 - height + 8):
                    text = ""
                    for _ in range(0, width - 1): text += "@"
                    a_screen.addstr(height - 1, 0, text, curses.color_pair(4))
                    text = " LEVEL {} ".format(level)
                    a_screen.addstr(height - 1, int((width - len(text)) / 2), text, curses.color_pair(3))
                elif metres == 1000:
                    metres = 0
                    level += 1
                    speed = 0.06 - (0.005 * level)
                else:
                    # Up to 6 trees per level
                    if gap_count >= 4:
                        for _ in range(0, 6):
                            tree_pos = random.randint(0, 100)
                            if tree_pos > (80 - (metres / 10)):
                                tree_pos = random.randint(0, width - 3)
                                a_screen.addstr(height - 3, tree_pos + 1, "X", curses.color_pair(1))
                                a_screen.addstr(height - 2, tree_pos, "XXX", curses.color_pair(1))
                                a_screen.addstr(height - 1, tree_pos + 1, "W", curses.color_pair(9))
                        if ghost is False and prize_off_screen < 0:
                            tree_pos = random.randint(0, 100)
                            if tree_pos < 8:
                                tree_pos = random.randint(0, width - 6)
                                a_screen.addstr(height - 3, tree_pos, "  *  ", curses.color_pair(8))
                                a_screen.addstr(height - 2, tree_pos, " *** ", curses.color_pair(8))
                                a_screen.addstr(height - 1, tree_pos, "  W  ", curses.color_pair(9))
                                prize_off_screen = height - 2
                        gap_count = 0

                    # Place some 'dirt' for colour
                    tree_pos = random.randint(0, 100)
                    if tree_pos > 60:
                        tree_pos = random.randint(0, width - 2)
                        a_screen.addstr(height - 1, tree_pos, ".", curses.color_pair(9))

                # Per loop is approx. 200ms
                a_screen.refresh()
                time.sleep(speed)

                metres += 1
                gap_count += 1
                prize_off_screen -= 1

                if ghost is True:
                    if ghost_count > 200:
                        ghost_count = 0
                        ghost = False
                    else:
                        ghost_count += 1

            # End of game loop

        play = play_again(a_screen)
        pause = not play

    # end of play loop
    end(a_screen)


##########################################################################
# Main entry point                                                       #
##########################################################################

if __name__ == '__main__':

    # Set up the screen and curses
    setup()

    # Begin the game loops by running curses
    curses.wrapper(main)
