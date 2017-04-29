"""
The class holding informatin about the project and the project_list.

The classes do not have privat values and setter and getter methods!
"""

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
        if offer_index is None or direction is None:
            return

        # cancel, if offer_index is out of range
        if offer_index >= len(self.offer_list):
            return

        # calculate new index: move up (direction == 1) or down (direction == -1)
        new_index = offer_index + direction

        # put at beginning, if it's at the end and it's moved up
        if new_index >= len(self.offer_list):
            new_index = 0

        # put at the end, if it's at the beginning and moved down
        if new_index < 0:
            new_index = len(self.offer_list) - 1

        # move it!
        self.offer_list.insert(new_index, self.offer_list.pop(offer_index))

    @property
    def project_id(self):
        """Generate id with [client_id]_[title]."""
        return self.client_id + '_' + self.title

    def to_json(self, indent=2):
        """Convert variables data to json format."""
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
        if data_path is None or not os.path.isdir(data_path):
            raise IOError
        self.data_path = data_path
        self.project_list = (self.load_from_file() if project_list is None
                             else project_list)

    def append(self, project=None):
        """Append a project, if its id does not exists already."""
        if type(project) is not Project:
            return

        # check if ID does not exist and append it only then
        if not project.project_id in self.get_all_ids():
            self.project_list.append(project)

    def pop(self, index):
        """Pop client with the given index from list."""
        try:
            self.project_list.pop(index)
        except Exception:
            pass

    def get_all_ids(self):
        """Get all project IDs."""
        return [project_id.project_id for project_id in self.project_list]

    def load_offer_from_json(self, js=None):
        """Load a Offer object from json string."""
        # if no js is given, return default Offer object
        if type(js) is None:
            return Offer()

        # generate main object
        out = Offer().from_json(js=js)

        # important: convert entry_list entries to correct entry objects
        correct_entries = []
        for entry in out.entry_list:
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
        out.entry_list = correct_entries

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
            filename = data_path + '/projects/' + project.project_id + '.flproject'
            filename_bu = (data_path + '/projects/' + project.project_id +
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
                for entry in tmp.offer_list:
                    js_tmp = json.loads(entry)
                    # check the type for the entry
                    if 'type' in js_tmp.keys():
                        # it is an Offer object
                        if js_tmp['type'] == 'Offer':
                            correct_entries.append(self.load_offer_from_json(js=js_tmp))

                tmp.offer_list = correct_entries
                out.append(tmp)

        return out
