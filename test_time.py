"""Testing app for own time module."""

from offer import time


def test_time():
    """Test calculation for the time module."""
    assert time.to_timedelta(1) == time.timedelta(hours=1)
    assert time.to_timedelta(1.5) == time.timedelta(hours=1.5)
    assert time.to_timedelta('00:05') == time.timedelta(seconds=5)
    assert time.to_timedelta('01:07') == time.timedelta(minutes=1, seconds=7)
    assert time.to_timedelta('03:02:04') == time.timedelta(
        hours=3,
        minutes=2,
        seconds=4
    )
    assert time.to_timedelta('Hackbraten') == time.timedelta()
    assert time.to_timedelta('1.3') == time.timedelta(hours=1.3)
    assert time.to_timedelta('3') == time.timedelta(hours=3)
