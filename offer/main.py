"""The main programm is executed here."""

from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry
from offer.entries import move_entry
import os
from decimal import Decimal


BASE_PATH = os.path.dirname(os.path.realpath(__file__))[
    :os.path.dirname(os.path.realpath(__file__)).rfind('/')
]


def main():
    """Run the programm."""
    a = ConnectEntry(
        title='Total individual',
        comment='Individual comment!',
        amount=1.23,
        amount_format='{M}:{S} min',
        is_time=False,
        multiplicator=9.99
    )
    c = BaseEntry()
    a.connect_entry([a, c], c.get_id())

    # make new default object
    b = ConnectEntry()

    print(a.to_json())
    b = b.from_json(a.to_json())
    print(b.to_json())
