"""The class holding informatin about the project."""

import json


class Project(object):
    """This class holds and project information."""

    def __init__(
        self,
        client_id=None,
        client_list=None,
        title=None,
        project_list=None,
        hours_per_day=None,
        work_days=None,
        minimum_days=None,
        offer_list=None
    ):
        """Initialize the class."""
        self._client_id = ''                        # set default
        self.set_client_id(client_id, client_list)  # tr to set argument
        self._title = ''                            # set default
        self.set_title(title, project_list)         # try to set argument
        self._hours_per_day = 4                     # set default
        self.set_hours_per_day(hours_per_day)       # try to set argument
        self._work_days = [0, 1, 2, 3, 4]           # set default
        self.set_work_days(work_days)               # try to set argument
        self._minimum_days = 2                      # set default
        self.set_minimum_days(minimum_days)         # try to set argument
        self._offer_list = []                       # set default
        self.set_offer_list(offer_list)             # try to set argument

    def set_title(self, value, project_list=None):
        """Try to set title list, if it's not already in the project_list."""
        done = False
        if type(project_list) is list:
            if not str(value) in [t.get_title() for t in project_list]:
                self._title = str(value)
                done = True
        return done

    def get_title(self):
        """Get title."""
        return self._title

    def set_client_id(self, value, client_list=None):
        """Try to set client_id, if it's in the client_list."""
        done = False
        if type(client_list) is list:
            if str(value) in [i.get_client_id() for i in client_list]:
                self._client_id = str(value)
                done = True
        return done

    def get_client_id(self):
        """Get client_id."""
        return self._client_id

    def set_offer_list(self, value):
        """Set offer_list."""
        # is list for working and dict while loading
        if type(value) is list:
            self._offer_list = value

    def get_offer_list(self):
        """Get offer_list."""
        return self._offer_list

    def append_offer(self, value):
        """Add offer to the offer_list."""
        if type(self._offer_list) is list:
            print('Added:', value)
            self._offer_list.append(value)

    def pop_offer(self, index):
        """Pop offer with the given index from list."""
        if type(self._offer_list) is list:
            self._offer_list.pop(index)

    def move_offer(self, offer_index=None, new_index=None):
        """Move an offer with offer_index in entry_list up/down."""
        if offer_index is None or new_index is None:
            return

        # only go on, if entry_list is a list
        if type(self._offer_list) is not list:
            return

        # cancel, if offer_index is out of range
        if offer_index >= len(self._offer_list):
            return

        # calculate new index: move up (new_index == 1) or down (new_index == -1)
        new_index = offer_index + new_index

        # put at beginning, if it's at the end and it's moved up
        if new_index >= len(self._offer_list):
            new_index = 0

        # put at the end, if it's at the beginning and moved down
        if new_index < 0:
            new_index = len(self._offer_list) - 1

        # move it!
        self._offer_list.insert(new_index, self._offer_list.pop(offer_index))

    def get_project_id(self):
        """Generate id with [client_id]_[title]."""
        return self.get_client_id() + '_' + self.get_title()

    def get_hours_per_day(self):
        """Get hours_per_day."""
        return self._hours_per_day

    def set_hours_per_day(self, value):
        """Set hours_per_day."""
        try:
            self._hours_per_day = int(value)
        except Exception:
            pass

    def get_work_days(self):
        """Get work_days."""
        return self._work_days

    def set_work_days(self, value):
        """Set work_days."""
        try:
            converter = []
            # value has to be list holding integers
            for x in value:
                converter.append(int(x))

            self._work_days = converter
        except Exception:
            pass

    def get_minimum_days(self):
        """Get minimum_days."""
        return self._minimum_days

    def set_minimum_days(self, value):
        """Set minimum_days."""
        try:
            self._minimum_days = int(value)
        except Exception:
            pass

    def to_json(self, indent=2):
        """Convert variables data to json format."""
        out = {}

        # fetch the variables
        out['type'] = self.__class__.__name__
        out['client_id'] = self.get_client_id()
        out['title'] = self.get_title()
        out['hours_per_day'] = self._hours_per_day
        out['work_days'] = self._work_days
        out['minimum_days'] = self._minimum_days

        # fetch the jsons from the entries
        out['offer_list'] = []
        for offer in self.get_offer_list():
            try:
                out['offer_list'].append(offer.to_json(indent=indent))
            except Exception:
                out['offer_list'].append(offer)

        # return the json
        return json.dumps(out, indent=indent, sort_keys=True)

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
