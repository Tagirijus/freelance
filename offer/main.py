"""The main programm is executed here."""

from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry
from offer.entries import move_entry
import os


BASE_PATH = os.path.dirname(os.path.realpath(__file__))[
    :os.path.dirname(os.path.realpath(__file__)).rfind('/')
]


def main():
    """Run the programm."""
    pass
