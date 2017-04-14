# coding=utf-8

"""The main programm is executed here."""

import curses
from offer import view
# from offer.entries import SimpleEntry


def main(screen):
    """Main process for the GUI handling."""
    # init the window
    w = view.OfferCurses()
    curses.echo()

    # main loop for the curses modul
    while 1:
        s = w.input(y=3, text='')
        if s == "q":
            break
        w.w.insertln()

        w.output(s)


def run():
    """Execute the programm via curses.wrapper()."""
    curses.wrapper(main)
