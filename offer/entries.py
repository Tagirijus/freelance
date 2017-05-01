"""
The classes for entries.

The classes have privat values and setter and getter methods.
"""

from decimal import Decimal
import json
from offer import time as time_module
import uuid


class BaseEntry(object):
    """A very simple entry with basic options and FIXED values."""

    def __init__(
        self,
        id=None,
        title=None,
        comment=None,
        amount=None,
        amount_format=None,
        time=None,
        price=None,
        connected=None
    ):
        """Init the class."""
        # gen ID if not set, otherwise get it from argument
        self._id = str(uuid.uuid1()) if id is None else str(id)

        # get other variables from arguments
        self.title = '' if title is None else str(title)
        self.comment = '' if comment is None else str(comment)
        self._amount = Decimal('0.0')               # set Default
        self.set_amount(amount)                     # try to set arguments value
        self.amount_format = '' if amount_format is None else str(amount_format)
        self._time = time_module.to_timedelta(time)
        self._price = Decimal('0.0')                # set default
        self.set_price(price)                       # try to set arguments value

        # get the connected list (for ConnectEntry only)
        if type(connected) is set:
            self._connected = connected
        else:
            self._connected = set()

    def set_amount(self, value):
        """Set amount."""
        try:
            # only works if value is convertable to Decimal
            self._amount = Decimal(str(value))
        except Exception:
            pass

    def get_amount(self):
        """Get amount."""
        return self._amount

    def get_amount_str(self, fmt=None):
        """
        Get amount as string with possible formatting.

        In case the offer is for music production for example, it would
        be good if the quantity of the offer posting would not be listed
        as a decimal rather than a readable time format. So instead of
        "1,5 minutes" -> "1:30 min" or similar. With the following format
        options you can achieve this - also with leading zeros:

        {d}:    amount in decimal
        {H}:    amount converted to hours (will be leading number)
        {M}:    amount to minutes (if no {H}, it will be leading number)
        {S}:    amount seconds (if no {H} or {M} it will be leading number)

        Means that 1.5 with fmt == "{H}:{M}" would output 1:30, while
        fmt == "{M}:{S}" would output 1:30 as well, because the highest
        possible number formatting will get its value from the integer part
        of the decimal and the other from the fractional part.
        1.75 with fmt == "{H}:{M}:{S}" would output 1:45:00 for example.
        """
        # get self._amount_format if no argument is given
        if fmt is None:
            fmt = self.amount_format

        # init formating output variable
        format_me = {}

        # get simple decimal
        format_me['d'] = self.get_amount()

        # {H} will be leading number
        if '{H}' in fmt:
            # get values from timedelta
            tdelta = time_module.timedelta(hours=float(self.get_amount()))
            format_me['H'], rem = divmod(tdelta.seconds, 3600)
            format_me['M'], format_me['S'] = divmod(rem, 60)

            # correct leading zeros
            fmt = fmt.replace('{M}', '{M:02}').replace('{S}', '{S:02}')

        # {M} will be leading number
        elif '{H}' not in fmt and '{M}' in fmt:
            # get values from timedelta
            tdelta = time_module.timedelta(minutes=float(self.get_amount()))
            format_me['M'], format_me['S'] = divmod(tdelta.seconds, 60)

            # correct leading zeros
            fmt = fmt.replace('{S}', '{S:02}')

        # {S} will be leading number
        elif '{H}' not in fmt and '{M}' not in fmt and '{S}' in fmt:
            # get values from timedelta
            tdelta = time_module.timedelta(seconds=float(self.get_amount()))
            format_me['S'], rem = divmod(tdelta.seconds, 1)

        # output the stuff
        try:
            return fmt.format(**format_me)
        except Exception:
            # if any wrong {...} are given
            return fmt

    def set_time(self, value):
        """Set time."""
        self._time = time_module.to_timedelta(value)

    def get_time(self, *args, **kwargs):
        """Get time."""
        return self._time

    def get_hours(self, *args, **kwargs):
        """Get hours as decimal."""
        return time_module.get_decimal_hours_from_timedelta(
            self.get_time()
        )

    def set_price(self, value):
        """Set price."""
        # try to set a new price
        try:
            # only works, if input is integer, float or string
            self._price = round(Decimal(str(value)), 2)
        except Exception:
            # otherwise don't do anything
            pass

    def get_price(self, *args, **kwargs):
        """Get price."""
        return self._price

    def get_id(self):
        """Get id."""
        return self._id

    def get_connected(self):
        """Get connected set."""
        return self._connected

    def to_dict(self):
        """Convert all data to a dict."""
        out = {}

        # fetch all important data for this entry type
        out['type'] = self.__class__.__name__
        out['title'] = self.title
        out['comment'] = self.comment
        out['amount'] = float(self.get_amount())
        out['amount_format'] = self.amount_format
        out['id'] = self.get_id()
        out['time'] = float(self.get_hours())
        out['price'] = float(self.get_price())

        return out

    def to_json(self, indent=2, ensure_ascii=False):
        """Convert all data to json format."""
        return json.dumps(
            self.to_dict(),
            indent=indent,
            ensure_ascii=ensure_ascii,
            sort_keys=True
        )

    @classmethod
    def from_json(cls, js=None, preset_loading=False):
        """Convert all data from json format."""
        if js is None:
            return cls()

        # get js as dict
        if type(js) is not dict:
            try:
                js = json.loads(js)
            except Exception:
                # return default object
                return cls()

        # create new entry object from json

        # get ID if it's no preset_loading
        if preset_loading:
            id = None
        else:
            if 'id' in js.keys():
                id = js['id']
            else:
                id = None

        # get other values
        if 'title' in js.keys():
            title = js['title']
        else:
            title = None

        if 'comment' in js.keys():
            comment = js['comment']
        else:
            comment = None

        if 'amount' in js.keys():
            amount = js['amount']
        else:
            amount = None

        if 'amount_format' in js.keys():
            amount_format = js['amount_format']
        else:
            amount_format = None

        if 'time' in js.keys():
            time = js['time']
        else:
            time = None

        if 'price' in js.keys():
            price = js['price']
        else:
            price = None

        return cls(
            id=id,
            title=title,
            comment=comment,
            amount=amount,
            amount_format=amount_format,
            time=time,
            price=price
        )

    def copy(self):
        """Return a copy of this object."""
        return BaseEntry().from_json(js=self.to_json())


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
        id=None,
        title=None,
        comment=None,
        amount=None,
        amount_format=None,
        hour_rate=None
    ):
        """Initialize the class."""
        # values of the BaseEntry class
        super(MultiplyEntry, self).__init__(
            id=id,
            title=title,
            comment=comment,
            amount=amount,
            amount_format=amount_format
        )

        # new values for this class
        self._hour_rate = time_module.to_timedelta(hour_rate)

    def set_time(self, value):
        """Disable the function."""
        pass

    def get_time(self, *args, **kwargs):
        """Get own amount * own hour as time."""
        return float(self.get_amount()) * self.get_hour_rate()

    def get_hours(self, *args, **kwargs):
        """Get hours as decimal."""
        return time_module.get_decimal_hours_from_timedelta(
            self.get_time()
        )

    def set_price(self, value):
        """Disable function."""
        pass

    def get_price(self, wage=Decimal('0.00'), *args, **kwargs):
        """Get own time * wage as price."""
        return round(self.get_hours() * wage, 2)

    def set_hour_rate(self, value):
        """Set hour_rate."""
        self._hour_rate = time_module.to_timedelta(value)

    def get_hour_rate(self):
        """Get hour_rate."""
        return self._hour_rate

    def to_dict(self):
        """Convert object to dict."""
        out = {}

        # fetch all important data for this entry type
        out['type'] = self.__class__.__name__
        out['title'] = self.title
        out['comment'] = self.comment
        out['amount'] = float(self.get_amount())
        out['amount_format'] = self.amount_format
        out['id'] = self.get_id()
        out['hour_rate'] = float(time_module.get_decimal_hours_from_timedelta(
            self.get_hour_rate()
        ))

        return out

    def to_json(self, indent=2, ensure_ascii=False):
        """Convert all data to json format."""
        return json.dumps(
            self.to_dict(),
            indent=indent,
            ensure_ascii=ensure_ascii,
            sort_keys=True
        )

    @classmethod
    def from_json(cls, js=None, preset_loading=False):
        """Convert all data from json format."""
        if js is None:
            return cls()

        # get js as dict
        if type(js) is not dict:
            try:
                js = json.loads(js)
            except Exception:
                # return default object
                return cls()

        # create new entry object from json

        # get ID if it's no preset_loading
        if preset_loading:
            id = None
        else:
            if 'id' in js.keys():
                id = js['id']
            else:
                id = None

        # get other values
        if 'title' in js.keys():
            title = js['title']
        else:
            title = None

        if 'comment' in js.keys():
            comment = js['comment']
        else:
            comment = None

        if 'amount' in js.keys():
            amount = js['amount']
        else:
            amount = None

        if 'amount_format' in js.keys():
            amount_format = js['amount_format']
        else:
            amount_format = None

        if 'hour_rate' in js.keys():
            hour_rate = js['hour_rate']
        else:
            hour_rate = None

        return cls(
            id=id,
            title=title,
            comment=comment,
            amount=amount,
            amount_format=amount_format,
            hour_rate=hour_rate
        )

    def copy(self):
        """Return a copy of this object."""
        return MultiplyEntry().from_json(js=self.to_json())


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
        id=None,
        title=None,
        comment=None,
        amount=None,
        amount_format=None,
        connected=None,
        is_time=None,
        multiplicator=None
    ):
        """Initialize the class."""
        # values of the BaseEntry class
        super(ConnectEntry, self).__init__(
            id=id,
            title=title,
            comment=comment,
            amount=amount,
            amount_format=amount_format,
            connected=connected
        )

        # new values for this class
        self._is_time = bool(is_time)
        self._multiplicator = Decimal('0.0')    # set default
        self.set_multiplicator(multiplicator)   # try to set arguments value

    def set_time(self, value):
        """Disable the function."""
        pass

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
        # if is_time() == False or entry_list not a list, return 0 timedelta
        if not self.get_is_time() or type(entry_list) is not list:
            return time_module.to_timedelta(0)
        # is_time() == True, calculate time respecting other entires
        else:
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

    def get_hours(self, entry_list=None):
        """Get hours as decimal."""
        if type(entry_list) is None:
            return Decimal('0.0')
        else:
            return time_module.get_decimal_hours_from_timedelta(
                self.get_time(entry_list=entry_list)
            )

    def set_price(self, value):
        """Disable function."""
        pass

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
        if self.get_is_time():
            return round(self.get_hours(entry_list=entry_list) * wage, 2)
        else:
            # otherwise iterate through entry_list and find prices of
            # entries which ids exist in the self._connected list
            # and multiply them
            out = Decimal('0.00')
            for entry in entry_list:
                if entry.get_id() in self._connected:
                    # if its in the list, multiply its price and add it
                    out += (self.get_multiplicator() *
                            entry.get_price(
                                entry_list=entry_list,
                                wage=wage))
            # return the value
            return round(out * self.get_amount(), 2)

    def set_multiplicator(self, value):
        """Set multiplicator."""
        # try to set a new multiplicator
        try:
            # only works, if input is integer, float or string
            self._multiplicator = Decimal(str(value))
        except Exception:
            # otherwise don't do anything
            pass

    def get_multiplicator(self):
        """Get multiplicator."""
        return self._multiplicator

    def set_is_time(self, value):
        """Set is_time value."""
        self._is_time = bool(value)

    def get_is_time(self, set_it=None):
        """Get is_time value."""
        return self._is_time

    def connect_entry(self, entry_list=None, entry_id=None, disconnect=False):
        """
        Append entry to the self._connected set.

        This function searches for the entry with the ID == entry_id
        in the entry_list. If it exists, it checks if the own ID does
        not exists in the found entry.get_connected() set and appends
        it to the own self._connected set then, if it.
        """
        one_not_set = type(entry_list) is not list or type(entry_id) is None
        is_own_id = entry_id == self.get_id()

        # cancel if one argument is not given or if entry_id is the own
        if one_not_set or is_own_id:
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

    def to_dict(self):
        """Convert object to dict."""
        out = {}

        # fetch all important data for this entry type
        out['type'] = self.__class__.__name__
        out['title'] = self.title
        out['comment'] = self.comment
        out['amount'] = float(self.get_amount())
        out['amount_format'] = self.amount_format
        out['id'] = self.get_id()
        out['is_time'] = self.get_is_time()
        out['multiplicator'] = float(self.get_multiplicator())
        out['connected'] = list(self.get_connected())

        return out

    def to_json(self, indent=2, ensure_ascii=False):
        """Convert all data to json format."""
        return json.dumps(
            self.to_dict(),
            indent=indent,
            ensure_ascii=ensure_ascii,
            sort_keys=True
        )

    @classmethod
    def from_json(cls, js=None, preset_loading=False):
        """Convert all data from json format."""
        if js is None:
            return cls()

        # get js as dict
        if type(js) is not dict:
            try:
                js = json.loads(js)
            except Exception:
                # return default object
                return cls()

        # create new entry object from json

        # get ID, if it's no preset_loading
        if preset_loading:
            id = None
        else:
            if 'id' in js.keys():
                id = js['id']
            else:
                id = None

        # get other values
        if 'title' in js.keys():
            title = js['title']
        else:
            title = None

        if 'comment' in js.keys():
            comment = js['comment']
        else:
            comment = None

        if 'amount' in js.keys():
            amount = js['amount']
        else:
            amount = None

        if 'amount_format' in js.keys():
            amount_format = js['amount_format']
        else:
            amount_format = None

        if 'is_time' in js.keys():
            is_time = js['is_time']
        else:
            is_time = None

        if 'multiplicator' in js.keys():
            multiplicator = js['multiplicator']
        else:
            multiplicator = None

        # get connected entries, if it's no preset_loading
        if 'connected' in js.keys() and not preset_loading:
            connected = set(js['connected'])
        else:
            connected = None

        return cls(
            id=id,
            title=title,
            comment=comment,
            amount=amount,
            amount_format=amount_format,
            is_time=is_time,
            multiplicator=multiplicator,
            connected=connected
        )

    def copy(self):
        """Return a copy of this object."""
        return ConnectEntry().from_json(js=self.to_json())
