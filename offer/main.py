"""The main programm is executed here."""

from offer.entries import BaseEntry
from offer.entries import ConnectEntry
from offer.entries import MultiplyEntry
from decimal import Decimal
import os


BASE_PATH = os.path.dirname(os.path.realpath(__file__))[
    :os.path.dirname(os.path.realpath(__file__)).rfind('/')
]


def main():
    """Run the programm."""
    a = BaseEntry(
        title='Base Eintrag A',
        comment='Kommentar Eintrag A',
        amount=1.0,
        time=1.0,
        price=50.00
    )

    b = ConnectEntry(
        title='Connect Eintrag B',
        comment='Kommentar Eintrag B',
        amount=2.5,
        is_time=False,
        multiplicator=0.5
    )

    c = ConnectEntry(
        title='Connect Eintrag C',
        comment='Kommentar Eintrag C',
        amount=1.0,
        is_time=False,
        multiplicator=2.0
    )

    d = MultiplyEntry(
        title='Multiply Eintrag D',
        comment='Kommentar Eintrag D',
        amount=2.0,
        hour_rate=0.5
    )

    entries = []
    entries.append(a)
    entries.append(b)
    entries.append(c)
    entries.append(d)
    entries[1].connect_entry(entries, entries[0].get_id())
    entries[2].connect_entry(entries, entries[0].get_id())
    entries[2].connect_entry(entries, entries[1].get_id())
    wage = Decimal('50.00')

    for e in entries:
        out = []
        out.append(str(e.get_title()))
        out.append(str(e.get_comment()))
        out.append(str(e.get_amount()))
        out.append(str(e.get_time(entry_list=entries)))
        out.append(str(e.get_price(wage=wage, entry_list=entries)))

        print(', '.join(out))
