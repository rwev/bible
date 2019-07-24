import curses
from curses import wrapper
import reader

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
BOOKS_WIDTH = 14
CHAPTERS_WIDTH = 10

def main(stdscr):
    stdscr.clear()
   
    trans_win = stdscr.derwin(curses.LINES, TRANSLATIONS_WIDTH, 0, 0)
    trans_win.box()
    trans_win.addstr('TRAN.')

    books_win = stdscr.derwin(curses.LINES, BOOKS_WIDTH, 0, TRANSLATIONS_WIDTH)
    books_win.box()
    books_win.addstr('BK.')

    # don't try to write outside the window!
    book_enums = list(enumerate(reader.get_books()))
    book_selection = book_enums[0]
    book_bounds = [0, curses.LINES - 2]

    def update_book_bounds():
        if book_selection[0] > book_bounds[1] and book_selection[0] < len(book_enums):
            return (book_bounds[0] + 1, book_bounds[1] + 1)
        elif book_selection[0] < book_bounds[0]:
            return (book_bounds[0] - 1, book_bounds[1] -1) 

    def draw_books():
        for (book_num, book_name) in book_enums[:curses.LINES-2]:
            if book_num == book_selection[0]:
                books_win.addnstr(1 + book_selection[0], 1, book_selection[1], BOOKS_WIDTH - 2, curses.A_STANDOUT)
            else: 
                books_win.addnstr(1 + book_num, 1, book_name, BOOKS_WIDTH - 2)
        books_win.refresh()
    
    
    draw_books()


    #chapters_win = stdscr.derwin(curses.LINES, CHAPTERS_WIDTH, 0,TRANSLATIONS_WIDTH + BOOKS_WIDTH)
    #chapters_win.box()
    #chapters_win.addstr('CH.')

    #books_win.refresh()
    #trans_win.refresh() 

    #stdscr.refresh()
    
    key = None
    while (key != 'q'): # TODO quit not working
        key = stdscr.getch()
        if key == curses.KEY_UP:
            book_selection = book_enums[book_selection[0] - 1]
            book_bounds = update_book_bounds()
            draw_books()
        elif key == curses.KEY_DOWN:
            book_selection = book_enums[book_selection[0] + 1]
            book_bounds = update_book_bounds()
            draw_books()


wrapper(main)            
