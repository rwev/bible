import curses
from curses import wrapper
import reader
import textwrap

TRANSLATIONS_WIDTH = 6
BOOKS_WIDTH = 14
CHAPTERS_WIDTH = 4
TEXT_WIDTH = 25
VERSES_WIDTH = 4

class ListWindow():
    def __init__(self, win, title, item_tuples, width):

        # win.addstr(title)
        # win.box()

        self._win = win
        self._width = width

        self._selected_tuple = item_tuples[0]
        self.set_selection_tuples(item_tuples)
        
    def get_selection_tuple(self):
        return self._selected_tuple

    def set_selection_tuples(self, item_tuples):
        self._item_tuples = item_tuples
        if self._selected_tuple not in item_tuples:
            self._selected_tuple = self._item_tuples[0]
        self._bounds = (0, curses.LINES - 2)
        self.draw()

    def increment_selection(self, i):
        new_index = self._selected_tuple[0] + i
        if new_index < 0 or new_index >= len(self._item_tuples):
            return

        self._selected_tuple = self._item_tuples[self._selected_tuple[0] + i]
        self.update_bounds()
        self.draw()

    def update_bounds(self):
        index = self._selected_tuple[0]
        (bound_lower, bound_upper) = self._bounds
        if index >= bound_upper and index < len(self._item_tuples):
            self._bounds = (bound_lower + 1, bound_upper + 1)
        elif index < self._bounds[0]:
            self._bounds = (bound_lower - 1, bound_upper - 1) 
    
    def draw(self):
        self._win.clear()
        for (i, val) in self._item_tuples[self._bounds[0]:self._bounds[1]]:
            y = 1 + i - self._bounds[0]
            str_len = self._width - 2
            string = str(val).ljust(str_len)

            if i == self._selected_tuple[0]:
                self._win.addnstr(y, 1, string, str_len, curses.A_STANDOUT)
            else: 
                self._win.addnstr(y, 1, string, str_len)
        self._win.refresh()

def main(stdscr):
    stdscr.clear()

    def make_enumeration(list_):
        return list(enumerate(list_))
  
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

        book = books_win.get_selection_tuple()[1]
        
        chapter_tuples = make_enumeration(reader.get_chapters(book))

        chapters_win.set_selection_tuples(chapter_tuples)


    def update_text():
        text_win.clear()
        raw_text = reader.get_chapter_text(
                books_win.get_selection_tuple()[1],
                chapters_win.get_selection_tuple()[1],
                )
        text = ' '.join(
                textwrap.fill(
                    raw_text,
                    text_width - 4
                ).split('\n')[0: curses.LINES - 2])
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
