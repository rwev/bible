import curses
from curses import wrapper
from reader import Reader
from list import ListWindow
from textwrap2 import wrap 
from hyphen import Hyphenator

TRANSLATIONS_WIDTH = 6
BOOKS_WIDTH = 14
CHAPTERS_WIDTH = 4
VERSES_WIDTH = 4

h_en = Hyphenator('en_US')

def make_enumeration(list_):
    return list(enumerate(list_))

class Main():
    def __init__(self, stdscr):
        self.stdscr = stdscr

        self.stdscr.clear()

        self.set_widths()

        self.initialize_reader()
        self.initialize_selection_windows()
        self.initialize_text_window()

        self.update_selections()
        self.update_text()

        self.start_input_loop()

    def initialize_reader(self):
        self.reader = Reader()
        self.reader.set_root('AMP')

    def initialize_selection_windows(self):

        self.translations_win = ListWindow(
                    self.stdscr.derwin(
                        curses.LINES,
                        TRANSLATIONS_WIDTH,
                        0,
                        0
                        ),
                    'TR',
                    make_enumeration(self.reader.get_translations()),
                    TRANSLATIONS_WIDTH
            )
    
        self.books_win = ListWindow(
                    self.stdscr.derwin(
                        curses.LINES,
                        BOOKS_WIDTH,
                        0,
                        TRANSLATIONS_WIDTH
                    ),
                    'BOOK',
                    make_enumeration(self.reader.get_books()),
                    BOOKS_WIDTH
                    )
        
        self.chapters_win = ListWindow(
                    self.stdscr.derwin(
                        curses.LINES,
                        CHAPTERS_WIDTH, 
                        0, 
                        TRANSLATIONS_WIDTH + BOOKS_WIDTH
                    ),
                    'CH',
                    make_enumeration(self.reader.get_chapters('Genesis')),
                    CHAPTERS_WIDTH
                    )

        self.verses_win = ListWindow(
                    self.stdscr.derwin(
                        curses.LINES,
                        VERSES_WIDTH,
                        0,
                        TRANSLATIONS_WIDTH + BOOKS_WIDTH
                        + CHAPTERS_WIDTH  #curses.COLS - VERSES_WIDTH,
                    ),
                    'VS',
                    make_enumeration(self.reader.get_verses('Genesis', 1)), # TODO
                    VERSES_WIDTH
            )

        self.windows_tuples = make_enumeration([
            self.translations_win,
            self.books_win,
            self.chapters_win,
            self.verses_win
            ])
        self.selected_window = self.windows_tuples[1]
        self.selected_window[1].set_active(True)

    def set_widths(self):
        self.text_start_x = TRANSLATIONS_WIDTH + BOOKS_WIDTH + CHAPTERS_WIDTH + VERSES_WIDTH # TODO smarter start vars
        self.text_width= curses.COLS - TRANSLATIONS_WIDTH - BOOKS_WIDTH - CHAPTERS_WIDTH - VERSES_WIDTH

    def initialize_text_window(self):
        # TODO make text box with outer border win class
        self.text_outer_win = self.stdscr.derwin(
                curses.LINES,
                self.text_width, 
                0,
                self.text_start_x
                )
        self.text_outer_win.box()

        self.text_win = self.text_outer_win.derwin(
            curses.LINES - 2,
            self.text_width - 2,
            1, 
            1,
            )

    
    def update_selections(self):
        trans = self.translations_win.get_selection_tuple()[1]
        self.reader.set_root(trans)

        book = self.books_win.get_selection_tuple()[1]
        
        chapter_tuples = make_enumeration(self.reader.get_chapters(book))

        self.chapters_win.set_selection_tuples(chapter_tuples)

        chapter = self.chapters_win.get_selection_tuple()[1]

        verses_tuples = make_enumeration(
                self.reader.get_verses(book, chapter)
                )

        self.verses_win.set_selection_tuples(verses_tuples)

    def update_text(self):
        
        trans_name = self.translations_win.get_selection_tuple()[1]
        book_name = self.books_win.get_selection_tuple()[1]
        chapter_name = self.chapters_win.get_selection_tuple()[1],
        verse = self.verses_win.get_selection_tuple()[1]

        text_title = " {0} {1}:{3} [{2}]".format(book_name, str(chapter_name[0]), trans_name, verse)
        text_title_centered = text_title.center(self.text_width, ' ')

        start_pad = len(text_title_centered) - len(text_title_centered.lstrip(' '))
        

        self.text_outer_win.clear()
        self.text_outer_win.box()
        self.text_outer_win.addstr(0, start_pad, text_title)
        self.text_outer_win.refresh()
       
        self.text_win.clear()
        
        raw_text = self.reader.get_chapter_text(
                self.books_win.get_selection_tuple()[1],
                self.chapters_win.get_selection_tuple()[1],
                verse_start = verse                )
        text = '\n'.join(
                wrap(
                    str(raw_text).decode('utf8'),
                    width=self.text_width - 3,
                    use_hyphenator=h_en
                )[0: curses.LINES - 2])
        self.text_win.addstr(text)
        self.text_win.refresh()

    def deactivate_all_windows(self):
        for (i, win) in self.windows_tuples:
            win.set_active(False)

    def start_input_loop(self):
        key = None
        while (key != ord('q')):
            
            key = self.stdscr.getch()
            
            if key == curses.KEY_UP:
                self.selected_window[1].increment_selection(-1)
            
            elif key == curses.KEY_DOWN:
                self.selected_window[1].increment_selection(1)
            
            elif key == curses.KEY_LEFT:
                self.deactivate_all_windows()
                
                new_windex = self.selected_window[0] - 1
                if new_windex < 0: new_windex = len(self.windows_tuples) - 1
                
                self.selected_window = self.windows_tuples[new_windex]
                self.selected_window[1].set_active(True)
            
            elif key == curses.KEY_RIGHT:
                self.deactivate_all_windows()
    
                new_windex = self.selected_window[0] + 1
                if new_windex >= len(self.windows_tuples): new_windex = 0
                
                self.selected_window = self.windows_tuples[new_windex]
                self.selected_window[1].set_active(True)
            
            self.update_selections()
            self.update_text()

wrapper(Main)            
