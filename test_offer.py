"""Testing app for offer class."""

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
        title='Testing offer'
    )

    # add entries to its list
    out.append(b)
    out.append(m)
    out.append(c)

    assert len(out.entry_list) == 3


def test_offer_data_structure():
    """Test the data structure for offer and appended entries."""
    myoffer = TestOffer().out

    # first check for title of second entry
    assert myoffer.entry_list[1].title == 'Multiply title'

    # check time of third entry
    t = myoffer.entry_list[2].get_time(myoffer.entry_list)
    assert t == time.to_timedelta(0)

    # connect connected entry to base entry (3rd entry to 1st)
    myoffer.entry_list[2].connect_entry(
        entry_list=myoffer.entry_list,
        entry_id=myoffer.entry_list[0].get_id()
    )

    # now time of third entry is 2 * 3 * 2.5 hours
    t = myoffer.entry_list[2].get_time(myoffer.entry_list)
    multi = 2 * 3 * time.to_timedelta(2.5)
    assert t == multi
