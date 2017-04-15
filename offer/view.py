# coding=utf-8

"""This script handles the GUI."""

import curses
import time


class OfferCurses(object):
    """Curses object with extra functions."""

    def __init__(self):
        """Init the stuff from curses."""
        self.w = curses.initscr()

    def cap_text(self, text='', y=1, x=1, shortener='>', additional_x=0, input=False):
        """Cap text, which could be too long for the display."""
        # get maximums
        max_y = self.w.getmaxyx()[0]
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

    def write(self, text, y=1, x=1, sec=0.1):
        """Typewrite a text on the screen."""
        dat = self.cap_text(text, y, x)
        if dat:
            # write it
            for char in xrange(0, len(dat) + 1):
                self.w.addstr(y, x, dat[0:char])
                self.w.refresh()
                time.sleep(sec)
        else:
            # cancel
            return

    def output(self, text, y=1, x=1):
        """Write a text on the screen."""
        dat = self.cap_text(text, y, x)
        if dat:
            # output it
            self.w.addstr(y, x, dat)
            self.w.refresh()
        else:
            # cancel
            return

    def input(self, y=1, x=1, text='', length=3, clear=False):
        """Get user input string."""
        check = self.cap_text(y=y, x=x, additional_x=length, input=True)
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
