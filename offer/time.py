"""
Time calculation module.

Neede, since timdelta has no strftime() function, neither has the time module
from datetime. So I wrote my own 'little parser'.
"""

from datetime import timedelta
from decimal import Decimal


def to_timedelta(i=None):
    """Convert string into timedelta object."""
    # input is an integer or float and stands for hours
    if type(i) == int or type(i) == float:
        return timedelta(hours=i)

    # input is a string and has to be parsed
    # or it is convertable as float and stands for hours
    elif type(i) == str:
        try:
            # it's convertable to float
            return timedelta(hours=float(i))
        except Exception:
            # it has to be parsed
            # split by ':'
            nums = []
            for num in i.split(':'):
                try:
                    # convert to int and append
                    nums.append(int(num))
                except Exception:
                    # error, return empty timedelta
                    return timedelta()

            # check how many numbers there are and convert them to timedelta
            # e.g.: 1 number stands for seconds, 2 numbers stand for min + sec
            #       3 numbers stand for hour + min + sec
            if len(nums) == 1:
                h = 0
                m = 0
                s = nums[0]
            elif len(nums) == 2:
                h = 0
                m = nums[0]
                s = nums[1]
            elif len(nums) >= 3:
                h = nums[0]
                m = nums[1]
                s = nums[2]
            return timedelta(hours=h, minutes=m, seconds=s)

    # input is something else, return empty timedelta
    else:
        return timedelta()


def get_decimal_hours_from_timedelta(timed):
    """Get decimal hours from timedelta."""
    seconds = Decimal(str(timed.seconds))
    return seconds / Decimal('3600')
