#!/usr/bin/env python

import curses, random, time

screen = None
y = 8
x = 80
d = 1
c = 0
z = 0
l = 0
high = 10

def setup():
    global screen
    screen = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)


def end():
    global screen
    screen.nodelay(False)
    curses.nocbreak()
    curses.echo()
    curses.curs_set(1)
    curses.endwin()


def crash():
    global screen
    global high

    height, width = screen.getmaxyx()
    screen.nodelay(False)
    d = (l - 1) * 1000 + c
    a = "YOU CRASHED! YOU TRAVELLED {} METRES".format(d)
    screen.addstr(13, ((width - len(a)) / 2), a, curses.color_pair(4))
    if d > high:
        high = d
        a = "YOU GOT THE HIGH SCORE!!"
        screen.addstr(14, ((width - len(a)) / 2), a, curses.color_pair(4))


def crashanim():
    global screen

    for i in range (0, 6):
        s = "#" 
        scr.addstr(y, x, s, curses.color_pair(3))
        scr.addstr(y + 1, x, s, curses.color_pair(3))



def playagain():
    global screen
    height, width = screen.getmaxyx()
    #screen.clear()
    screen.nodelay(True)
    screen.addstr(15, ((width - 17) / 2), "PLAY AGAIN? (Y/N)", curses.color_pair(4))
    h = False
    o = None
    while h == False:
        a = screen.getch()
        if a == ord("y"):
            o = True
            h = True
        if a == ord("n"):
            o = False
            h = True
    return o


def init(scr):
    global x
    global d
    global c
    global l

    height, width = scr.getmaxyx()
    c = 0
    d = 1
    l = 1
    x = width / 2
    scr.clear()


def main(scr):
    global x
    global d
    global c
    global l
    global z
    global high

    height, width = scr.getmaxyx()
    scr.nodelay(True)
    scr.scrollok(True)
    pause = False
    play = True

    while play == True:
        # Play loop
        #
        init(scr)

        while True:
            # Game loop
            if pause == False:
                # Scroll if game is not paused
                scr.scroll(1)

            # Display the status bar at the top
            scr.addstr(0, 0, "Distance: {}".format((l - 1) * 1000 + c), curses.color_pair(3))
            s = "High Score: {}".format(high)
            w = (width - len(s)) / 2
            scr.addstr(0, w, s, curses.color_pair(3))
            a = "Level: {}".format(l)
            scr.addstr(0, width - len(a), a, curses.color_pair(3))

            # Crash?
            a = scr.instr(y + 1, x, 1)
            if a == "X":
                crash()
                break

            # Check for a key press
            k = scr.getch()
            if k == ord("q"):
                break;
            if k == ord("p"):
                pause = not pause
            if k == ord(" "):
                d = d * -1

            if pause == False:
                x = x + d

                # Bounce off the edges
                if x < 2:
                    x = 2
                    d = 1
                if x > width - 2:
                    x = width - 3
                    d = -1

                # If the game is not paused, display the entities
                # Display the skier
                if d == 1:
                    scr.addstr(y - 1, x - 2, "\\ \\", curses.color_pair(2))
                    scr.addstr(y, x, "\\o\\", curses.color_pair(2))
                    #scr.addstr(y + 1, x + 1, "*", curses.color_pair(2))
                else:
                    scr.addstr(y - 1, x - 2, " / / ", curses.color_pair(2))
                    scr.addstr(y, x - 2, "/o/", curses.color_pair(2))
                    #scr.addstr(y + 1, x - 1, "*", curses.color_pair(2))

                # Every 1000 metres show the level-up banner
                if c == 500:
                    a = ""
                    for i in range(0, width - 1):
                        a = a + "@"
                    b = " LEVEL {} ".format(l)
                    scr.addstr(height - 1, 0, a, curses.color_pair(4))
                    scr.addstr(height - 1, ((width - len(b)) / 2), b, curses.color_pair(3))
                    c = 0
                    l = l + 1
                else:
                    # 'level' trees per level
                    if z >= 4:
                        for i in range(0, l):
                            t = random.randint(0, 100)
                            if t > (80 - (c / 10)):
                                t = random.randint(0, width - 2)
                                scr.addstr(height - 3, t + 1, "X", curses.color_pair(1))
                                scr.addstr(height - 2, t, "XXX", curses.color_pair(1))
                                scr.addstr(height - 1, t + 1, "X", curses.color_pair(1))
                        z = 0
                            
                scr.refresh()
                s = 0.01 * (3 - l)
                time.sleep(s)
                c = c + 1

                z = z + 1
            # End of game loop
        play = playagain()
    # end of play loop
    end()


setup()
screen.clear()
curses.wrapper(main)
