# coding=utf-8

"""This script handles the GUI."""

import curses
import time


class OfferCurses(object):
    """Curses object with extra functions."""

    def __init__(self):
        """Init the stuff from curses."""
        self.w = curses.initscr()

    def cap_text(
        self,
        text='',
        y=0,
        x=0,
        max_y=None,
        max_x=None,
        shortener='>',
        additional_x=0,
        input=False
    ):
        """Cap text, which could be too long for the display."""
        # max_y == terminal height if not set
        if max_y is None:
            max_y = self.w.getmaxyx()[0]

        # max_x == terminal width if not set
        if max_x is None:
            max_x = self.w.getmaxyx()[1]

        # check maximum line / y. when over: return without doing anything
        if y >= max_y:
            return False

        # also cancel, if x >= max_x - 2 {or even - (3 + additional) if input}
        if x >= max_x - 2 - (1 + additional_x if input else 0):
            return False

        # check continues for output functions only
        if not input:
            # check maximum width / x + len(text)
            if x + len(text) + additional_x >= max_x:
                # it's too long, shorten it and check if this works
                # calculate new lenght
                new_len = max_x - x - additional_x - 2
                # get new text
                text = text[:new_len] + shortener

            # return new text
            return text
        else:
            return True

    def write(self, text, y=0, x=0, max_y=None, max_x=None, sec=0.1):
        """Typewrite a text on the screen."""
        # max_y == terminal height if not set
        if max_y is None:
            max_y = self.w.getmaxyx()[0]

        # max_x == terminal width if not set
        if max_x is None:
            max_x = self.w.getmaxyx()[1]

        dat = self.cap_text(text, y, x, max_y, max_x)
        if dat:
            # write it
            for char in xrange(0, len(dat) + 1):
                self.w.addstr(y, x, dat[0:char])
                self.w.refresh()
                time.sleep(sec)
        else:
            # cancel
            return

    def output(self, text, y=1, x=1, max_y=None, max_x=None):
        """Write a text on the screen."""
        # max_y == terminal height if not set
        if max_y is None:
            max_y = self.w.getmaxyx()[0]

        # max_x == terminal width if not set
        if max_x is None:
            max_x = self.w.getmaxyx()[1]

        dat = self.cap_text(text, y, x)
        if dat:
            # output it
            self.w.addstr(y, x, dat)
            self.w.refresh()
        else:
            # cancel
            return

    def input(self, text='', y=0, x=0, max_y=None, max_x=None, length=3, clear=False):
        """Get user input string."""
        # max_y == terminal height if not set
        if max_y is None:
            max_y = self.w.getmaxyx()[0]

        # max_x == terminal width if not set
        if max_x is None:
            max_x = self.w.getmaxyx()[1]

        check = self.cap_text(y=y, x=x, max_y=max_y, max_x=max_x, additional_x=length, input=True)
        if check:
            # output text before input, if it fits
            dat = self.cap_text(text, y, x, additional_x=length)
            if dat:
                # output it
                self.output(dat, y, x)
                new_x = x + len(dat)
            else:
                new_x = x + len(text)

            # get user input
            curses.echo()
            if clear:
                self.w.clrtoeol()
            return self.w.getstr(y, new_x)
        else:
            # cancel, since too long
            return ''

    def get_key(self):
        """Get a single key stroke."""
        curses.noecho()
        return self.w.getch()

    def output_table_line(self, table, y=0, x=0, height=None, width=None, space=1, col_widths=None):
        """Output a table nearly like tabulate, but curses compliant."""
        # cancel if table is empty or table is not a list
        if len(table) < 1 or type(table) != list:
            return

        # get height if height==None
        if height is None:
            height = self.w.getmaxyx()[0] - y

        # get width if width==None
        if width is None:
            width = self.w.getmaxyx()[1] - x

        """
        Auto calculate the col_widths list here.

        The col_widths list holds percantages for the column widths. E.g.
        if the table list has three items and you want them to spread like
        first column = 10 %, second = 70 % and third = 20 %, you will write
        col_widths = [10, 70, 20]. The script then calculates according to
        the width of the table, which column will get how much characters.
        E.g. if the table widths is 100 characters and the space between
        every column is 1 (space == 1), the script would then modify the
        col_widths to col_widths = [10, 68, 19]. Explained:
        width == 100 - space (3 * 1) == 97. 10% from 97 rounded == 10,
        70 % from 97 rounded == 68 and the remaining space is
        97 - 10 - 68 == 19.

        If col_widths is not set (thus col_widths is None), the script
        will calculate an even spread width for the columns, while the
        last column is the remaining width, for rounding issues. E.g. if
        table holds three items, the width == 100 and the space == 1,
        it should calculate something like: col_widths = [32, 32, 33].
        """
        # automatic col_widths calculation
        # count columns according to table list
        cols = len(table)
        if col_widths is None:
            # calculate width of one col so that it still fits in the width
            one_col_width = int((width - (space * cols - 1)) / cols)

            # add this to the col_widths list
            col_widths = []
            space_used = 0
            for entry in table:
                # check if the is space left, or if left space is < one_col_width
                if (width - space_used) < one_col_width:
                    # add the remaining space
                    col_widths.append(width - space_used)
                else:
                    # add one_col_width
                    col_widths.append(one_col_width)
                    space_used += one_col_width

        # manual col_widths calculation
        else:
            # first check if the values add up to 100 and get it correct
            summing = 0
            for which, col_widths_entry in enumerate(col_widths):
                try:
                    # check if it's the last one
                    if which == len(col_widths) - 1:
                        # caculate the last value automatic
                        # (to avoid wrong input)
                        col_widths[which] = 100 - summing
                    else:
                        # just add the other to the summing
                        summing += col_widths_entry
                except Exception:
                    # entry is maybe no integer ... just add 5% and "correct" the entry
                    summing += 5
                    col_widths[which] = 5

            # calculate every row correct
            left_space = int(width - (space * cols - 1))
            all_space = left_space
            for which, col_widths_entry in enumerate(col_widths):
                # check if it's the last one
                if which == len(col_widths) - 1:
                    # get the remaining space to the end
                    col_widths[which] = left_space
                else:
                    # get the amount of chars according to the percentage
                    chars = int((col_widths[which] / 100.0) * all_space)
                    col_widths[which] = chars
                    left_space -= chars

        # WEITER HIER:
        # jetzt wird die zeile geschrieben!

        # DEBUG OUTPUT
        self.w.addstr(1, 0, ', '.join([str(text) for text in col_widths]))
