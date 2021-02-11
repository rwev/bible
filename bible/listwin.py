import curses


class ListWindow:
    def __init__(self, win, title, item_tuples, width):

        self.MAX_ITEMS = curses.LINES - 2

        self._win = win
        self._width = width
        self._title = title
        self._active = False
        self._item_tuples = item_tuples
        self.select_first()

    def set_active(self, is_active):
        self._active = is_active
        self.draw()

    def get_selection_tuple(self):
        return self._selected_tuple

    def set_selection_tuples(self, item_tuples):
        self._item_tuples = item_tuples
        if self._selected_tuple not in item_tuples:
            self.select_first()
        else:
            self.draw()

    def increment_selection(self, i):
        new_index = self._selected_tuple[0] + i
        if new_index < 0 or new_index >= len(self._item_tuples):
            return

        self._selected_tuple = self._item_tuples[new_index]

        (bound_lower, bound_upper) = self._bounds

        shift_up = bound_upper <= new_index < len(self._item_tuples)
        shift_down = 0 <= new_index < bound_lower
        shift = shift_down or shift_up

        if shift:
            self._bounds = (bound_lower + i, bound_upper + i)

        self.draw()

    def select_first(self):
        self._selected_tuple = self._item_tuples[0]
        self._bounds = (0, self.MAX_ITEMS)
        self.draw()

    def write_title(self):
        self._win.addnstr(
            0, 0, self._title.center(self._width, " "), self._width, curses.A_UNDERLINE
        )

    def draw(self):
        self._win.clear()
        self.write_title()

        for (i, val) in self._item_tuples[self._bounds[0]: self._bounds[1]]:

            y = 1 + i - self._bounds[0]
            str_len = self._width - 2
            string = str(val).ljust(str_len)

            if i == self._selected_tuple[0]:
                self._win.addnstr(
                    y,
                    0,
                    ">{0}".format(string),
                    str_len + 1,
                    curses.A_STANDOUT if self._active else curses.A_BOLD,
                )
            else:
                self._win.addnstr(y, 1, string, str_len)

        self._win.refresh()
