# coding=utf-8

"""The main programm is executed here."""

import curses
from offer import view
# from offer.entries import SimpleEntry


def main(screen):
    """Main process for the GUI handling."""
    # init the window
    w = view.OfferCurses()

    # main loop for the curses modul
    while 1:
        s = w.input(y=26, x=83, text='huh? ', length=2)
        if s == '':
            break


def run():
    """Execute the programm via curses.wrapper()."""
    curses.wrapper(main)
