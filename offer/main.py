"""
A tool for generating an offer.

This tool calculates prices according to hour times wage. It can be handy
for self-employed people, who has to send offers to clients. It is also
handy for just calculating the estimated time for a specific task.
"""

from npy_gui import npy_gui


def main():
    """Run the programm with the npyscreen GUI."""
    App = npy_gui.FreelanceApplication()
    App.run()
