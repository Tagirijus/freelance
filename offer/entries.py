"""
The classes for entries.

The classes have privat values and setter and getter methods.
"""

from decimal import Decimal
import json
from offer.offeramounttime import OfferAmountTime
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
        amount_b=None,
        amount_b_format=None,
        tax=None,
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
        self._amount = OfferAmountTime(amount)
        self.amount_format = '' if amount_format is None else str(amount_format)
        if amount_b is None:
            self._amount_b = OfferAmountTime(1)
        else:
            self._amount_b = OfferAmountTime(amount_b)
        self.amount_b_format = '' if amount_b_format is None else str(amount_b_format)
        self._tax = Decimal(0)                  # set default
        self.set_tax(tax)                       # try to set arguments value
        self._time = OfferAmountTime(time)
        self._price = Decimal(0)                # set default
        self.set_price(price)                   # try to set arguments value

        # get the connected list (for ConnectEntry only)
        if type(connected) is set:
            self._connected = connected
        else:
            self._connected = set()

    def get_id(self):
        """Get id."""
        return self._id

    def set_amount(self, value):
        """Set amount."""
        self._amount.set(value)

    def get_amount(self):
        """Get amount."""
        return self._amount

    def get_amount_str(self, fmt=None):
        """Get self._amount as string."""
        return self.get_amount_universal_str(
            fmt=fmt,
            amount=self._amount,
            amount_fmt=self.amount_format
        )

    def set_amount_b(self, value):
        """Set amount_b."""
        self._amount_b.set(value)

    def get_amount_b(self):
        """Get amount_b."""
        return self._amount_b

    def get_amount_b_str(self, fmt=None):
        """Get self._amount_b as string."""
        return self.get_amount_universal_str(
            fmt=fmt,
            amount=self._amount_b,
            amount_fmt=self.amount_b_format
        )

    def get_amount_universal_str(self, fmt=None, amount=None, amount_fmt=None):
        """
        Get amount as string with possible formatting.

        In case the offer is for music production for example, it would
        be good if the quantity of the offer posting would not be listed
        as a decimal rather than a readable time format. So instead of
        "1.5 min" -> "1:30 min" or similar. With the following format
        options you can achieve this - also with leading zeros:

        {s}: standard automatic amount
        {d}: amount in decimal
        {F}: amount converted to time, show full
        {R}: amount converted to time, show remaining

        Means that 1.5 with fmt == "{F}:{R}" would output 0:01, while
        fmt == "{F}:{R}" would output 1:30. 61.75 with
        """
        if type(amount) is not OfferAmountTime:
            return str(fmt)

        # get self.amount_format if no argument is given
        if fmt is None:
            fmt = amount_fmt

        # is this also is empty, get '{s}' as default output
        # (so that it shows the default at least)
        if fmt == '':
            fmt = '{s}'

        # init formating output variable
        format_me = {}

        # get format_me
        format_me['s'] = amount
        format_me['d'] = amount.get()
        format_me['F'] = amount.full()
        format_me['R'] = amount.remain()

        # {F} exists
        if '{F}' in fmt:
            # correct leading zeros
            fmt = fmt.replace('{R}', '{R:02}')

        # output the stuff
        try:
            return fmt.format(**format_me)
        except Exception:
            # if any wrong {...} are given
            return fmt

    def set_tax(self, value):
        """Set tax."""
        # check if value is decimal
        try:
            is_percent = True if float(value) > 1.0 else False
        except Exception:
            is_percent = False

        # try to set a new tax
        try:
            # only works, if input is integer, float or string
            if is_percent:
                self._tax = Decimal(str(value)) / 100
            else:
                self._tax = Decimal(str(value))
        except Exception:
            # otherwise don't do anything
            pass

    def get_tax(self, *args, **kwargs):
        """Get tax."""
        return self._tax

    def get_tax_percent(self, *args, **kwargs):
        """Get tax."""
        return self._tax * 100

    def set_time(self, value):
        """Set time."""
        self._time.set(value)

    def get_time(self, *args, **kwargs):
        """Get time."""
        self._time.type('time')
        return self._time * self._amount * self._amount_b

    def get_time_raw(self, *args, **kwargs):
        """Get raw time value."""
        self._time.type('time')
        return self._time

    def get_time_zero(self, *args, **kwargs):
        """Get time as '-' if time is 0, else str of time."""
        if self.get_time(*args, **kwargs) == OfferAmountTime(0):
            return '-'
        else:
            return str(self.get_time(*args, **kwargs))

    def set_price(self, value):
        """Set price."""
        # try to set a new price
        try:
            # only works, if input is integer, float or string
            self._price = round(Decimal(str(value)), 2)
        except Exception:
            # otherwise don't do anything
            pass

    def get_price(self, round_price=False, *args, **kwargs):
        """Get price."""
        if round_price:
            rounder = 0
        else:
            rounder = 2
        return round(self._price * self._amount.get() * self._amount_b.get(), rounder)

    def get_unit_price(self, round_price=False, *args, **kwargs):
        """Get price / amount."""
        amounts = self._amount.get() * self._amount_b.get()

        # divide with amount, if its > 0
        if amounts > 0:
            return round(
                self.get_price(
                    round_price=round_price,
                    *args,
                    **kwargs
                ) / amounts,
                2
            )

        # fallback output: simple get_price
        else:
            return round(
                self.get_price(
                    round_price=round_price,
                    *args,
                    **kwargs
                ),
                2
            )

    def get_price_raw(self):
        """Get raw price value."""
        return self._price

    def get_price_tax(self, *args, **kwargs):
        """Get tax of the price."""
        return round(
            self._tax * self.get_price(
                *args,
                **kwargs
            ),
            2
        )

    def get_unit_price_tax(self, *args, **kwargs):
        """Get price_tax / amount."""
        amounts = self._amount.get() * self._amount_b.get()

        # divide with amount, if its > 0
        if amounts > 0:
            return round(
                self.get_price_tax(
                    *args,
                    **kwargs
                ) / amounts,
                2
            )

        # fallback output: simple get_price_tax
        else:
            return round(
                self.get_price_tax(
                    *args,
                    **kwargs
                ),
                2
            )

    def get_connected(self):
        """Get connected set."""
        return self._connected

    def to_dict(self):
        """Convert all data to a dict."""
        out = {}

        # fetch all important data for this entry type
        out['type'] = self.__class__.__name__
        out['id'] = self.get_id()
        out['title'] = self.title
        out['comment'] = self.comment
        out['amount'] = str(self._amount)
        out['amount_format'] = self.amount_format
        out['amount_b'] = str(self._amount_b)
        out['amount_b_format'] = self.amount_b_format
        out['tax'] = float(self._tax)
        out['time'] = str(self._time)
        out['price'] = float(self._price)

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
    def from_json(cls, js=None, keep_id=True):
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
        if not keep_id:
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

        if 'amount_b' in js.keys():
            amount_b = js['amount_b']
        else:
            amount_b = None

        if 'amount_b_format' in js.keys():
            amount_b_format = js['amount_b_format']
        else:
            amount_b_format = None

        if 'tax' in js.keys():
            tax = js['tax']
        else:
            tax = None

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
            amount_b=amount_b,
            amount_b_format=amount_b_format,
            tax=tax,
            time=time,
            price=price
        )

    def copy(self, keep_id=True):
        """Return a copy of this object."""
        return BaseEntry().from_json(js=self.to_json(), keep_id=keep_id)

    def is_project(self, project=None):
        """
        Check if given argument is project object.

        This is some kind of workaround, since I canot import the Project class
        into Offer module due to circular dependencies. Do I really still have
        a that bad programm manufacture? )=
        """
        try:
            return project.i_am_project()
        except Exception:
            return False

    def return_changed_type(
        self,
        into='BaseEntry',
        entry_list=None,
        wage=None,
        project=None,
        round_price=None
    ):
        """Return the own entry object into other entry object."""
        # return changed into MultiplyEntry
        if into == 'MultiplyEntry':
            new_entry = MultiplyEntry(
                id=self.get_id(),
                title=self.title,
                comment=self.comment,
                amount=self.get_amount(),
                amount_format=self.amount_format,
                amount_b=self.get_amount_b(),
                amount_b_format=self.amount_b_format,
                tax=self.get_tax()
            )

            return new_entry

        # return changed into ConnectEntry
        elif into == 'ConnectEntry':
            new_entry = ConnectEntry(
                id=self.get_id(),
                title=self.title,
                comment=self.comment,
                amount=self.get_amount(),
                amount_format=self.amount_format,
                amount_b=self.get_amount_b(),
                amount_b_format=self.amount_b_format,
                tax=self.get_tax()
            )

            return new_entry

        # return changed into BaseEntry (also as fallback if into argument is invalid)
        else:
            new_entry = BaseEntry(
                id=self.get_id(),
                title=self.title,
                comment=self.comment,
                amount=self.get_amount(),
                amount_format=self.amount_format,
                amount_b=self.get_amount_b(),
                amount_b_format=self.amount_b_format,
                tax=self.get_tax(),
                price=self.get_price(
                    entry_list=entry_list,
                    wage=wage,
                    round_price=round_price
                ),
                time=self.get_time(
                    entry_list=entry_list
                )
            )

            return new_entry


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
        amount_b=None,
        amount_b_format=None,
        tax=None,
        hour_rate=None
    ):
        """Initialize the class."""
        # values of the BaseEntry class
        super(MultiplyEntry, self).__init__(
            id=id,
            title=title,
            comment=comment,
            amount=amount,
            amount_format=amount_format,
            amount_b=amount_b,
            amount_b_format=amount_b_format,
            tax=tax
        )

        # new values for this class
        self._hour_rate = OfferAmountTime(hour_rate)

    def set_time(self, value):
        """Disable the function."""
        pass

    def get_time(self, *args, **kwargs):
        """Get own amount * own hour as time."""
        out = self._amount * self._amount_b * self._hour_rate
        out.type('time')
        return out

    def set_price(self, value):
        """Disable function."""
        pass

    def get_price(self, wage=Decimal('0.00'), round_price=False, *args, **kwargs):
        """Get own time * wage as price."""
        if round_price:
            rounder = 0
        else:
            rounder = 2
        return round(self.get_time(*args, **kwargs).get() * wage, rounder)

    def set_hour_rate(self, value):
        """Set hour_rate."""
        self._hour_rate.set(value)

    def get_hour_rate(self):
        """Get hour_rate."""
        return self._hour_rate

    def to_dict(self):
        """Convert object to dict."""
        out = {}

        # fetch all important data for this entry type
        out['type'] = self.__class__.__name__
        out['id'] = self.get_id()
        out['title'] = self.title
        out['comment'] = self.comment
        out['amount'] = str(self._amount)
        out['amount_format'] = self.amount_format
        out['amount_b'] = str(self._amount_b)
        out['amount_b_format'] = self.amount_b_format
        out['tax'] = float(self._tax)
        out['hour_rate'] = str(self._hour_rate)

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
    def from_json(cls, js=None, keep_id=True):
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
        if not keep_id:
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

        if 'amount_b' in js.keys():
            amount_b = js['amount_b']
        else:
            amount_b = None

        if 'amount_b_format' in js.keys():
            amount_b_format = js['amount_b_format']
        else:
            amount_b_format = None

        if 'tax' in js.keys():
            tax = js['tax']
        else:
            tax = None

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
            amount_b=amount_b,
            amount_b_format=amount_b_format,
            tax=tax,
            hour_rate=hour_rate
        )

    def copy(self, keep_id=True):
        """Return a copy of this object."""
        return MultiplyEntry().from_json(js=self.to_json(), keep_id=keep_id)


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
        amount_b=None,
        amount_b_format=None,
        tax=None,
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
            amount_b=amount_b,
            amount_b_format=amount_b_format,
            tax=tax,
            connected=connected
        )

        # new values for this class
        self._is_time = bool(is_time)
        self._multiplicator = Decimal(0)    # set default
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
        # if is_time() == False or entry_list not a list, return 0
        if not self.get_is_time() or type(entry_list) is not list:
            return OfferAmountTime('0:00')
        # is_time() == True, calculate time respecting other entires
        else:
            # otherwise iterate through entry_list and find
            # entries which ids exist in the self._connected list
            out = OfferAmountTime('0:00')
            for entry in entry_list:
                if entry.get_id() in self._connected:
                    # if its in the list, multiply its time and add it
                    out += (self.get_multiplicator() *
                            entry.get_time(entry_list=entry_list))
            # return the result
            return out * self._amount * self._amount_b

    def set_price(self, value):
        """Disable function."""
        pass

    def get_price(
        self,
        entry_list=None,
        wage=Decimal('0.00'),
        round_price=False,
        *args,
        **kwargs
    ):
        """
        Get price according to entry_list or self.get_time().

        entry_list is the global list holding all entry-objects.
        Depending on self.is_time() this function calculates the price
        according to the entry_list. It is similar to self.get_time(),
        but it just calculates the prices instead of the time_module.
        wage should be a Decimal() object.
        """
        # set up rounder
        if round_price:
            rounder = 0
        else:
            rounder = 2

        # if no list is given, return zero
        if type(entry_list) is None:
            return Decimal('0.00')
        # if self.is_time() == True, just multiply self.get_hours() * wage
        if self.get_is_time():
            return round(self.get_time(entry_list=entry_list).get() * wage, rounder)
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
            return round(out * self._amount.get() * self._amount_b.get(), rounder)

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

    def get_is_time(self):
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
            return False

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
            return False

        # append / "connect" id to _connected set
        # or remove / "discconnect" id to _connected set
        if disconnect:
            self._connected -= set([entry_id])
        else:
            self._connected |= set([entry_id])

        return True

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
        out['id'] = self.get_id()
        out['title'] = self.title
        out['comment'] = self.comment
        out['amount'] = str(self._amount)
        out['amount_format'] = self.amount_format
        out['amount_b'] = str(self._amount_b)
        out['amount_b_format'] = self.amount_b_format
        out['tax'] = float(self._tax)
        out['is_time'] = self.get_is_time()
        out['multiplicator'] = float(self._multiplicator)
        out['connected'] = list(self._connected)

        return out

    def disconnect_all_entries(self):
        """Delete all connections."""
        self._connected = set()

    def to_json(self, indent=2, ensure_ascii=False):
        """Convert all data to json format."""
        return json.dumps(
            self.to_dict(),
            indent=indent,
            ensure_ascii=ensure_ascii,
            sort_keys=True
        )

    @classmethod
    def from_json(cls, js=None, keep_id=True):
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
        if not keep_id:
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

        if 'amount_b' in js.keys():
            amount_b = js['amount_b']
        else:
            amount_b = None

        if 'amount_b_format' in js.keys():
            amount_b_format = js['amount_b_format']
        else:
            amount_b_format = None

        if 'tax' in js.keys():
            tax = js['tax']
        else:
            tax = None

        if 'is_time' in js.keys():
            is_time = js['is_time']
        else:
            is_time = None

        if 'multiplicator' in js.keys():
            multiplicator = js['multiplicator']
        else:
            multiplicator = None

        if 'connected' in js.keys():
            connected = set(js['connected'])
        else:
            connected = None

        return cls(
            id=id,
            title=title,
            comment=comment,
            amount=amount,
            amount_format=amount_format,
            amount_b=amount_b,
            amount_b_format=amount_b_format,
            tax=tax,
            is_time=is_time,
            multiplicator=multiplicator,
            connected=connected
        )

    def copy(self, keep_id=True):
        """Return a copy of this object."""
        return ConnectEntry().from_json(js=self.to_json(), keep_id=keep_id)
