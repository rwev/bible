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
    reader.set_root('AMP')

    translations_win = ListWindow(
            stdscr.derwin(
                curses.LINES,
                TRANSLATIONS_WIDTH,
                0,
                0
                ),
            'TR',
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
                    'BOOK',
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
                    'CH',
                    make_enumeration(reader.get_chapters('Genesis')),
                    CHAPTERS_WIDTH
                    )

    verses_win = ListWindow(
            stdscr.derwin(
                curses.LINES,
                VERSES_WIDTH,
                0,
                TRANSLATIONS_WIDTH + BOOKS_WIDTH
                + CHAPTERS_WIDTH  #curses.COLS - VERSES_WIDTH,
                ),
            'VS',
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
    selected_window[1].set_active(True)

    text_width= curses.COLS - TRANSLATIONS_WIDTH - BOOKS_WIDTH - CHAPTERS_WIDTH - VERSES_WIDTH
    text_start = TRANSLATIONS_WIDTH + BOOKS_WIDTH + CHAPTERS_WIDTH + VERSES_WIDTH # TODO smarter start vars
    text_outer_win = stdscr.derwin(
                curses.LINES,
                text_width, 
                0,
                text_start
                )
    text_outer_win.box()
    # text_outer_win.vline(0, 0, '|', curses.LINES)


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

        chapter = chapters_win.get_selection_tuple()[1]

        verses_tuples = make_enumeration(
                reader.get_verses(book, chapter)
                )

        verses_win.set_selection_tuples(verses_tuples)

    h_en = Hyphenator('en_US')
    def update_text():
        
        trans_name = translations_win.get_selection_tuple()[1]
        book_name = books_win.get_selection_tuple()[1]
        chapter_name = chapters_win.get_selection_tuple()[1],
        verse = verses_win.get_selection_tuple()[1]

        text_title = " {0} {1}:{3} [{2}]".format(book_name, str(chapter_name[0]), trans_name, verse) # TODO
        text_title_centered = text_title.center(text_width, ' ')

        start_pad = len(text_title_centered) - len(text_title_centered.lstrip(' '))

        text_outer_win.clear()
        text_outer_win.box()
        text_outer_win.addstr(0, start_pad, text_title)
        text_outer_win.refresh()
       
        text_win.clear()
        
        raw_text = reader.get_chapter_text(
                books_win.get_selection_tuple()[1],
                chapters_win.get_selection_tuple()[1],
                verse_start = verse                )
        text = '\n'.join(
                wrap(
                    str(raw_text).decode('utf8'),
                    width=text_width - 3,
                    use_hyphenator=h_en
                )[0: curses.LINES - 2])
        text_win.addstr(text)
        text_win.refresh()

    def deactivate_all_windows():
        for (i, win) in windows_tuples:
            win.set_active(False)

    update_selections()
    update_text()
    
    key = None
    while (key != ord('q')): # TODO quit not working
        key = stdscr.getch()
        if key == curses.KEY_UP:
            selected_window[1].increment_selection(-1)
        elif key == curses.KEY_DOWN:
            selected_window[1].increment_selection(1)
        elif key == curses.KEY_LEFT:
            deactivate_all_windows()
            new_windex = selected_window[0] - 1
            if new_windex < 0: new_windex = len(windows_tuples) - 1
            selected_window = windows_tuples[new_windex]
            selected_window[1].set_active(True)
        elif key == curses.KEY_RIGHT:
            deactivate_all_windows()
            new_windex = selected_window[0] + 1
            if new_windex >= len(windows_tuples): new_windex = 0
            selected_window = windows_tuples[new_windex]
            selected_window[1].set_active(True)
        update_selections()
        update_text()


wrapper(main)            
