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
        w.output_table_line([1, 2, 3], col_widths=[10, 70, 30])
        s = w.input(y=10, x=10)
        if s == '':
            break


def run():
    """Execute the programm via curses.wrapper()."""
    curses.wrapper(main)
