"""The classes for entries."""

from decimal import Decimal
from offer import time
import uuid


class BaseEntry(object):
    """A very simple entry with basic options and FIXED values."""

    def __init__(
        self,
        title='Fixed entry',
        comment='',
        amount=0.0,
        time_input=0.0,
        price=0.00
    ):
        """Init the class."""
        self._title = title
        self._comment = comment
        self._amount = amount
        self._time = time.to_timedelta(time_input)
        self._price = round(Decimal(str(price)), 2)
        self._id = str(uuid.uuid1())

    @property
    def time(self):
        """Get time."""
        return self._time

    @time.setter
    def time(self, value):
        """Set time."""
        self._time = time.to_timedelta(value)

    def get_hours(self):
        """Get hours as decimal."""
        return time.get_decimal_hours_from_timedelta(self._time)

    @property
    def price(self):
        """Get price."""
        return self._price

    @price.setter
    def price(self, value):
        """Set price."""
        # try to set a new price
        try:
            # only works, if input is integer or float
            self._price = round(Decimal(str(value)), 2)
        except Exception:
            # otherwise don't do anything
            pass

    @property
    def id(self):
        """Get id."""
        return self._id

    @id.setter
    def id(self, value):
        """Do not set the id, if user tries to."""
        pass
