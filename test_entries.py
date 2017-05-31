"""Testing app for entry classes."""

from decimal import Decimal
from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry
from offer.offeramounttime import OfferAmountTime


def test_baseentry_set_price():
    """Set the price for BaseEntry."""
    a = BaseEntry(amount=1)
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
    assert entries[0].get_time() == OfferAmountTime(1.0)
    assert entries[0].get_price() == Decimal('50.00')

    # check values for MultiplyEntry
    assert entries[1].title == 'Title B'
    assert entries[1].comment == 'Comment B'
    assert entries[1].get_amount() == Decimal('2.0')
    assert entries[1].get_hour_rate() == OfferAmountTime(0.5)
    assert entries[1].get_time() == OfferAmountTime(1.0)
    assert entries[1].get_price(wage=wage) == Decimal('50.00')

    # check values for first ConnectEntry
    assert entries[2].title == 'Title C'
    assert entries[2].comment == 'Comment C'
    assert entries[2].get_amount() == Decimal('2.5')
    assert entries[2].get_is_time() is False
    assert entries[2].get_time(
        entry_list=entries
    ) == OfferAmountTime(0)
    assert entries[2].get_price(
        entry_list=entries,
        wage=wage
    ) == Decimal('125.00')

    # check values for second ConnectEntry
    assert entries[3].title == 'Title D'
    assert entries[3].comment == 'Comment D'
    assert entries[3].get_amount() == Decimal('3.0')
    assert entries[3].get_is_time() is True
    assert entries[3].get_time(
        entry_list=entries
    ) == OfferAmountTime('2:15:00')
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
        amount_format='{F}:{R} min',
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
    b = BaseEntry().from_json(js=a.to_json())

    # now the values must be the same
    assert b.get_id() == a.get_id()
    assert b.title == a.title
    assert b.comment == a.comment
    assert b.get_amount() == a.get_amount()
    assert b.amount_format == a.amount_format
    assert b.get_time() == a.get_time()
    assert b.get_price() == a.get_price()

    # load a into b with json as preset
    b = BaseEntry().from_json(js=a.to_json(), keep_id=False)

    # now the values must be the same
    assert b.get_id() != a.get_id()     # not same, since "preset loading"
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
        amount_format='{F}:{R} min',
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
    b = MultiplyEntry().from_json(js=a.to_json())

    # now the values must be the same
    assert b.get_id() == a.get_id()
    assert b.title == a.title
    assert b.comment == a.comment
    assert b.get_amount() == a.get_amount()
    assert b.amount_format == a.amount_format
    assert b.get_hour_rate() == a.get_hour_rate()

    # load a into b with json as a preset
    b = MultiplyEntry().from_json(js=a.to_json(), keep_id=False)

    # now the values must be the same - preset alike
    assert b.get_id() != a.get_id()     # not same, since "preset loading"
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
        amount_format='{F}:{R} min',
        is_time=True,
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

    # load a into b with json as object with same attributes
    b = ConnectEntry().from_json(js=a.to_json())

    # now the values must be the same
    assert b.get_id() == a.get_id()
    assert b.title == a.title
    assert b.comment == a.comment
    assert b.get_amount() == a.get_amount()
    assert b.amount_format == a.amount_format
    assert b.get_is_time() == a.get_is_time()
    assert b.get_multiplicator() == a.get_multiplicator()
    assert b.get_connected() == a.get_connected()

    # load a into b with json as a preset (don't keep the id)
    b = ConnectEntry().from_json(js=a.to_json(), keep_id=False)

    # now the values must be the same - preset alike
    assert b.get_id() != a.get_id()     # except the id, since it's "preset loading"
    assert b.title == a.title
    assert b.comment == a.comment
    assert b.get_amount() == a.get_amount()
    assert b.amount_format == a.amount_format
    assert b.get_is_time() == a.get_is_time()
    assert b.get_multiplicator() == a.get_multiplicator()
    assert b.get_connected() == a.get_connected()


def test_get_amount_str():
    """Test the get_amount_str method."""
    # init object
    a = BaseEntry(
        title='Total individual',
        comment='Individual comment!',
        amount=61.75,
        amount_format=''
    )

    # test differnet amount formats
    a.amount_format = '{F}:{R}'
    assert a.get_amount_str() == '61:45'

    a.amount_format = '{s}'
    assert a.get_amount_str() == '61.75'


def test_entry_tax_set():
    """Test the entry tax setter and getter."""
    taxi = BaseEntry()

    taxi.set_tax(1.54)
    assert taxi.get_tax() == Decimal('0.0154')
    assert taxi.get_tax_percent() == Decimal('1.54')

    taxi.set_tax('17.3')
    assert taxi.get_tax() == Decimal('0.173')
    assert taxi.get_tax_percent() == Decimal('17.3')

    taxi.set_tax(0.45)
    assert taxi.get_tax() == Decimal('0.45')
    assert taxi.get_tax_percent() == Decimal('45')


def test_entry_tax_price():
    """Test the price calculation with tax."""
    blubb = MultiplyEntry(
        amount=1.0,
        hour_rate=2.0
    )

    wage = Decimal('50')

    assert blubb.get_price(wage=wage) == Decimal('100')
    assert blubb.get_price_tax(wage=wage) == Decimal('0')

    # set tax to 19 %
    blubb.set_tax(19)

    assert blubb.get_price(wage=wage) == Decimal('100')
    assert blubb.get_price_tax(wage=wage) == Decimal('19')

    assert blubb.get_tax_percent() == Decimal('19')


def test_copy_entry():
    """Copy an entry."""
    ac = BaseEntry()
    bc = ac.copy()

    # by default copy does keep the ID
    assert ac.get_id() == bc.get_id()

    bc = ac.copy(keep_id=False)

    # now bc is a copy of ac, but with its own ID
    assert ac.get_id() != bc.get_id()


def test_unit_price():
    """Test unit price and unit price tax methods."""
    # BaseEntry
    a_unitp = BaseEntry(
        amount=2,
        price=100
    )

    assert a_unitp.get_price() == Decimal('200.00')
    assert a_unitp.get_unit_price() == Decimal('100.00')

    # MultiplyEntry
    b_unitp = MultiplyEntry(
        amount=2,
        hour_rate='0:30'
    )

    assert b_unitp.get_price(wage=Decimal('50.00')) == Decimal('50.00')
    assert b_unitp.get_unit_price(wage=Decimal('50.00')) == Decimal('25.00')

    # ConnectEntry
    c_unitp = ConnectEntry(
        amount=3,
        multiplicator=2
    )

    # list creation
    liste = []
    liste.append(b_unitp)
    liste.append(c_unitp)

    # linking
    liste[1].connect_entry(
        entry_list=liste,
        entry_id=liste[0].get_id()
    )

    assert c_unitp.get_price(
        entry_list=liste,
        wage=Decimal('50.00')
    ) == Decimal('300.00')

    assert c_unitp.get_unit_price(
        entry_list=liste,
        wage=Decimal('50.00')
    ) == Decimal('100.00')
