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
        self._amount = Decimal(str(amount))
        self._time = time.to_timedelta(time_input)
        self._price = round(Decimal(str(price)), 2)
        self._id = str(uuid.uuid1())

    @property
    def comment(self):
        """Get comment."""
        return self._comment

    @comment.setter
    def comment(self, value):
        """Set comment."""
        try:
            # has to be convertable to string
            self._comment = str(value)
        except Exception:
            # otherwise pass
            pass

    @property
    def title(self):
        """Get title."""
        return self._title

    @title.setter
    def title(self, value):
        """Set title."""
        try:
            # has to be convertable to string
            self._title = str(value)
        except Exception:
            # otherwise pass
            pass

    @property
    def amount(self):
        """Get amount."""
        return self._amount

    @amount.setter
    def amount(self, value):
        """Set amount."""
        # try to set a new amount
        try:
            # only works, if input is integer, float or string
            self._amount = Decimal(str(value))
        except Exception:
            # otherwise don't do anything
            pass

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
            # only works, if input is integer, float or string
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


class ModEntry(BaseEntry):
    """Entry for modulating respecting other entries."""

    def __init__(self, title='Mod entry'):
        """Initialize the class."""
        super(ModEntry, self).__init__()
        self._connected = []
        self._title = str(title)

    @property
    def connected(self):
        """Get connected value."""
        return self._connected

    @connected.setter
    def connected(self, value):
        """Do not set the connected value."""
        pass

    def connect_entry(self, entry_id):
        """Append to the self._connected list."""
        self._connected.append(str(entry_id))

    def disconnect_entry(self, entry_id):
        """Delete the entry_id from the self._connected list."""
        if str(entry_id) in self._connected:
            self._connected.pop(self._connected.index(str(entry_id)))
