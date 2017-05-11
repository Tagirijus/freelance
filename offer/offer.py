"""
The class holds a list of entries.

The classes do not have privat values and setter and getter methods!
"""

from datetime import date as ddate
from datetime import datetime
from datetime import timedelta
from decimal import Decimal
import json
from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry
from offer.offeramounttime import OfferAmountTime

from general.debug import debug


class Offer(object):
    """A class holding a list of entries."""

    def __init__(
        self,
        title=None,
        date_fmt=None,
        date=None,
        wage=None,
        round_price=None,
        entry_list=None
    ):
        """Initialize the class."""
        self.title = '' if title is None else str(title)
        self.date_fmt = '%d.%m.%Y' if date_fmt is None else str(date_fmt)
        self._date = ddate.today()          # set default
        self.set_date(date)                 # try to set arguments value
        self._round_price = False           # set default
        self.set_round_price(round_price)   # try to set arguments value
        self._wage = Decimal(0)             # set default
        self.set_wage(wage)                 # try to set arguments value
        self._entry_list = []               # set default
        self.set_entry_list(entry_list)     # try to set arguments value

    def set_date(self, value):
        """Set date."""
        if type(value) is ddate:
            self._date = value
        else:
            try:
                self._date = datetime.strptime(value, '%Y-%m-%d').date()
            except Exception:
                pass

    def get_date(self):
        """Get date."""
        return self._date

    def set_wage(self, value):
        """Set wage."""
        try:
            # only works if value is convertable to Decimal
            self._wage = Decimal(str(value))
        except Exception:
            pass

    def get_round_price(self):
        """Get round_price."""
        return self._round_price

    def set_round_price(self, value):
        """Set round_price."""
        self._round_price = bool(value)

    def get_wage(self, project=None):
        """Get wage."""
        # tr to get projects wage
        if self.is_project(project):
            p_wage = project.get_wage()
        else:
            p_wage = Decimal(0)

        # return project wage, if own wage is 0, other wise return own wage
        if self._wage == 0:
            return p_wage
        else:
            return self._wage

    def set_entry_list(self, value):
        """Set entry_list."""
        if type(value) is list:
            self._entry_list = value

    def get_entry_list(self):
        """Get entry_list."""
        return self._entry_list

    def append(self, entry=None):
        """Add entry to the entry_list."""
        is_entry = (type(entry) is BaseEntry or type(entry) is MultiplyEntry or
                    type(entry) is ConnectEntry)

        if not is_entry:
            return

        self._entry_list.append(entry)

    def pop(self, index):
        """Pop entry with the given index from list."""
        try:
            self._entry_list.pop(index)
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
            out['date'] = self._date.strftime('%Y-%m-%d')
        except Exception:
            out['date'] = ddate.today().strftime('%Y-%m-%d')

        out['wage'] = float(self._wage)
        out['round_price'] = self._round_price

        # fetch the jsons from the entries
        out['entry_list'] = []
        for entry in self._entry_list:
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
                date = datetime.strptime(js['date'], '%Y-%m-%d').date()
            except Exception:
                date = None
        else:
            date = None

        if 'wage' in js.keys():
            wage = js['wage']
        else:
            wage = None

        if 'round_price' in js.keys():
            round_price = js['round_price']
        else:
            round_price = None

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
            wage=wage,
            round_price=round_price,
            entry_list=entry_list
        )

    def copy(self):
        """Copy the own offer into new offer object."""
        return Offer().from_json(js=self.to_json())

    def get_price_total(self, wage=None, project=None, tax=False, round_price=None):
        """Get prices of entries summerized."""
        if wage is None:
            wage = self.get_wage(project=project)

        if round_price is None:
            round_price = self._round_price

        # init output variable
        out = Decimal(0)

        # iterate through the entries and get its price
        for e in self._entry_list:
            out += e.get_price(
                entry_list=self._entry_list,
                wage=wage
            ) if not tax else e.get_price_tax(
                entry_list=self._entry_list,
                wage=wage
            )

        # return it, check if rounded or not
        if round_price:
            return round(out)
        else:
            return out

    def get_price_tax_total(self, wage=None, project=None, round_price=None):
        """Get summerized total tax prices form entry_list."""
        return self.get_price_total(
            wage=wage, project=project, tax=True, round_price=round_price
        )

    def get_time_total(self):
        """Get times of entries summerized."""
        # init output variable
        out = OfferAmountTime('0:00')

        # iterate through the entries and get its time
        for e in self._entry_list:
            out += e.get_time(
                entry_list=self._entry_list
            )

        # return it
        return out

    def get_hourly_wage(self, wage=None, project=None, tax=False, round_price=None):
        """Calculate hourly wage according to price and time."""
        if wage is None:
            wage = self.get_wage(project=project)

        if round_price is None:
            round_price = self._round_price

        # get price
        price = self.get_price_total(
            wage=wage,
            tax=tax,
            round_price=round_price
        )

        # get hours from total time
        hours = self.get_time_total().get()

        # check round price for own output
        if round_price:
            rounder = 0
        else:
            rounder = 2

        # simply return a Decimal with the calculation
        if hours > 0.0:
            return round(Decimal(float(price) / float(hours)), rounder)
        else:
            return round(Decimal(0), rounder)

    def get_finish_date(self, project=None):
        """Calculate and return the finish date."""
        # if no projetc is given, return 1987-15-10
        # if not is_project(project):
        if not self.is_project(project):
            return ddate(1987, 10, 15)

        # get time needed for this offer
        time = self.get_time_total()

        # get initial date
        date = self._date

        # get first workday
        while date.weekday() not in project.get_work_days():
            date += timedelta(days=1)

        # add minimum_days
        min_days = project.get_minimum_days()
        while min_days > 0:
            # add the day only, if it is a working day
            if date.weekday() in project.get_work_days():
                min_days -= 1

            # add a day
            date += timedelta(days=1)

        # subtract hours_per_day from time on work_days, till time <= 0
        while time > 0:
            # t's a work day so subtract hours_per_day from time
            if date.weekday() in project.get_work_days():
                time -= project.get_hours_per_day()

            # add a day
            date += timedelta(days=1)

        return date

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
