"""The class holding informatin about the project."""

class Project(object):
    """This class holds and project information."""

    def __init__(
        self,
        client_id='',
        title='',
        hours_per_day=4,
        work_days=[0, 1, 2, 3, 4],
        minimum_days=2
    ):
        """Initialize the class."""
        self.client_id = str(client_id)
        self.title = str(title)
        self._hours_per_day = 4                 # set default
        self.set_hours_per_day(hours_per_day)   # try to set argument
        self._work_days = [0, 1, 2, 3, 4]       # set default
        self.set_work_days(work_days)           # try to set argument
        self._minimum_days = 2                  # set default
        self.set_minimum_days(minimum_days)     # try to set argument

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

        # fetch teh variables
        out['client_id'] = self.client_id
        out['title'] = self.title
        out['hours_per_day'] = self._hours_per_day
        out['work_days'] = self._work_days
        out['minimum_days'] = self._minimum_days

        # return the json
        return json.dumps(out, indent=indent, sort_keys=True)

    @classmethod
    def from_json(cls, js=None):
        """Convert all data from json format."""
        if js is None:
            return cls()

        # get js as dict
        try:
            js = json.loads(js)
        except Exception:
            # return default object
            return cls()

        # create object from variables
        if 'client_id' in js.keys():
            client_id = js['client_id']

        if 'title' in js.keys():
            title = js['title']

        if 'hours_per_day' in js.keys():
            hours_per_day = js['hours_per_day']

        if 'work_days' in js.keys():
            work_days = js['work_days']

        if 'minimum_days' in js.keys():
            minimum_days = js['minimum_days']

        # return new object
        return cls(
            client_id=client_id,
            title=title,
            hours_per_day=hours_per_day,
            work_days=work_days,
            minimum_days=minimum_days
        )
