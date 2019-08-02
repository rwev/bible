import curses


class TextWindow:
    def __init__(self, win, width):
        self._outer_win = win
        self._outer_win.box()

        self._width = width

        self._inner_win = self._outer_win.derwin(
            curses.LINES - 2, self._width - 2, 1, 1
        )

    def update_text_title(self, title):
        self._outer_win.clear()
        self._outer_win.box()

        title_centered = title.center(self._width, " ")
        start_pad = len(title_centered) - len(title_centered.lstrip(" "))

        self._outer_win.addstr(0, start_pad, title)
        self._outer_win.refresh()

    def update_text(self, text):
        self._inner_win.clear()
        self._inner_win.addstr(text)
        self._inner_win.refresh()
