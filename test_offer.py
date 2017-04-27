"""Testing app for offer class."""

from general import load_save
from offer.offer import Offer
from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry
from offer import time


class TestOffer(object):
    """Simple test offer."""

    # generate some example entries
    b = BaseEntry(
        title='Base title',
        comment='Base comment',
        amount=1,
        time=2.5,
        price=125
    )

    m = MultiplyEntry(
        title='Multiply title',
        comment='Multiply comment',
        amount=0.5,
        hour_rate=4
    )

    c = ConnectEntry(
        title='Connect title',
        comment='Connect comment',
        amount=3,
        is_time=True,
        multiplicator=2
    )

    # init the offer
    out = Offer(
        title='Testing offer',
        number='9'
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
    assert t == time.to_timedelta(0)

    # connect connected entry to base entry (3rd entry to 1st)
    myoffer.get_entry_list()[2].connect_entry(
        entry_list=myoffer.get_entry_list(),
        entry_id=myoffer.get_entry_list()[0].get_id()
    )

    # now time of third entry is 2 * 3 * 2.5 hours
    t = myoffer.get_entry_list()[2].get_time(myoffer.get_entry_list())
    multi = 2 * 3 * time.to_timedelta(2.5)
    assert t == multi


def test_offer_json_conversion():
    """Test the json conversion of the offer class."""
    # init offer object
    myoffer = TestOffer().out

    # connect connected entry to base entry (3rd entry to 1st)
    myoffer.get_entry_list()[2].connect_entry(
        entry_list=myoffer.get_entry_list(),
        entry_id=myoffer.get_entry_list()[0].get_id()
    )

    # generate it to another new object
    new_offer = load_save.load_offer_from_json(js=myoffer.to_json())

    # check if everything loaded up correctly
    assert myoffer.title == new_offer.title
    assert myoffer.number == new_offer.number

    # prices for connect entries must be the same
    assert(myoffer.get_entry_list()[2].get_price(myoffer.get_entry_list()) ==
           new_offer.get_entry_list()[2].get_price(new_offer.get_entry_list()))
