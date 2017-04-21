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
        self._title = str(title)
        self._comment = str(comment)
        self._amount = Decimal('0.0')               # set default
        self.set_amount(amount)                     # try to set arguments value
        self._time = time.to_timedelta(time_input)
        self._price = Decimal('0.00')               # set default
        self.set_price(price)                       # try to set arguments value
        self._id = str(uuid.uuid1())

    def get_comment(self):
        """Get comment."""
        return self._comment

    def set_comment(self, value):
        """Set comment."""
        try:
            # has to be convertable to string
            self._comment = str(value)
        except Exception:
            # otherwise pass
            pass

    def get_title(self):
        """Get title."""
        return self._title

    def set_title(self, value):
        """Set title."""
        try:
            # has to be convertable to string
            self._title = str(value)
        except Exception:
            # otherwise pass
            pass

    def get_amount(self):
        """Get amount."""
        return self._amount

    def set_amount(self, value):
        """Set amount."""
        # try to set a new amount
        try:
            # only works, if input is integer, float or string
            self._amount = Decimal(str(value))
        except Exception:
            # otherwise don't do anything
            pass

    def get_time(self):
        """Get time."""
        return self._time

    def set_time(self, value):
        """Set time."""
        self._time = time.to_timedelta(value)

    def get_hours(self):
        """Get hours as decimal."""
        return time.get_decimal_hours_from_timedelta(self._time)

    def get_price(self):
        """Get price."""
        return self._price

    def set_price(self, value):
        """Set price."""
        # try to set a new price
        try:
            # only works, if input is integer, float or string
            self._price = round(Decimal(str(value)), 2)
        except Exception:
            # otherwise don't do anything
            pass

    def get_id(self):
        """Get id."""
        return self._id


class ModEntry(BaseEntry):
    """Entry for modulating respecting other entries."""

    def __init__(
        self,
        title='Mod entry',
        is_time=True,
        multiplicator=1.0
    ):
        """Initialize the class."""
        super(ModEntry, self).__init__()
        self._title = str(title)
        self._connected = []
        self._is_time = bool(is_time)
        self._multiplicator = Decimal('1.0')  # set default
        self.set_multiplicator(multiplicator)  # try to set arguments value

    def get_multiplicator(self):
        """Get multiplicator."""
        return self._multiplicator

    def set_multiplicator(self, value):
        """Set multiplicator."""
        # try to set a new multiplicator
        try:
            # only works, if input is integer, float or string
            self._multiplicator = Decimal(str(value))
        except Exception:
            # otherwise don't do anything
            pass

    def is_time(self, set_it=None):
        """Get or set is_time value."""
        if set_it == None:
            # set_it not set, so show me the value
            return self._is_time
        else:
            # parameter given, set the value
            self._is_time = bool(set_it)
            # and return it afterwards
            return self._is_time

    def get_connected(self):
        """Get connected list."""
        return self._connected

    def connect_entry(self, entry_id):
        """Append to the self._connected list."""
        self._connected.append(str(entry_id))

    def disconnect_entry(self, entry_id):
        """Delete the entry_id from the self._connected list."""
        if str(entry_id) in self._connected:
            self._connected.pop(self._connected.index(str(entry_id)))
