"""
A simple tool for generating an offer.

This tool calculates prices according to hour times wage. It can be handy
for self-employed people, who has to send offers to clients. It is also
handy for just calculating the estimated time for a specific task.
"""

from offer import main

if __name__ == '__main__':
    App = main.OfferApp()
    App.run()
