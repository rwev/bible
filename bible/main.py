#!/usr/bin/env python3

import curses

from textwrap2 import wrap
from hyphen import Hyphenator

from .reader import Reader
from .textwin import TextWindow
from .listwin import ListWindow

TRANSLATIONS_WIDTH = 6
BOOKS_WIDTH = 14
CHAPTERS_WIDTH = 4
VERSES_WIDTH = 4

h_en = Hyphenator("en_US")


def make_enumeration(list_):
    return list(enumerate(list_))


class Main:
    def __init__(self, stdscr):
        self.stdscr = stdscr

        self.stdscr.clear()

        self.initialize_reader()
        self.initialize_windows()
        self.initialize_selections()

        self.update_selections()
        self.update_text()

        self.start_input_loop()

    def initialize_reader(self):
        self.reader = Reader()
        self.reader.set_root("AMP")

    def initialize_windows(self):

        start_x = 0
        self.translations_win = ListWindow(
            self.stdscr.derwin(curses.LINES, TRANSLATIONS_WIDTH, start_x, 0),
            "TR",
            make_enumeration(self.reader.get_translations()),
            TRANSLATIONS_WIDTH,
        )

        start_x += TRANSLATIONS_WIDTH
        self.books_win = ListWindow(
            self.stdscr.derwin(curses.LINES, BOOKS_WIDTH, 0, start_x),
            "BOOK",
            make_enumeration(self.reader.get_books()),
            BOOKS_WIDTH,
        )

        start_x += BOOKS_WIDTH
        self.chapters_win = ListWindow(
            self.stdscr.derwin(curses.LINES, CHAPTERS_WIDTH, 0, start_x),
            "CH",
            make_enumeration(self.reader.get_chapters("Genesis")),
            CHAPTERS_WIDTH,
        )

        start_x += CHAPTERS_WIDTH
        self.verses_win = ListWindow(
            self.stdscr.derwin(curses.LINES, VERSES_WIDTH, 0, start_x),
            "VS",
            make_enumeration(self.reader.get_verses("Genesis", 1)),
            VERSES_WIDTH,
        )

        start_x += VERSES_WIDTH
        self.text_width = curses.COLS - start_x
        self.text_win = TextWindow(
            self.stdscr.derwin(curses.LINES, self.text_width, 0, start_x),
            self.text_width,
        )

    def initialize_selections(self):
        self.windows_tuples = make_enumeration(
            [self.translations_win, self.books_win, self.chapters_win, self.verses_win]
        )
        self.selected_window = self.windows_tuples[1]
        self.selected_window[1].set_active(True)

    def update_selections(self):
        trans = self.translations_win.get_selection_tuple()[1]
        self.reader.set_root(trans)

        book = self.books_win.get_selection_tuple()[1]

        chapter_tuples = make_enumeration(self.reader.get_chapters(book))

        self.chapters_win.set_selection_tuples(chapter_tuples)

        chapter = self.chapters_win.get_selection_tuple()[1]

        verses_tuples = make_enumeration(self.reader.get_verses(book, chapter))

        self.verses_win.set_selection_tuples(verses_tuples)

    def update_text(self):
        trans_name = self.translations_win.get_selection_tuple()[1]
        book_name = self.books_win.get_selection_tuple()[1]
        chapter_name = (self.chapters_win.get_selection_tuple()[1],)
        verse = self.verses_win.get_selection_tuple()[1]

        text_title = " {0} {1}:{3} [{2}]".format(
            book_name, str(chapter_name[0]), trans_name, verse
        )

        raw_text = self.reader.get_chapter_text(
            self.books_win.get_selection_tuple()[1],
            self.chapters_win.get_selection_tuple()[1],
            verse_start=verse,
        )
        text = "\n".join(
            wrap(
                raw_text,
                width=self.text_width - 3,
                use_hyphenator=h_en,
            )[0 : curses.LINES - 2]
        )

        self.text_win.update_text_title(text_title)
        self.text_win.update_text(text)

    def deactivate_all_windows(self):
        for (i, win) in self.windows_tuples:
            win.set_active(False)

    def start_input_loop(self):
        key = None
        while key != ord("q"):

            key = self.stdscr.getch()

            if key == curses.KEY_UP:
                self.selected_window[1].increment_selection(-1)

            elif key == curses.KEY_DOWN:
                self.selected_window[1].increment_selection(1)

            elif key == curses.KEY_LEFT:
                self.deactivate_all_windows()

                new_windex = self.selected_window[0] - 1
                if new_windex < 0:
                    new_windex = len(self.windows_tuples) - 1

                self.selected_window = self.windows_tuples[new_windex]
                self.selected_window[1].set_active(True)

            elif key == curses.KEY_RIGHT:
                self.deactivate_all_windows()

                new_windex = self.selected_window[0] + 1
                if new_windex >= len(self.windows_tuples):
                    new_windex = 0

                self.selected_window = self.windows_tuples[new_windex]
                self.selected_window[1].set_active(True)

            if key == ord('k'):
                self.selected_window[1].increment_selection(-1)

            elif key == ord('j'):
                self.selected_window[1].increment_selection(1)

            elif key == ord('h'):
                self.deactivate_all_windows()

                new_windex = self.selected_window[0] - 1
                if new_windex < 0:
                    new_windex = len(self.windows_tuples) - 1

                self.selected_window = self.windows_tuples[new_windex]
                self.selected_window[1].set_active(True)

            elif key == ord('l'):
                self.deactivate_all_windows()

                new_windex = self.selected_window[0] + 1
                if new_windex >= len(self.windows_tuples):
                    new_windex = 0

                self.selected_window = self.windows_tuples[new_windex]
                self.selected_window[1].set_active(True)

            self.update_selections()
            self.update_text()


def main():
    curses.wrapper(Main)


if __name__ == "__main__":
    main()
