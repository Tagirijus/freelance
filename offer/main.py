"""The main programm is executed here."""

from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry
from decimal import Decimal
import os


BASE_PATH = os.path.dirname(os.path.realpath(__file__))[
    :os.path.dirname(os.path.realpath(__file__)).rfind('/')
]


def main():
    """Run the programm."""
    a = BaseEntry(
        title='Title A',
        comment='Comment A',
        amount=1.0,
        time=1.0,
        price=50.00
    )

    b = MultiplyEntry(
        title='Title B',
        comment='Comment B',
        amount=2.0,
        amount_format='{M}:{S} min',
        hour_rate=0.5
    )

    c = ConnectEntry(
        title='Title C',
        comment='Comment C',
        amount=2.5,
        is_time=False,
        multiplicator=0.5
    )

    d = ConnectEntry(
        title='Title D',
        comment='Comment D',
        amount=3.0,
        amount_format='{S} %',
        is_time=True,
        multiplicator=0.75
    )

    # init entries in list
    entries = []
    entries.append(a)
    entries.append(b)
    entries.append(c)
    entries.append(d)

    # connect first two entries two the first ConnectEntry
    entries[2].connect_entry(
        entry_list=entries,
        entry_id=entries[0].get_id()
    )
    entries[2].connect_entry(
        entry_list=entries,
        entry_id=entries[1].get_id()
    )

    # connect first ConnectEntry to the second ConnectEntry
    entries[3].connect_entry(
        entry_list=entries,
        entry_id=entries[2].get_id()
    )

    # connect second ConnectEntry to the first ConnectEntry
    # and it should not work anymore
    entries[2].connect_entry(
        entry_list=entries,
        entry_id=entries[3].get_id()
    )

    # connect MultiplyEntry to the second ConnectEntry
    entries[3].connect_entry(
        entry_list=entries,
        entry_id=entries[1].get_id()
    )

    # set wage to work with
    wage = Decimal('50.00')

    for e in entries:
        out = []
        out.append(str(e.get_title()))
        out.append(str(e.get_comment()))
        out.append(str(e.get_amount_str()))
        out.append(str(e.get_time(entry_list=entries)))
        out.append(str(e.get_price(wage=wage, entry_list=entries)))

        print(', '.join(out))
