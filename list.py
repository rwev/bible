import curses

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


