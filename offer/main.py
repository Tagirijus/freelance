"""The main programm is executed here."""

from offer.entries import BaseEntry
import os


BASE_PATH = os.path.dirname(os.path.realpath(__file__))[
    :os.path.dirname(os.path.realpath(__file__)).rfind('/')
]


def main():
    """Run the programm."""
    a = BaseEntry()
    print(a)
