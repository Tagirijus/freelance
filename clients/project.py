"""
The class holding informatin about the project and the project_list.

The classes do not have privat values and setter and getter methods!
"""

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
        offer_list=None
    ):
        """Initialize the class."""
        self.client_id = 'no_id' if client_id is None else str(client_id)
        self.title = '' if title is None else str(title)
        self.hours_per_day = 4 if hours_per_day is None else hours_per_day
        self.work_days = [0, 1, 2, 3, 4] if work_days is None else work_days
        self.minimum_days = 2 if minimum_days is None else minimum_days
        self.offer_list = [] if offer_list is None else offer_list

    def append_offer(self, offer=None):
        """Append offer to project."""
        if type(offer) is Offer:
            self.offer_list.append(offer)

    def pop_offer(self, index=None):
        """Pop offer from project."""
        try:
            self.offer_list.pop(index)
        except Exception:
            pass

    def move_offer(self, offer_index=None, direction=None):
        """Move an offer with offer_index in entry_list up/down."""
        one_not_set = offer_index is None or direction is None
        out_of_range = offer_index >= len(self.offer_list)

        # cancel, if one argument is not set or offer_index is out of range
        if one_not_set or out_of_range:
            return

        # calculate new index: move up (direction == 1) or down (direction == -1)
        new_index = offer_index + direction

        # put at beginning, if it's at the end and it's moved up
        new_index = 0 if new_index >= len(self.offer_list) else new_index

        # put at the end, if it's at the beginning and moved down
        new_index = len(self.offer_list) - 1 if new_index < 0 else new_index

        # move it!
        self.offer_list.insert(new_index, self.offer_list.pop(offer_index))

    def project_id(self):
        """Generate id with [client_id]_[title]."""
        return self.client_id + '_' + self.title

    def to_dict(self):
        """Convert object to dict."""
        out = {}

        # fetch the variables
        out['type'] = self.__class__.__name__
        out['client_id'] = self.client_id
        out['title'] = self.title
        out['hours_per_day'] = self.hours_per_day
        out['work_days'] = self.work_days
        out['minimum_days'] = self.minimum_days

        # fetch the jsons from the entries
        out['offer_list'] = []
        for offer in self.offer_list:
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

        if 'offer_list' in js.keys():
            offer_list = js['offer_list']
        else:
            offer_list = None

        # return new object
        return cls(
            client_id=client_id,
            title=title,
            hours_per_day=hours_per_day,
            work_days=work_days,
            minimum_days=minimum_days,
            offer_list=offer_list
        )

    def copy(self):
        """Return copy of own object as new object."""
        return Project().from_json(js=self.to_json())
