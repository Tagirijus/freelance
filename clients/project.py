"""The class holding informatin about the project and the project_list."""

import json
from offer.offer import Offer
from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry
import os
import shutil


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
        if project_list is None:
            self._title = str(value)
            return True
        if type(project_list) is list:
            if not str(value) in [t.get_title() for t in project_list]:
                self._title = str(value)
                return True
        return False

    def get_title(self):
        """Get title."""
        return self._title

    def set_client_id(self, value, client_list=None):
        """Try to set client_id, if it's in the client_list."""
        if client_list is None:
            self._client_id = str(value)
            return True
        if type(client_list) is list:
            if str(value) in [i.get_client_id() for i in client_list]:
                self._client_id = str(value)
                return True
        return False

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

    def append_offer(self, offer=None):
        """Add offer to the offer_list."""
        if type(offer) is not Offer:
            return

        self._offer_list.append(offer)

    def pop_offer(self, index):
        """Pop offer with the given index from list."""
        if index < len(self._offer_list):
            self._offer_list.pop(index)

    def move_offer(self, offer_index=None, direction=None):
        """Move an offer with offer_index in entry_list up/down."""
        if offer_index is None or direction is None:
            return

        # cancel, if offer_index is out of range
        if offer_index >= len(self._offer_list):
            return

        # calculate new index: move up (direction == 1) or down (direction == -1)
        new_index = offer_index + direction

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


class ProjectList(object):
    """The list holding the project objects."""

    def __init__(
        self,
        data_path=None,
        project_list=None
    ):
        """Initialize the class."""
        self.data_path = data_path
        self._project_list = self.load_from_file()
        self.set_project_list(project_list)

    def append(self, project=None):
        """Append a project, if its id does not exists already."""
        if type(project) is not Project:
            return

        # check if ID does not exist and append it only then
        if not project.get_project_id() in self.get_all_ids():
            self._project_list.append(project)

    def pop(self, index):
        """Pop client with the given index from list."""
        if index < len(self._project_list):
            self._project_list.pop(index)

    def move(self, entry_index=None, direction=None):
        """Move an entry with entry_index in client_list up/down."""
        if entry_index is None or direction is None:
            return

        # cancel, if entry_index is out of range
        if entry_index >= len(self._project_list):
            return

        # calculate new index: move up (direction == 1) or down (direction == -1)
        new_index = entry_index + direction

        # put at beginning, if it's at the end and it's moved up
        if new_index >= len(self._project_list):
            new_index = 0

        # put at the end, if it's at the beginning and moved down
        if new_index < 0:
            new_index = len(self._project_list) - 1

        # move it!
        self._project_list.insert(new_index, self._project_list.pop(entry_index))

    def get_all_ids(self):
        """Get all project IDs."""
        return [project_id.get_project_id() for project_id in self._project_list]

    def set_project_list(self, project_list=None):
        """Try to set project list."""
        if type(project_list) is list:
            # each type inside list has to be Project object
            for i in project_list:
                if type(i) is not Project:
                    return

            # done and correct, set it
            self._project_list = project_list

    def get_project_list(self):
        """Get the project list."""
        return self._project_list

    def load_offer_from_json(self, js=None):
        """Load a Offer object from json string."""
        # if no js is given, return default Offer object
        if type(js) is None:
            return Offer()

        # generate main object
        out = Offer().from_json(js=js)

        # important: convert entry_list entries to correct entry objects
        correct_entries = []
        for entry in out.get_entry_list():
            js_tmp = json.loads(entry)
            # check the type for the entry
            if 'type' in js_tmp.keys():
                # it's BaseEntry - convert it from json and append it
                if js_tmp['type'] == 'BaseEntry':
                    correct_entries.append(BaseEntry().from_json(js=js_tmp))

                # it's MultiplyEntry - convert it from json and append it
                if js_tmp['type'] == 'MultiplyEntry':
                    correct_entries.append(MultiplyEntry().from_json(js=js_tmp))

                # it's ConnectEntry - convert it from json and append it
                if js_tmp['type'] == 'ConnectEntry':
                    correct_entries.append(ConnectEntry().from_json(js=js_tmp))
        out.set_entry_list(correct_entries)

        return out

    def save_to_file(self, data_path=None):
        """
        Save projects from project_list.

        Save it to [data_path]/projects/[project_id].flproject.
        """
        if data_path is None:
            if self.data_path is None:
                return False
            else:
                data_path = self.data_path

        # check if project directory exists and create one if needed
        if not os.path.isdir(data_path + '/projects'):
            os.mkdir(data_path + '/projects')

        # cycle through projects and save each project into its own file
        for project in self.get_project_list():
            # cancel this entry, if it's no Project object
            if type(project) is not Project:
                continue

            # generate filenames
            filename = data_path + '/projects/' + project.get_project_id() + '.flproject'
            filename_bu = (data_path + '/projects/' + project.get_project_id() +
                           '.flproject_bu')

            # if it already exists, save a backup
            if os.path.isfile(filename):
                shutil.copy2(filename, filename_bu)

            # write the file
            f = open(filename, 'w')
            f.write(project.to_json())
            f.close()
        return True

    def load_from_file(self, data_path=None):
        """Load the projects files and return project list."""
        # if no js is given, return default Project object
        if data_path is None:
            if self.data_path is None:
                return []
            else:
                data_path = self.data_path

        # cycle through the files and append them converted from json to the list
        out = []

        path = data_path + '/projects/'

        # check if the data_path/clients directory exists and cancel otherwise
        if not os.path.isdir(path):
            return []

        for file in sorted(os.listdir(path)):
            if file.endswith('.flproject'):
                # load the file
                f = open(path + file, 'r')
                load = f.read()
                f.close()

                # generate main object
                tmp = Project().from_json(js=load)

                # important: convert entry_list entries to correct entry objects
                correct_entries = []
                for entry in tmp.get_offer_list():
                    js_tmp = json.loads(entry)
                    # check the type for the entry
                    if 'type' in js_tmp.keys():
                        # it is an Offer object
                        if js_tmp['type'] == 'Offer':
                            correct_entries.append(self.load_offer_from_json(js=js_tmp))

                tmp.set_offer_list(correct_entries)
                out.append(tmp)

        return out
