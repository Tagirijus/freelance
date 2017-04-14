# coding=utf-8

"""This script handles the GUI."""

import curses
import time


class OfferCurses(object):
    """Curses object with extra functions."""

    def __init__(self):
        """Init the stuff from curses."""
        self.w = curses.initscr()

    def write(self, text, y=1, x=1, sec=0.1):
        """Typewrite a text on the screen."""
        for char in xrange(0, len(text) + 1):
            self.w.addstr(y, x, text[0:char])
            self.w.refresh()
            time.sleep(sec)

    def output(self, text, y=1, x=1):
        """Write a text on the screen."""
        self.w.addstr(y, x, text)
        self.w.refresh()

    def input(self, y=1, x=1, text='> ', length=0):
        """Get user input."""
        self.w.addstr(y, x, text)
        self.w.clrtoeol()
        return self.w.getstr()
