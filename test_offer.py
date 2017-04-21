"""Testing app."""

from offer.entries import BaseEntry
from offer import time


def test_id_not_setable():
    """Test if id of BaseEntry is really not setable by the user."""
    a = BaseEntry()     # assign class
    tmp = a.id          # save its id
    a.id = 3            # try to assign new (should not work!!!)
    assert a.id == tmp  # test if id is the same as before


def set_price():
    """Set the price for BaseEntry."""
    a = BaseEntry()
    a.price = 3
    assert str(a.price) == '3.00'   # integer gets two decimal after comma
    a.price = 'pupsen'
    assert str(a.price) == '3.00'   # price is not changed due to wrong input type


def test_time():
    """Test calculation for the time module."""
    assert time.to_timedelta(1) == time.timedelta(seconds=1)
    assert time.to_timedelta(1.5) == time.timedelta(hours=1.5)
    assert time.to_timedelta('00:05') == time.timedelta(seconds=5)
    assert time.to_timedelta('01:07') == time.timedelta(minutes=1, seconds=7)
    assert time.to_timedelta('03:02:04') == time.timedelta(
        hours=3,
        minutes=2,
        seconds=4
    )
    assert time.to_timedelta('Hackbraten') == time.timedelta()
