"""Testing app for entry classes."""

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
    assert entries[0].title == 'Title A'
    assert entries[0].comment == 'Comment A'
    assert entries[0].get_amount() == Decimal('1.0')
    assert entries[0].get_time() == time.to_timedelta(1.0)
    assert entries[0].get_price() == Decimal('50.00')

    # check values for MultiplyEntry
    assert entries[1].title == 'Title B'
    assert entries[1].comment == 'Comment B'
    assert entries[1].get_amount() == Decimal('2.0')
    assert entries[1].get_hour_rate() == time.to_timedelta(0.5)
    assert entries[1].get_time() == time.to_timedelta(1.0)
    assert entries[1].get_price(wage=wage) == Decimal('50.00')

    # check values for first ConnectEntry
    assert entries[2].title == 'Title C'
    assert entries[2].comment == 'Comment C'
    assert entries[2].get_amount() == Decimal('2.5')
    assert entries[2].get_is_time() == False
    assert entries[2].get_time(
        entry_list=entries
        ) == time.to_timedelta(0)
    assert entries[2].get_price(
        entry_list=entries,
        wage=wage
        ) == Decimal('125.00')

    # check values for second ConnectEntry
    assert entries[3].title == 'Title D'
    assert entries[3].comment == 'Comment D'
    assert entries[3].get_amount() == Decimal('3.0')
    assert entries[3].get_is_time() == True
    assert entries[3].get_time(
        entry_list=entries
        ) == time.to_timedelta('2:15:00')
    assert entries[3].get_price(
        entry_list=entries,
        wage=wage
        ) == Decimal('112.50')

def test_json_conversion_baseentry():
    """Test the json conversion."""
    # init the individual object
    a = BaseEntry(
        title='Total individual',
        comment='Individual comment!',
        amount=1.25,
        amount_format='{M}:{S} min',
        time='1:45',
        price=1000
    )

    # make new default object
    b = BaseEntry()

    # for now the values must not be the same
    assert b.get_id() != a.get_id()
    assert b.title != a.title
    assert b.comment != a.comment
    assert b.get_amount() != a.get_amount()
    assert b.amount_format != a.amount_format
    assert b.get_time() != a.get_time()
    assert b.get_price() != a.get_price()

    # load a into b with json as object with same attrbutes
    b = BaseEntry().from_json(js=a.to_json(), preset_loading=False)

    # now the values must be the same
    assert b.get_id() == a.get_id()
    assert b.title == a.title
    assert b.comment == a.comment
    assert b.get_amount() == a.get_amount()
    assert b.amount_format == a.amount_format
    assert b.get_time() == a.get_time()
    assert b.get_price() == a.get_price()

    # load a into b with json as preset
    b = BaseEntry().from_json(js=a.to_json(), preset_loading=True)

    # now the values must be the same
    assert b.get_id() != a.get_id()     # not same, since preset_loading
    assert b.title == a.title
    assert b.comment == a.comment
    assert b.get_amount() == a.get_amount()
    assert b.amount_format == a.amount_format
    assert b.get_time() == a.get_time()
    assert b.get_price() == a.get_price()

def test_json_conversion_multiplyentry():
    """Test the json conversion."""
    # init the individual object
    a = MultiplyEntry(
        title='Total individual',
        comment='Individual comment!',
        amount=1.25,
        amount_format='{M}:{S} min',
        hour_rate=0.75
    )

    # make new default object
    b = MultiplyEntry()

    # for now the values must not be the same
    assert b.get_id() != a.get_id()
    assert b.title != a.title
    assert b.comment != a.comment
    assert b.get_amount() != a.get_amount()
    assert b.amount_format != a.amount_format
    assert b.get_hour_rate() != a.get_hour_rate()

    # load a into b with json as object with same attrbutes
    b = MultiplyEntry().from_json(js=a.to_json(), preset_loading=False)

    # now the values must be the same
    assert b.get_id() == a.get_id()
    assert b.title == a.title
    assert b.comment == a.comment
    assert b.get_amount() == a.get_amount()
    assert b.amount_format == a.amount_format
    assert b.get_hour_rate() == a.get_hour_rate()

    # load a into b with json as a preset
    b = MultiplyEntry().from_json(js=a.to_json(), preset_loading=True)

    # now the values must be the same - preset alike
    assert b.get_id() != a.get_id()     # not same, since preset_loading
    assert b.title == a.title
    assert b.comment == a.comment
    assert b.get_amount() == a.get_amount()
    assert b.amount_format == a.amount_format
    assert b.get_hour_rate() == a.get_hour_rate()

def test_json_conversion_connectentry():
    """Test the json conversion."""
    # init the individual object
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
    assert c.get_id() in a.get_connected()

    # make new default object
    b = ConnectEntry()

    # for now the values must not be the same
    assert b.get_id() != a.get_id()
    assert b.title != a.title
    assert b.comment != a.comment
    assert b.get_amount() != a.get_amount()
    assert b.amount_format != a.amount_format
    assert b.get_is_time() != a.get_is_time()
    assert b.get_multiplicator() != a.get_multiplicator()
    assert b.get_connected() != a.get_connected()

    # load a into b with json as object with same attrbutes
    b = ConnectEntry().from_json(js=a.to_json(), preset_loading=False)

    # now the values must be the same
    assert b.get_id() == a.get_id()
    assert b.title == a.title
    assert b.comment == a.comment
    assert b.get_amount() == a.get_amount()
    assert b.amount_format == a.amount_format
    assert b.get_is_time() == a.get_is_time()
    assert b.get_multiplicator() == a.get_multiplicator()
    assert b.get_connected() == a.get_connected()

    # load a into b with json as a preset
    b = ConnectEntry().from_json(js=a.to_json(), preset_loading=True)

    # now the values must be the same - preset alike
    assert b.get_id() != a.get_id()     # except the id, since it's preset_loading
    assert b.title == a.title
    assert b.comment == a.comment
    assert b.get_amount() == a.get_amount()
    assert b.amount_format == a.amount_format
    assert b.get_is_time() == a.get_is_time()
    assert b.get_multiplicator() == a.get_multiplicator()
    assert b.get_connected() == set()   # except the set, since it's preset_loading