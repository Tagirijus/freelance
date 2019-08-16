"""Testing app for project class."""

from clients.project import Project
from decimal import Decimal
from offer.offerinvoice import Offer
from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry


class TestOfferA(object):
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
        title='Testing offer A'
    )

    # add entries to its list
    out.append(b)
    out.append(m)
    out.append(c)

    assert len(out.get_entry_list()) == 3


class TestOfferB(object):
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

    c = MultiplyEntry(
        title='Multiply title 2',
        comment='Multiply comment 2',
        quantity=4,
        hour_rate=3.15
    )

    d = ConnectEntry(
        title='Connect title 2',
        comment='Connect comment 2',
        quantity=9,
        is_time=False,
        multiplicator=0.25
    )

    # init the offer
    out = Offer(
        title='Testing offer B'
    )

    # add entries to its list
    out.append(b)
    out.append(m)
    out.append(c)
    out.append(d)

    # connect 2nd entry to 4th entry
    out.get_entry_list()[3].connect_entry(
        entry_list=out.get_entry_list(),
        entry_id=out.get_entry_list()[1].get_id()
    )

    # 4th entry get_price() should now return 0.5 * 4 * 9 * 0.25 * 50.00 = 225.00
    wage = Decimal('50.00')
    p = round(Decimal(0.5 * 4 * 9 * 0.25) * wage, 2)
    assert out.get_entry_list()[3].get_price(
        entry_list=out.get_entry_list(),
        wage=wage
    ) == p

    assert len(out.get_entry_list()) == 4


def test_offer_data_structure():
    """Test the data structure for project and appended offers."""
    # init test offers
    myoffer_a = TestOfferA().out
    myoffer_b = TestOfferB().out

    # init test project
    myproject = Project(
        client_id='clcl01',
        title='Test Project',
        hours_per_day=6,
        work_days=[0, 1, 2, 3, 4],
        minimum_days=2
    )

    # append test offers to the test project
    myproject.append_offer(myoffer_a)
    myproject.append_offer(myoffer_b)

    # 1st offer, 2nd entry title should be 'Multiply title'
    assert myproject.get_offer_list()[0].get_entry_list()[1].title == (
        'Multiply title'
    )

    # 2nd offer, 3rd entry price should be Decimal(630.00)
    wage = Decimal('50.00')
    assert myproject.get_offer_list()[1].get_entry_list()[2].get_price(
        wage=wage) == Decimal('630.00')


def test_project_copy():
    """Copy a project."""
    a = Project(
        title='Project A'
    )

    a.append_offer(Offer(
        title='Offer A'
    ))

    b = a.copy()

    # both should have the same title
    assert a.title == b.title

    # both also should have one offer with the same title
    assert a.get_offer_list()[0].title == b.get_offer_list()[0].title
