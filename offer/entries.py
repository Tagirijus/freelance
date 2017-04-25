"""The classes for entries."""

from decimal import Decimal
from offer import time as time_module
import uuid


class BaseEntry(object):
    """A very simple entry with basic options and FIXED values."""

    def __init__(
        self,
        title='Base entry',
        comment='',
        amount=1.0,
        time=0.0,
        price=0.00
    ):
        """Init the class."""
        self._title = str(title)
        self._comment = str(comment)
        self._amount = Decimal('0.0')               # set default
        self.set_amount(amount)                     # try to set arguments value
        self._time = time_module.to_timedelta(time)
        self._price = Decimal('0.00')               # set default
        self.set_price(price)                       # try to set arguments value
        self._id = str(uuid.uuid1())
        self._connected = set()

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
        self._title = str(value)

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

    def get_time(self, *args, **kwargs):
        """Get time."""
        return self._time

    def set_time(self, value):
        """Set time."""
        self._time = time_module.to_timedelta(value)

    def get_hours(self, *args, **kwargs):
        """Get hours as decimal."""
        return time_module.get_decimal_hours_from_timedelta(
            self.get_time()
        )

    def get_price(self, *args, **kwargs):
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

    def get_connected(self):
        """Get connected list."""
        return self._connected


class MultiplyEntry(BaseEntry):
    """
    A multiplying entry.

    This entry type is similar to the BaseEntry, except that
    it calculates the time according to a given hour_rate value.
    The class has a new value "hour_rate" which will be multiplicated
    by the amount and thus calculates the time.
    """

    def __init__(
        self,
        title='Multiply entry',
        comment='',
        amount=1.0,
        hour_rate=1.0
    ):
        """Initialize the class."""
        super(MultiplyEntry, self).__init__()
        self._title = str(title)
        self._comment = str(comment)
        self._amount = Decimal('0.0')               # set default
        self.set_amount(amount)                     # try to set arguments value
        self._hour_rate = time_module.to_timedelta(hour_rate)

    def get_time(self, *args, **kwargs):
        """Get own amount * own hour as time."""
        return float(self.get_amount()) * self.get_hour_rate()

    def set_time(self, value):
        """Disable the function."""
        pass

    def get_hours(self, *args, **kwargs):
        """Get hours as decimal."""
        return time_module.get_decimal_hours_from_timedelta(
            self.get_time()
        )

    def get_price(self, wage=Decimal('0.00'), *args, **kwargs):
        """Get own time * wage as price."""
        return round(self.get_hours() * wage, 2)

    def set_price(self, value):
        """Disable function."""
        pass

    def get_hour_rate(self):
        """Get hour_rate."""
        return self._hour_rate

    def set_hour_rate(self, value):
        """Set hour_rate."""
        self._hour_rate = time_module.to_timedelta(value)


class ConnectEntry(BaseEntry):
    """
    This entry type can connect to other entries.

    It's meant to act as a modulator respecting other entries.
    If it is connected to other entries, it calculates time
    and price according to the time and price of the connected
    entries multiplied by the own multiplicator.
    """

    def __init__(
        self,
        title='Connect entry',
        comment='',
        amount=1.0,
        is_time=True,
        multiplicator=1.0
    ):
        """Initialize the class."""
        super(ConnectEntry, self).__init__()
        self._title = str(title)
        self._comment = str(comment)
        self._amount = Decimal('0.0')           # set default
        self.set_amount(amount)                 # try to set arguments value
        self._is_time = bool(is_time)
        self._multiplicator = Decimal('1.0')    # set default
        self.set_multiplicator(multiplicator)   # try to set arguments value

    def get_time(self, entry_list=None, *args, **kwargs):
        """
        Get time according to entry_list or zero.

        entry_list is the global list holding all entry-objects.
        This function calculates the time respecting the entries from the
        entry_list. The ConnectEntry class is an entry for multiplying entries
        times or only prices (depenging on self.is_time()) - e.g. licences
        can cost x-times multiplied the original working time of a task.
        This class can calculate it.
        """
        # if is_time() == False, return 0 timedelta
        if not self.is_time() or type(entry_list) is None:
            return time_module.to_timedelta(0)
        # is_time() == True, calculate time respecting other entires
        else:
            # cancel and return zero, if entry_list is no list
            if type(entry_list) != list:
                return time_module.to_timedelta(0)

            # otherwise iterate through entry_list and find
            # entries which ids exist in the self._connected list
            out = time_module.to_timedelta(0)
            for entry in entry_list:
                if entry.get_id() in self._connected:
                    # if its in the list, multiply its time and add it
                    out += (float(self.get_multiplicator()) *
                            entry.get_time(entry_list=entry_list))
            # return the result
            return out * float(self.get_amount())

    def set_time(self, value):
        """Disable the function."""
        pass

    def get_hours(self, entry_list=None):
        """Get hours as decimal."""
        if type(entry_list) is None:
            return Decimal('0.0')
        else:
            return time_module.get_decimal_hours_from_timedelta(
                self.get_time(entry_list=entry_list)
            )

    def get_price(self, entry_list=None, wage=Decimal('0.00')):
        """
        Get price according to entry_list or self.get_time().

        entry_list is the global list holding all entry-objects.
        Depending on self.is_time() this function calculates the price
        according to the entry_list. It is similar to self.get_time(),
        but it just calculates the prices instead of the time_module.
        wage should be a Decimal() object.
        """
        # if no list is given, return zero
        if type(entry_list) is None:
            return Decimal('0.00')
        # if self.is_time() == True, just multiply self.get_hours() * wage
        if self.is_time():
            return round(self.get_hours(entry_list=entry_list) * wage, 2)
        else:
            # otherwise iterate through entry_list and find prices of
            # entries which ids exist in the self._connected list
            # and multiply them
            out = Decimal(0)
            for entry in entry_list:
                if entry.get_id() in self._connected:
                    # if its in the list, multiply its price and add it
                    out += (self.get_multiplicator() *
                            entry.get_price(
                                entry_list=entry_list,
                                wage=wage))
            # return the value
            return round(out * self.get_amount(), 2)

    def set_price(self, value):
        """Disable function."""
        pass

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
        """Get is_time value."""
        return self._is_time

    def set_is_time(self, value):
        """Set is_time value."""
        self._is_time = bool(value)

    def connect_entry(self, entry_list=None, entry_id=None, disconnect=False):
        """
        Append entry to the self._connected set.

        This function searches for the entry with the ID == entry_id
        in the entry_list. If it exists, it checks if the own ID does
        not exists in the found entry.get_connected() set and appends
        it to the own self._connected set then, if it.
        """
        # if one argument is not given, cancel
        if type(entry_list) is None or type(entry_id) is None:
            return

        # also cancel if entry_id is the own
        if entry_id == self.get_id():
            return

        # check if other entry id exists in entry_list
        connection_possible = False
        for index, entry in enumerate(entry_list):
            if entry.get_id() == entry_id:
                # and also check if the entry has self.get_id()
                # in its get_connected() set.
                if self.get_id() not in entry.get_connected():
                    connection_possible = True

        # cancel if nothing found
        if not connection_possible:
            return

        # append / "connect" id to _connected set
        # or remove / "discconnect" id to _connected set
        if disconnect:
            self._connected -= set([entry_id])
        else:
            self._connected |= set([entry_id])

    def disconnect_entry(self, entry_list=None, entry_id=None):
        """Delete the entry_id from the _connected set."""
        self.connect_entry(
            entry_list=entry_list,
            entry_id=entry_id,
            disconnect=True
        )
