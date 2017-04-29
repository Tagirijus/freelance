"""
The class holds a list of entries.

The classes do not have privat values and setter and getter methods!
"""

from datetime import datetime
import json
from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry


class Offer(object):
    """A class holding a list of entries."""

    def __init__(
        self,
        title=None,
        project_id=None,
        date_fmt=None,
        date=None,
        entry_list=None
    ):
        """Initialize the class."""
        self.title = '' if title is None else str(title)
        self.project_id = '' if project_id is None else str(project_id)
        self.date_fmt = date_fmt
        self.date = datetime.now() if date is None else date
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

    def move(self, entry_index=None, direction=None):
        """Move an entry with entry_index in entry_list up/down."""
        if entry_index is None or direction is None:
            return

        # cancel, if entry_index is out of range
        if entry_index >= len(self.entry_list):
            return

        # calculate new index: move up (direction == 1) or down (direction == -1)
        new_index = entry_index + direction

        # put at beginning, if it's at the end and it's moved up
        if new_index >= len(self.entry_list):
            new_index = 0

        # put at the end, if it's at the beginning and moved down
        if new_index < 0:
            new_index = len(self.entry_list) - 1

        # move it!
        self.entry_list.insert(new_index, self.entry_list.pop(entry_index))

    def to_json(self, indent=2):
        """Convert variables data to json format."""
        out = {}

        # fetch the variables
        out['type'] = self.__class__.__name__
        out['title'] = self.title
        out['project_id'] = self.project_id
        out['date_fmt'] = self.date_fmt
        try:
            out['date'] = self.date.strftime('%Y-%m-%d')
        except Exception as e:
            out['date'] = datetime.now().strftime('%Y-%m-%d')

        # fetch the jsons from the entries
        out['entry_list'] = []
        for entry in self.entry_list:
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

        if 'project_id' in js.keys():
            project_id = js['project_id']
        else:
            project_id = None

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
            project_id=project_id,
            date_fmt=date_fmt,
            date=date,
            entry_list=entry_list
        )
