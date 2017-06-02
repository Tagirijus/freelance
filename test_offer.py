"""Testing app for offer class."""

from clients.project import Project
from datetime import date
from decimal import Decimal
from offer.offerinvoice import Offer
from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry
from offer.quantitytime import QuantityTime


class TestOffer(object):
    """Simple test offer."""

    # generate some example entries
    b = BaseEntry(
        title='Base title',
        comment='Base comment',
        quantity=1,
        time=2.5,
        price=125
    )

    m = MultiplyEntry(
        title='Multiply title',
        comment='Multiply comment',
        quantity=0.5,
        hour_rate=4
    )

    c = ConnectEntry(
        title='Connect title',
        comment='Connect comment',
        quantity=3,
        is_time=True,
        multiplicator=2
    )

    # init the offer
    out = Offer(
        title='Testing offer'
    )

    # add entries to its list
    out.append(b)
    out.append(m)
    out.append(c)

    assert len(out.get_entry_list()) == 3


def test_offer_data_structure():
    """Test the data structure for offer and appended entries."""
    myoffer = TestOffer().out

    # first check for title of second entry
    assert myoffer.get_entry_list()[1].title == 'Multiply title'

    # check time of third entry
    t = myoffer.get_entry_list()[2].get_time(myoffer.get_entry_list())
    assert t == QuantityTime(0)

    # connect connected entry to base entry (3rd entry to 1st)
    myoffer.get_entry_list()[2].connect_entry(
        entry_list=myoffer.get_entry_list(),
        entry_id=myoffer.get_entry_list()[0].get_id()
    )

    # now time of third entry is 2 * 3 * 2.5 hours
    t = myoffer.get_entry_list()[2].get_time(myoffer.get_entry_list())
    multi = 2 * 3 * QuantityTime(2.5)
    assert t == multi


def test_offer_date():
    """Set offer date."""
    da = Offer(date=date(1987, 10, 15))
    assert da.get_date() == date(1987, 10, 15)

    da.set_date('1992-08-02')
    assert da.get_date() == date(1992, 8, 2)


def test_offer_copy():
    """Convert offer and convert it back."""
    a = Offer(
        title='Testuel',
        date_fmt='%d.%m.%Y',
        date='2017-01-01',
        wage=Decimal('50.0'),
        round_price=True
    )
    b = a.copy()

    # both have the same
    assert a.title == b.title
    assert a.date_fmt == b.date_fmt
    assert a.get_date() == b.get_date()
    assert a.get_wage() == b.get_wage()

    a.title = 'other'
    a.date_fmt = '%d. in %m, %Y'
    a.set_date(date.today())
    a.set_wage('40.0')

    # both now don't have the same
    assert a.title != b.title
    assert a.date_fmt != b.date_fmt
    assert a.get_date() != b.get_date()
    assert a.get_wage() != b.get_wage()


def test_price_total():
    """Test the total methods."""
    off = Offer()

    off.append(
        BaseEntry(
            quantity=1.0,
            price=100.0,
            tax=19
        )
    )

    off.append(
        BaseEntry(
            quantity=1.0,
            price=10.0,
            tax=7
        )
    )

    off.append(
        ConnectEntry(
            quantity=1.0,
            tax=19,
            multiplicator=1
        )
    )

    off.get_entry_list()[2].connect_entry(
        entry_list=off.get_entry_list(),
        entry_id=off.get_entry_list()[1].get_id()
    )

    wage = Decimal('50.00')

    assert off.get_price_total(wage=wage) == Decimal('120')
    assert off.get_price_tax_total(wage=wage) == Decimal('21.6')


def test_offer_wage_zero():
    """
    Normally you can get project as argument to get its wage, if own is 0.

    The fallback however should return 0 as wage, when offer wage is zero.
    """
    # test offer wage getter on its own
    offer_wage_test = Offer(wage=0)

    assert offer_wage_test.get_wage() == Decimal(0)

    # now test it with a project linked to it
    proj = Project(wage=10)
    assert offer_wage_test.get_wage(project=proj) == Decimal(10)
