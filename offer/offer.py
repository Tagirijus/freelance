"""The class holds a list of entries."""

from datetime import datetime
import json


class Offer(object):
    """A class holding a list of entries."""

    def __init__(
        self,
        title='',
        number='1',
        date_fmt=None,
        date=None,
        entry_list=None
    ):
        """Initialize the class."""
        self.title = '' if title is None else str(title)
        self.number = '1' if number is None else str(number)
        self.date_fmt = date_fmt
        self._date = datetime.now()             # set default
        self.set_date(date, fmt=self.date_fmt)  # try to set argument
        self._entry_list = []                   # set default
        self.set_entry_list(entry_list)         # try to set argument

    def set_date(self, value, fmt=None):
        """Set the date."""
        # given value is a datetime object
        if type(value) is datetime:
            self._date = value

        # given value is string and fmt not given (guess it)
        elif type(value) is str and fmt is None:
            # try class date_fmt variable
            try:
                self._date = datetime.strptime(value, self.date_fmt)
            except Exception:
                pass

            # try '%Y-%m-%d' format
            try:
                self._date = datetime.strptime(value, '%Y-%m-%d')
            except Exception:
                pass

            # try '%d.%m.%Y' format
            try:
                self._date = datetime.strptime(value, '%d.%m.%Y')
            except Exception:
                pass

        # given value is string and fmt is given
        elif type(value) is str and type(fmt) is str:
            try:
                self._date = datetime.strptime(value, fmt)
            except Exception:
                pass

    def get_date(self):
        """Get date."""
        return self._date

    def set_entry_list(self, value):
        """Set entry_list."""
        # is list for working and dict while loading
        if type(value) is list:
            self._entry_list = value

    def get_entry_list(self):
        """Get entry_list."""
        return self._entry_list

    def append(self, value):
        """Add entry to the entry_list."""
        if type(self._entry_list) is list:
            print('Added:', value)
            self._entry_list.append(value)

    def pop(self, index):
        """Pop entry with the given index from list."""
        if type(self._entry_list) is list:
            self._entry_list.pop(index)

    def move(self, entry_index=None, new_index=None):
        """Move an entry with entry_id in entry_list up/down."""
        if entry_index is None or new_index is None:
            return

        # only go on, if entry_list is a list
        if type(self._entry_list) is not list:
            return

        # cancel, if entry_index is out of range
        if entry_index >= len(self._entry_list):
            return

        # calculate new index: move up (new_index == 1) or down (new_index == -1)
        new_index = entry_index + new_index

        # put at beginning, if it's at the end and it's moved up
        if new_index >= len(self._entry_list):
            new_index = 0

        # put at the end, if it's at the beginning and moved down
        if new_index < 0:
            new_index = len(self._entry_list) - 1

        # move it!
        self._entry_list.insert(new_index, self._entry_list.pop(entry_index))

    def to_json(self, indent=2):
        """Convert variables data to json format."""
        out = {}

        # fetch the variables
        out['type'] = self.__class__.__name__
        out['title'] = self.title
        out['number'] = self.number
        out['date_fmt'] = self.date_fmt
        out['date'] = self.get_date().strftime('%Y-%m-%d')

        # fetch the jsons from the entries
        out['entry_list'] = []
        for entry in self.get_entry_list():
            try:
                out['entry_list'].append(entry.to_json(indent=indent))
            except Exception:
                out['entry_list'].append(entry)

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

        # create object from json
        if 'title' in js.keys():
            title = js['title']
        else:
            title = None

        if 'number' in js.keys():
            number = js['number']
        else:
            number = None

        if 'date_fmt' in js.keys():
            date_fmt = js['date_fmt']
        else:
            date_fmt = None

        if 'date' in js.keys():
            try:
                date = datetime.strptime(js['date'], '%Y-%m-%d')
            except Exception:
                date = None
        else:
            date = None

        if 'entry_list' in js.keys():
            entry_list = js['entry_list']
        else:
            entry_list = None

        # return new object
        return cls(
            title=title,
            number=number,
            date_fmt=date_fmt,
            date=date,
            entry_list=entry_list
        )
