"""
The class holding informatin about the project and the project_list.

The classes do not have privat values and setter and getter methods!
"""

from decimal import Decimal
import json
from offer.offer import Offer


class Project(object):
    """This class holds and project information."""

    def __init__(
        self,
        client_id=None,
        title=None,
        hours_per_day=None,
        work_days=None,
        minimum_days=None,
        wage=None,
        offer_list=None
    ):
        """Initialize the class."""
        self.client_id = 'no_id' if client_id is None else str(client_id)
        self.title = '' if title is None else str(title)
        self._hours_per_day = 4                 # set default
        self.set_hours_per_day(hours_per_day)   # try to set arguments value
        self._work_days = [0, 1, 2, 3, 4]       # set default
        self.set_work_days(work_days)           # try to set arguments value
        self._minimum_days = 2                  # set default
        self.set_minimum_days(minimum_days)     # try to set arguments value
        self._wage = Decimal('0.00')            # set default
        self.set_wage(wage)                     # try to set arguments value
        self._offer_list = []                   # set default
        self.set_offer_list(offer_list)         # try to set arguments value

    def set_hours_per_day(self, value):
        """Set hours_per_day."""
        try:
            self._hours_per_day = int(value)
        except Exception:
            pass

    def get_hours_per_day(self):
        """Get hours_per_day."""
        return self._hours_per_day

    def set_work_days(self, value):
        """Set work_days."""
        if type(value) is list:
            self._work_days = value

    def get_work_days(self):
        """Get work_days."""
        return self._work_days

    def set_minimum_days(self, value):
        """Set minimum_days."""
        try:
            self._minimum_days = int(value)
        except Exception:
            pass

    def get_minimum_days(self):
        """Get minimum_days."""
        return self._minimum_days

    def set_wage(self, value):
        """Set wage."""
        try:
            # only works if value is convertable to Decimal
            self._wage = Decimal(str(value))
        except Exception:
            pass

    def get_wage(self):
        """Get wage."""
        return self._wage

    def set_offer_list(self, value):
        """Set offer_list."""
        if type(value) is list:
            self._offer_list = value

    def get_offer_list(self):
        """Get offer_list."""
        return self._offer_list

    def append_offer(self, offer=None):
        """Append offer to project."""
        if type(offer) is Offer:
            self._offer_list.append(offer)

    def pop_offer(self, index=None):
        """Pop offer from project."""
        try:
            self._offer_list.pop(index)
        except Exception:
            pass

    def project_id(self, title=None):
        """Generate id with [client_id]_[title]."""
        if title is None:
            return self.client_id + '_' + self.title
        else:
            return self.client_id + '_' + title

    def to_dict(self):
        """Convert object to dict."""
        out = {}

        # fetch the variables
        out['type'] = self.__class__.__name__
        out['client_id'] = self.client_id
        out['title'] = self.title
        out['hours_per_day'] = self._hours_per_day
        out['work_days'] = self._work_days
        out['wage'] = float(self._wage)
        out['minimum_days'] = self._minimum_days

        # fetch the jsons from the entries
        out['offer_list'] = []
        for offer in self._offer_list:
            try:
                out['offer_list'].append(offer.to_dict())
            except Exception:
                out['offer_list'].append(offer)

        return out

    def to_json(self, indent=2, ensure_ascii=False):
        """Convert variables data to json format."""
        return json.dumps(
            self.to_dict(),
            indent=indent,
            ensure_ascii=ensure_ascii,
            sort_keys=True
        )

    def load_offer_list_from_js(self, lis=None):
        """Convert list to offer object list."""
        offer_list = []
        # cycle through the list of dicts
        for offer in lis:
            # it should have a type key
            if 'type' in offer.keys():
                # this type key should be "Offer"
                if offer['type'] == 'Offer':
                    # convert this dict to an offer objetc then!
                    offer_list.append(Offer().from_json(
                        js=offer
                    ))

        return offer_list

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

        # create object from variables
        if 'client_id' in js.keys():
            client_id = js['client_id']
        else:
            client_id = None

        if 'title' in js.keys():
            title = js['title']
        else:
            title = None

        if 'hours_per_day' in js.keys():
            hours_per_day = js['hours_per_day']
        else:
            hours_per_day = None

        if 'work_days' in js.keys():
            work_days = js['work_days']
        else:
            work_days = None

        if 'minimum_days' in js.keys():
            minimum_days = js['minimum_days']
        else:
            minimum_days = None

        if 'wage' in js.keys():
            wage = js['wage']
        else:
            wage = None

        if 'offer_list' in js.keys():
            offer_list = js['offer_list']
            offer_list = cls().load_offer_list_from_js(lis=offer_list)
        else:
            offer_list = None

        # return new object
        return cls(
            client_id=client_id,
            title=title,
            hours_per_day=hours_per_day,
            work_days=work_days,
            minimum_days=minimum_days,
            wage=wage,
            offer_list=offer_list
        )

    def copy(self):
        """Return copy of own object as new object."""
        return Project().from_json(js=self.to_json())

    def i_am_project(self, project=None):
        """
        Check if given argument is project object.

        This is some kind of workaround, since I canot import the Project class
        into Offer module due to circular dependencies. Do I really still have
        a that bad programm manufacture? )=
        """
        return True
