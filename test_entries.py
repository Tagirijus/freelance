"""Testing app."""

from decimal import Decimal
from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry
from offer import time


def test_baseentry_set_price():
    """Set the price for BaseEntry."""
    a = BaseEntry()
    a.set_price(3)

    # integer gets two decimal after comma
    assert a.get_price() == Decimal('3.00')

    # price should not changed due to wrong input
    a.set_price('pupsen')
    assert a.get_price() == Decimal('3.00')


def test_integrety_entry():
    """Test if BaseEntry, ConnectEntry and MultiplyEntry work as they should."""
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
    assert entries[3].get_id() not in entries[2].get_connected()

    # connect MultiplyEntry to the second ConnectEntry
    entries[3].connect_entry(
        entry_list=entries,
        entry_id=entries[1].get_id()
    )

    # set wage to work with
    wage = Decimal('50.00')

    # check values for BaseEntry
    assert entries[0].get_title() == 'Title A'
    assert entries[0].get_comment() == 'Comment A'
    assert entries[0].get_amount() == Decimal('1.0')
    assert entries[0].get_time() == time.to_timedelta(1.0)
    assert entries[0].get_price() == Decimal('50.00')

    # check values for MultiplyEntry
    assert entries[1].get_title() == 'Title B'
    assert entries[1].get_comment() == 'Comment B'
    assert entries[1].get_amount() == Decimal('2.0')
    assert entries[1].get_hour_rate() == time.to_timedelta(0.5)
    assert entries[1].get_time() == time.to_timedelta(1.0)
    assert entries[1].get_price(wage=wage) == Decimal('50.00')

    # check values for first ConnectEntry
    assert entries[2].get_title() == 'Title C'
    assert entries[2].get_comment() == 'Comment C'
    assert entries[2].get_amount() == Decimal('2.5')
    assert entries[2].is_time() == False
    assert entries[2].get_time(
        entry_list=entries
        ) == time.to_timedelta(0)
    assert entries[2].get_price(
        entry_list=entries,
        wage=wage
        ) == Decimal('125.00')

    # check values for second ConnectEntry
    assert entries[3].get_title() == 'Title D'
    assert entries[3].get_comment() == 'Comment D'
    assert entries[3].get_amount() == Decimal('3.0')
    assert entries[3].is_time() == True
    assert entries[3].get_time(
        entry_list=entries
        ) == time.to_timedelta('2:15:00')
    assert entries[3].get_price(
        entry_list=entries,
        wage=wage
        ) == Decimal('112.50')
