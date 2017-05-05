"""
Global list holding clients and projects.

This class can set the client_id, while it keeps being unique. Same
for the project_title, while it keeps beeing unique according to the
project_id.
"""

from clients.client import Client
from clients.project import Project
from general.settings import Settings
import json
from offer.offer import Offer
from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry
import os
import shutil


def get_inactive_list(settings=None):
    """Get inactive clients and projects and return it into new list."""
    if type(settings) is Settings:
        data_path = settings.data_path
        client_dir = '/clients' + settings.inactive_dir
        project_dir = '/projects' + settings.inactive_dir
        return List(
            data_path=data_path,
            client_dir=client_dir,
            project_dir=project_dir
        )


def activate_project(
    active_list=None,
    inactive_list=None,
    inactive_project=None
):
    """Activate the project."""
    are_lists = type(active_list) is List and type(inactive_list) is List
    is_project = type(inactive_project) is Project

    if not are_lists and not is_project:
        return False

    active_list.add_project(project=inactive_project.copy())
    inactive_list.remove_project(project=inactive_project)
    return True


def us(string=''):
    """Return string with underscores instead of whitespace."""
    return string.replace(' ', '_')


class List(object):
    """List holding clients and projects."""

    def __init__(
        self,
        data_path=None,
        client_dir='/clients',
        client_list=None,
        project_dir='/projects',
        project_list=None
    ):
        """Initialize the class."""
        self.data_path = data_path

        is_dir = os.path.isdir(str(self.data_path))
        if not is_dir:
            raise IOError

        self.client_dir = client_dir
        self.client_list = (self.load_client_list_from_file() if client_list is None
                            else client_list)

        self.project_dir = project_dir
        self.project_list = (self.load_project_list_from_file() if project_list is None
                             else project_list)

    def add_client(self, client=None):
        """Add a client, if its ID does not already exist."""
        is_client = type(client) is Client
        id_exists = client.client_id in [c.client_id for c in self.client_list]

        # cancel if it's no client or the client_id already exists
        if not is_client or id_exists:
            return False

        # append the client and save it immediately
        self.client_list.append(client)
        self.save_client_to_file(client=client)

        return True

    def remove_client(self, client=None):
        """Remove client, if it exists (according to its ID)."""
        is_client = type(client) is Client
        id_exists = client.client_id in [c.client_id for c in self.client_list]

        # cancel if it's not client or the client_id does NOT exist
        if not is_client or not id_exists:
            return False

        # try to remove the client and its projects
        try:
            # first delete attached projects
            for p in self.get_client_projects(client=client):
                self.project_list.pop(self.project_list.index(p))
                self.delete_project_file(project=p)

            # then delete the client itself
            self.client_list.pop(self.client_list.index(client))
            self.delete_client_file(client=client)
            return True
        except Exception:
            return False

    def deactivate_client(self, client=None, inactive_dir=None):
        """Pop client and move its file to the inactive dir."""
        # create absolute path to deactivated_dir and working dir
        path_deact = self.data_path + self.client_dir + str(inactive_dir)
        path = self.data_path + self.client_dir

        # check arguments and directory
        one_not_set = client is None or inactive_dir is None
        is_client = type(client) is Client
        is_dir = os.path.isdir(path_deact)

        # cancel if one argument is not set or client isn't Client
        if one_not_set or not is_client:
            return False

        # first all the clients projects
        for p in self.get_client_projects(client=client):
            self.deactivate_project(
                project=p,
                inactive_dir=inactive_dir
            )

        # and now the client itself !!!
        # create dir if it does not exist
        if not is_dir:
            os.mkdir(path_deact)

        # generate filenames
        filename_old = path + '/' + client.client_id + '.flclient'
        filename_new = path_deact + '/' + client.client_id + '.flclient'
        filename_new_bu = path_deact + '/' + client.client_id + '.flclient_bu'

        # if it already exists, save a backup
        if os.path.isfile(filename_new):
            shutil.copy2(filename_new, filename_new_bu)

        # move the old file to the inactive directory and pop variable from list
        try:
            shutil.move(filename_old, filename_new)
            self.client_list.pop(self.client_list.index(client))
        except Exception:
            return False

        return True

    def set_client_id(self, client=None, client_id=None):
        """Try to set new client ID for client and its projects."""
        is_client = type(client) is Client
        id_exists = client_id in [c.client_id for c in self.client_list]

        # cancel if it's no client or the client_id does already exist
        if not is_client or id_exists:
            return False

        # change every client_id of the projects of the original client
        for p in self.get_client_projects(client=client):
            self.delete_project_file(project=p)
            p.client_id = client_id
            self.save_project_to_file(project=p)

        # change the client_id of the original client_id
        self.delete_client_file(client=client)
        self.client_list[self.client_list.index(client)].client_id = client_id
        self.save_client_to_file(client=client)

        return True

    def get_client_projects(self, client=None):
        """Return list with projects for given client."""
        if type(client) is Client:
            return [p for p in self.project_list if client.client_id == p.client_id]

    def add_project(self, project=None):
        """Add a project, if its ID does not already exist and the client exist."""
        is_project = type(project) is Project
        id_exists = project.client_id in [c.client_id for c in self.client_list]
        pid_exists = project.project_id() in [p.project_id() for p in self.project_list]

        # cancel if it's no project or the client_id does not exist
        #   or the project_id already exists
        if not is_project or not id_exists or pid_exists:
            return False

        # add the project
        self.project_list.append(project)
        self.save_project_to_file(project=project)
        return True

    def remove_project(self, project=None):
        """Remove project, if it exists (according to its ID)."""
        is_project = type(project) is Project
        pid_exists = project.project_id() in [p.project_id() for p in self.project_list]

        # cancel if it's no project or project_id does not exist
        if not is_project or not pid_exists:
            return False

        # try to remove the project
        try:
            self.project_list.pop(self.project_list.index(project))
            self.delete_project_file(project=project)
            return True
        except Exception:
            return False

    def deactivate_project(self, project=None, inactive_dir=None):
        """Pop project and move its file to the inactive dir."""
        # create absolute path to deactivated_dir and working dir
        path_deact = self.data_path + self.project_dir + str(inactive_dir)
        path = self.data_path + self.project_dir

        # check arguments and directory
        one_not_set = project is None or inactive_dir is None
        is_project = type(project) is Project
        is_dir = os.path.isdir(path_deact)

        # cancel if one argument is not set or project isn't Project
        if one_not_set or not is_project:
            return False

        # create dir if it does not exist
        if not is_dir:
            os.mkdir(path_deact)

        # generate filenames
        filename_old = path + '/' + project.project_id() + '.flproject'
        filename_new = path_deact + '/' + project.project_id() + '.flproject'
        filename_new_bu = path_deact + '/' + project.project_id() + '.flproject_bu'

        # if it already exists, save a backup
        if os.path.isfile(filename_new):
            shutil.copy2(filename_new, filename_new_bu)

        # move the old file to the inactive directory and pop variable from list
        try:
            shutil.move(filename_old, filename_new)
            self.project_list.pop(self.project_list.index(project))
        except Exception:
            return False

        return True

    def set_project_title(self, project=None, title=None):
        """Try to set new project title for project."""
        is_project = type(project) is Project
        title_exists = title in [p.title for p in self.project_list
                                 if p != project and project.client_id == p.client_id]

        # cancel if it's no project or title exists in clients other project-titles
        if not is_project or title_exists:
            return False

        # change the title
        self.delete_project_file(project=project)
        self.project_list[self.project_list.index(project)].title = title
        self.save_project_to_file(project=project)
        return True

    def assign_project_to_client(self, project=None, client_id=None):
        """Try to change the projects client_id."""
        is_project = type(project) is Project
        one_not_set = project is None or client_id is None
        client_exists = client_id in [c.client_id for c in self.client_list]
        client_is_self = client_id == project.client_id

        # cancel, if either:
        #   argument is not a project
        #   one argument not set
        #   client_id already exists
        #   client already assigned
        if not is_project or one_not_set or not client_exists or client_is_self:
            return False

        # assign the project to the new client
        self.delete_project_file(project=project)
        project.client_id = client_id
        self.save_project_to_file(project=project)
        return True

    def load_client_list_from_file(self):
        """Load the clients from file and return client_list."""
        path = self.data_path + self.client_dir

        # check if the data_path/clients directory exists and cancel otherwise
        if not os.path.isdir(str(path)):
            return []

        # cycle through the files and append them converted from json to the list
        out = []
        for file in sorted(os.listdir(path)):
            if file.endswith('.flclient'):
                # load the file
                f = open(path + '/' + file, 'r')
                load = f.read()
                f.close()

                # convert file content to Client object and append it
                out.append(Client().from_json(js=load))

        return out

    def load_project_list_from_file(self):
        """Load the projects files and return project list."""
        # cycle through the files and append them converted from json to the list
        out = []

        path = self.data_path + self.project_dir

        # check if the data_path/clients directory exists and cancel otherwise
        if not os.path.isdir(str(path)):
            return []

        for file in sorted(os.listdir(path)):
            if file.endswith('.flproject'):
                # load the file
                f = open(path + '/' + file, 'r')
                load = f.read()
                f.close()

                # generate main object
                tmp = Project().from_json(js=load)

                # important: convert entry_list entries to correct entry objects
                correct_entries = []
                for entry in tmp.offer_list:
                    if type(entry) is not dict:
                        js_tmp = json.loads(entry)
                    else:
                        js_tmp = entry
                    # check the type for the entry
                    if 'type' in js_tmp.keys():
                        # it is an Offer object
                        if js_tmp['type'] == 'Offer':
                            correct_entries.append(self.load_offer_from_json(js=js_tmp))

                tmp.offer_list = correct_entries
                out.append(tmp)

        return out

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
            if type(entry) is not dict:
                js_tmp = json.loads(entry)
            else:
                js_tmp = entry
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

    def delete_client_file(self, client=None):
        """Delete the file for this client."""
        if type(client) is not Client:
            return False

        path = self.data_path + self.client_dir

        # generate filenames
        filename = path + '/' + us(client.client_id) + '.flclient'

        # check if the file exists and delete it
        if os.path.isfile(filename):
            os.remove(filename)
            return True
        else:
            return False

    def save_client_to_file(self, client=None):
        """Save single client to file."""
        if type(client) is not Client:
            return False

        path = self.data_path + self.client_dir

        # create dir if it does not exist
        is_dir = os.path.isdir(str(path))
        is_file = os.path.isfile(str(path))
        if not is_dir and not is_file:
            os.mkdir(path)

        # generate filenames
        filename = path + '/' + us(client.client_id) + '.flclient'
        filename_bu = path + '/' + us(client.client_id) + '.flclient_bu'

        # if it already exists, save a backup
        if os.path.isfile(filename):
            shutil.copy2(filename, filename_bu)

        # write the file
        f = open(filename, 'w')
        f.write(client.to_json())
        f.close()

        return True

    def save_client_list_to_file(self):
        """Save clients from client_list to [data_path]/clients/[client_id].flclient."""
        # cycle through clients and save each client into its own file
        for client in self.client_list:
            self.save_client_to_file(client=client)

    def delete_project_file(self, project=None):
        """Delete the file for this project."""
        if type(project) is not Project:
            return False

        path = self.data_path + self.project_dir

        # generate filenames
        filename = path + '/' + us(project.project_id()) + '.flproject'

        # check if the file exists and delete it
        if os.path.isfile(filename):
            os.remove(filename)
            return True
        else:
            return False

    def save_project_to_file(self, project=None):
        """Save single project to file."""
        if type(project) is not Project:
            return False

        path = self.data_path + self.project_dir

        # create dir if it does not exist
        is_dir = os.path.isdir(str(path))
        is_file = os.path.isfile(str(path))
        if not is_dir and not is_file:
            os.mkdir(path)

        # generate filenames
        filename = path + '/' + us(project.project_id()) + '.flproject'
        filename_bu = path + '/' + us(project.project_id()) + '.flproject_bu'

        # if it already exists, save a backup
        if os.path.isfile(filename):
            shutil.copy2(filename, filename_bu)

        # write the file
        f = open(filename, 'w')
        f.write(project.to_json())
        f.close()

    def save_project_list_to_file(self):
        """
        Save projects from project_list.

        Save it to [data_path]/projects/[project_id].flproject.
        """
        # cycle through projects and save each project into its own file
        for project in self.project_list:
            self.save_project_to_file(project=project)

    def save_all(self):
        """Save all the lists."""
        self.save_client_list_to_file()
        self.save_project_list_to_file()

    def copy(self):
        """Copy the own object and return it as a new one."""
        # get copy of client_list
        new_client_list = []

        for c in self.client_list:
            new_client_list.append(Client().from_json(js=c.to_json()))

        # get copy of project_list
        new_project_list = []

        for p in self.project_list:
            new_project_list.append(Project().from_json(js=p.to_json()))

        return List(
            data_path=self.data_path[:],
            client_dir=self.client_dir[:],
            client_list=new_client_list,
            project_dir=self.project_dir[:],
            project_list=new_project_list
        )

    def reload(self, data_path=None):
        """Reload the list."""
        is_dir = os.path.isdir(str(data_path))

        if not is_dir:
            raise IOError

        self.data_path = data_path
        self.client_list = self.load_client_list_from_file()
        self.project_list = self.load_project_list_from_file()