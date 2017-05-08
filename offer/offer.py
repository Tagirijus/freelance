"""
The class holds a list of entries.

The classes do not have privat values and setter and getter methods!
"""

from datetime import date as ddate
from decimal import Decimal
import json
from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry
from offer import time as time_module


class Offer(object):
    """A class holding a list of entries."""

    def __init__(
        self,
        title=None,
        date_fmt=None,
        date=None,
        entry_list=None
    ):
        """Initialize the class."""
        self.title = '' if title is None else str(title)
        self.date_fmt = '%d.%m.%Y' if date_fmt is None else str(date_fmt)
        self.date = ddate.today() if date is None else date
        self.entry_list = [] if entry_list is None else entry_list

    def append(self, entry=None):
        """Add entry to the entry_list."""
        is_entry = (type(entry) is BaseEntry or type(entry) is MultiplyEntry or
                    type(entry) is ConnectEntry)

        if not is_entry:
            return

        self.entry_list.append(entry)

    def pop(self, index):
        """Pop entry with the given index from list."""
        try:
            self.entry_list.pop(index)
        except Exception:
            pass

    def to_dict(self):
        """Convert object to dict."""
        out = {}

        # fetch the variables
        out['type'] = self.__class__.__name__
        out['title'] = self.title
        out['date_fmt'] = self.date_fmt
        try:
            out['date'] = self.ddate.strftime('%Y-%m-%d')
        except Exception:
            out['date'] = ddate.today().strftime('%Y-%m-%d')

        # fetch the jsons from the entries
        out['entry_list'] = []
        for entry in self.entry_list:
            try:
                out['entry_list'].append(entry.to_dict())
            except Exception:
                out['entry_list'].append(entry)

        return out

    def to_json(self, indent=2, ensure_ascii=False):
        """Convert variables data to json format."""
        return json.dumps(
            self.to_dict(),
            indent=indent,
            ensure_ascii=ensure_ascii,
            sort_keys=True
        )

    def load_entry_list_from_js(self, lis=None):
        """Convert list to entry object list."""
        entry_list = []
        # cycle through the list of dicts
        for entry in lis:
            # it should have a type key
            if 'type' in entry.keys():
                # entry is BaseEntry
                if entry['type'] == 'BaseEntry':
                    # convert this dict to an offer objetc then!
                    entry_list.append(BaseEntry().from_json(
                        js=entry
                    ))

                # entry is MultiplyEntry
                if entry['type'] == 'MultiplyEntry':
                    # convert this dict to an offer objetc then!
                    entry_list.append(MultiplyEntry().from_json(
                        js=entry
                    ))

                # entry is ConnectEntry
                if entry['type'] == 'ConnectEntry':
                    # convert this dict to an offer objetc then!
                    entry_list.append(ConnectEntry().from_json(
                        js=entry
                    ))

        return entry_list

    @classmethod
    def from_json(cls, js=None):
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

        # create object from json
        if 'title' in js.keys():
            title = js['title']
        else:
            title = None

        if 'date_fmt' in js.keys():
            date_fmt = js['date_fmt']
        else:
            date_fmt = None

        if 'date' in js.keys():
            try:
                date = ddate.strptime(js['date'], '%Y-%m-%d')
            except Exception:
                date = None
        else:
            date = None

        if 'entry_list' in js.keys():
            entry_list = js['entry_list']
            entry_list = cls().load_entry_list_from_js(lis=entry_list)
        else:
            entry_list = None

        # return new object
        return cls(
            title=title,
            date_fmt=date_fmt,
            date=date,
            entry_list=entry_list
        )

    def copy(self):
        """Copy the own offer into new offer object."""
        return Offer().from_json(js=self.to_json())

    def get_connected_entries(self, entry=None):
        """Return list with entries, which are connected to the given entry."""
        is_entry = (
            type(entry) is BaseEntry or
            type(entry) is MultiplyEntry or
            type(entry) is ConnectEntry
        )

        # return empty list, if argument is no valid entry object
        if not is_entry:
            return []

        # get connected ids from given entry
        connected = entry.get_connected()

        # init output list
        entries = []

        # iterate through entry_list and find connected entries
        for e in self.entry_list:
            if e.get_id() in connected:
                entries.append(e)

        # return list
        return entries

    def get_price_total(self, wage=None, tax=False):
        """Get prices of entries summerized."""
        # get wage as Decimal
        try:
            wage = Decimal(wage)
        except Exception:
            wage = Decimal(0)

        # init output variable
        out = Decimal(0)

        # iterate through the entries and get its price
        for e in self.entry_list:
            out += e.get_price(
                entry_list=self.entry_list,
                wage=wage
            ) if not tax else e.get_price_tax(
                entry_list=self.entry_list,
                wage=wage
            )

        # return it
        return out

    def get_price_tax_total(self, wage=None):
        """Get summerized total tax prices form entry_list."""
        return self.get_price_total(wage=wage, tax=True)

    def get_time_total(self):
        """Get times of entries summerized."""
        # init output variable
        out = time_module.timedelta(0)

        # iterate through the entries and get its time
        for e in self.entry_list:
            out += e.get_time(
                entry_list=self.entry_list
            )

        # return it
        return out

    def get_hourly_wage(self, wage=None, tax=False):
        """Calculate hourly wage according to price and time."""
        # get wage as Decimal
        try:
            wage = Decimal(wage)
        except Exception:
            wage = Decimal(0)

        # get price
        price = self.get_price_total(
            wage=wage,
            tax=tax
        )

        # get hours from total time
        hours = self.get_time_total().total_seconds() / 3600

        # simply return a Decimal with the calculation
        return round(Decimal(float(price) / hours), 2)
