import curses

from curses import wrapper


# WRAPPER HANDLES AUTOMAGICALLY
# start
# stdscr = curses.initscr()
# curses.noecho()
# curses.cbreak()
# stdscr.keypad(True)


# end
# curses.nocbreak()
# stdscr.keypad(False)
# curses.echo()
# curses.endwin()

TRANSLATIONS_WIDTH = 10
BOOKS_WIDTH = 10
CHAPTERS_WIDTH = 10

def main(stdscr):
    
    stdscr.clear()
   
    trans_win = stdscr.derwin(curses.LINES, TRANSLATIONS_WIDTH, 0, 0)
    trans_win.box()
    trans_win.addstr('TRANS')

    books_win = stdscr.derwin(curses.LINES, BOOKS_WIDTH, 0, TRANSLATIONS_WIDTH)
    books_win.box()
    books_win.addstr('BOOK')

    chapters_win = stdscr.derwin(curses.LINES, CHAPTERS_WIDTH, 0,TRANSLATIONS_WIDTH + BOOKS_WIDTH)
    chapters_win.box()
    chapters_win.addstr('CH.')

    books_win.refresh()
    trans_win.refresh() 

    stdscr.refresh()
    stdscr.getkey()

wrapper(main)
