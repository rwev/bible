import curses
from curses import wrapper
from reader import Reader
from list import ListWindow
# import textwrap
from textwrap2 import wrap 
from hyphen import Hyphenator


TRANSLATIONS_WIDTH = 6
BOOKS_WIDTH = 14
CHAPTERS_WIDTH = 4
TEXT_WIDTH = 25
VERSES_WIDTH = 4

def main(stdscr):
    stdscr.clear()

    def make_enumeration(list_):
        return list(enumerate(list_))
  
    reader = Reader()
    reader.set_root('MSG')

    translations_win = ListWindow(
            stdscr.derwin(
                curses.LINES,
                TRANSLATIONS_WIDTH,
                0,
                0
                ),
            'T.',
            make_enumeration(reader.get_translations()),
            TRANSLATIONS_WIDTH
            )
    
    books_win = ListWindow(
                    stdscr.derwin(
                        curses.LINES,
                        BOOKS_WIDTH,
                        0,
                        TRANSLATIONS_WIDTH
                    ),
                    'BK.',
                    make_enumeration(reader.get_books()),
                    BOOKS_WIDTH
                    )

    chapters_win = ListWindow(
            stdscr.derwin(
                curses.LINES,
                CHAPTERS_WIDTH, 
                0, 
                TRANSLATIONS_WIDTH + BOOKS_WIDTH
                ),
            'CH.',
            make_enumeration(reader.get_chapters('Genesis')),
            CHAPTERS_WIDTH
            )

    verses_win = ListWindow(
            stdscr.derwin(
                curses.LINES,
                VERSES_WIDTH,
                0,
                curses.COLS - VERSES_WIDTH,
                ),
            'VS.',
            make_enumeration(reader.get_verses('Genesis', 1)), # TODO
            VERSES_WIDTH
            )


    windows_tuples = make_enumeration([
            translations_win,
            books_win,
            chapters_win,
            verses_win
            ])
    selected_window = windows_tuples[1]

    text_width= curses.COLS - TRANSLATIONS_WIDTH - BOOKS_WIDTH - CHAPTERS_WIDTH - VERSES_WIDTH
    text_start = TRANSLATIONS_WIDTH + BOOKS_WIDTH + CHAPTERS_WIDTH
    text_outer_win = stdscr.derwin(
                curses.LINES,
                text_width, 
                0,
                text_start
                )
    text_outer_win.box()



    text_win = text_outer_win.derwin(
            curses.LINES - 2,
            text_width - 2,
            1, 
            1,
            )

    def update_selections():
        # TODO translations
        trans = translations_win.get_selection_tuple()[1]
        reader.set_root(trans)

        book = books_win.get_selection_tuple()[1]
        
        chapter_tuples = make_enumeration(reader.get_chapters(book))

        chapters_win.set_selection_tuples(chapter_tuples)


    h_en = Hyphenator('en_US')
    def update_text():
        text_win.clear()
        raw_text = reader.get_chapter_text(
                books_win.get_selection_tuple()[1],
                chapters_win.get_selection_tuple()[1],
                )
        text = '\n'.join(
                wrap(
                    str(raw_text).decode('utf8'),
                    width=text_width - 3,
                    use_hyphenator=h_en
                )[0: curses.LINES - 2])
        text_win.addstr(text)
        text_win.refresh()

    update_selections()
    update_text()
    
    key = None
    while (key != 'q'): # TODO quit not working
        key = stdscr.getch()
        if key == curses.KEY_UP:
            selected_window[1].increment_selection(-1)
        elif key == curses.KEY_DOWN:
            selected_window[1].increment_selection(1)
        elif key == curses.KEY_LEFT:
            new_windex = selected_window[0] - 1
            if new_windex < 0: new_windex = len(windows_tuples) - 1
            selected_window = windows_tuples[new_windex]
        elif key == curses.KEY_RIGHT:
            new_windex = selected_window[0] + 1
            if new_windex >= len(windows_tuples): new_windex = 0
            selected_window = windows_tuples[new_windex]
        update_selections()
        update_text()


wrapper(main)            
