"""
Global list holding clients and projects.

This class can set the client_id, while it keeps being unique. Same
for the project_title, while it keeps beeing unique according to the
project_id.
"""

from clients.client import Client
from clients.project import Project
from general.settings import Settings
import os
import shutil


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

        self.inactive_list = None

    def client_exists(self, client=None):
        """Check if client exists according to the ID."""
        if type(client) is Client:
            return client.client_id in [c.client_id for c in self.client_list]
        else:
            return False

    def get_client_index(self, client=None):
        """Get the index of the client."""
        if type(client) is Client:
            for i, c in enumerate(self.client_list):
                if client.client_id == c.client_id:
                    return i

        return False

    def add_client(self, client=None, activate=False):
        """Add a client, if its ID does not already exist."""
        is_client = type(client) is Client
        id_exists = client.client_id in [c.client_id for c in self.client_list]
        id_exists_inactive = (
            self.inactive_list.client_exists(client)
            if not activate
            else False
        )
        id_is_empty = client.client_id == ''

        # cancel if it's no client or the client_id already exists or empty
        if not is_client or id_exists or id_exists_inactive or id_is_empty:
            return False

        # append the client and save it immediately
        self.client_list.append(client)
        self.save_client_to_file(client=client)

        return True

    def update_client(self, old_client=None, new_client=None):
        """Update old client with new client."""
        old_is_client = type(old_client) is Client
        new_is_client = type(new_client) is Client

        # cancel if these are no clients
        if not old_is_client and not new_is_client:
            return False

        # try to change the id (and its files) first
        old_index = self.get_client_index(old_client)
        id_available = self.set_client_id(
            client=old_client,
            client_id=new_client.client_id
        )

        # only go on, if the ID is possible
        if id_available:
            self.client_list[old_index] = new_client
            return True
        else:
            return False

    def set_client_id(self, client=None, client_id=None):
        """Try to set new client ID for client and its projects."""
        # cancel if its not a client object
        is_client = type(client) is Client

        if not is_client:
            return False

        # check id
        id_exists = client_id in [c.client_id for c in self.client_list]
        id_is_empty = client_id == ''
        id_is_own = client.client_id == client_id

        # cancel with true, if there's no need to change the ID
        if id_is_own:
            return True

        # cancel if it's no client or the client_id does already exist or is empty
        if id_exists or id_is_empty:
            return False

        # change every client_id of the projects of the original client
        for p in self.get_client_projects(client=client):
            # get old and new project
            old_p = p.copy()
            new_p = p.copy()
            new_p.client_id = client_id

            # set new projects client_id
            self.set_project_id(
                old_project=old_p,
                new_project=new_p
            )

        # rename the file
        self.rename_client_file(
            old_client_id=client.client_id,
            new_client_id=client_id
        )

        # get index
        index = self.get_client_index(client)

        # change the client_id of the original client to the new id
        self.client_list[index].client_id = client_id

        # get new client and save it
        self.save_client_to_file(client=self.client_list[index])

        return True

    def remove_client(self, client=None, settings=None):
        """Remove client, if it exists (according to its ID)."""
        is_client = type(client) is Client
        id_exists = client.client_id in [c.client_id for c in self.client_list]

        # cancel if it's not client or the client_id does NOT exist
        if not is_client or not id_exists:
            return False

        # try to remove the client and its projects
        try:
            # then delete the client itself
            self.client_list.pop(self.get_client_index(client))
            self.delete_client_file(client=client)

            # update the inactive_list
            self.update_inactive_list(settings=settings)

            return True
        except Exception:
            return False

    def deactivate_client(self, client=None, inactive_dir=None, settings=None):
        """Pop client and move its file to the inactive dir."""
        # create absolute path to deactivated_dir and working dir
        path = self.data_path + self.client_dir
        path_deact = path + str(inactive_dir)

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
        filename_old = path + '/' + self.us(client.client_id) + '.flclient'
        filename_old_bu = path + '/' + self.us(client.client_id) + '.flclient_bu'
        filename_new = path_deact + '/' + self.us(client.client_id) + '.flclient'
        filename_new_bu = path_deact + '/' + self.us(client.client_id) + '.flclient_bu'

        # move the old file to the inactive directory and pop variable from list
        try:
            # move original file
            shutil.move(filename_old, filename_new)

            # move backup only if it exists
            if os.path.isfile(filename_old_bu):
                shutil.move(filename_old_bu, filename_new_bu)

            # pop it from the list
            self.client_list.pop(self.get_client_index(client))

            # update the inactive_list
            self.update_inactive_list(settings=settings)

            return True
        except Exception:
            return False

    def activate_client(self, client=None, settings=None, inactive_list=None):
        """Add client and move its file from the inactive dir."""
        # cancel if no settings object is given
        if type(settings) is not Settings:
            return False

        # create absolute path to deactivated_dir and working dir
        path = self.data_path + self.client_dir
        path_deact = path + str(settings.inactive_dir)

        # check arguments and directory
        one_not_set = client is None or settings is None or inactive_list is None
        is_client = type(client) is Client
        is_dir = os.path.isdir(path_deact)

        # cancel if one argument is not set or client isn't Client, or dir not exists
        if one_not_set or not is_client or not is_dir:
            return False

        # generate filenames
        filename_old = path_deact + '/' + self.us(client.client_id) + '.flclient'
        filename_old_bu = path_deact + '/' + self.us(client.client_id) + '.flclient_bu'
        filename_new = path + '/' + self.us(client.client_id) + '.flclient'
        filename_new_bu = path + '/' + self.us(client.client_id) + '.flclient_bu'

        # move the old file to the inactive directory and add variable to list
        try:
            # check if the language exists and adjust it, if not
            if client.language not in settings.get_languages():
                client.language = 'en'

            # add client to the active list
            added = self.add_client(client=client, activate=True)

            # cancel if it did not work
            if not added:
                return False

            # remove client form inactive list
            inactive_list.client_list.pop(inactive_list.get_client_index(client))

            # move original file
            shutil.move(filename_old, filename_new)

            # move backup only if it exists
            if os.path.isfile(filename_old_bu):
                shutil.move(filename_old_bu, filename_new_bu)

            # update the inactive_list
            self.update_inactive_list(settings=settings)

            return True
        except Exception:
            return False

    def get_client_projects(self, client=None):
        """Return list with projects for given client."""
        if type(client) is Client:
            return [p for p in self.project_list if client.client_id == p.client_id]

    def get_client_by_id(self, client_id=None):
        """Return client object according to found client_id."""
        # search client_id in list and return the client object
        for client in self.client_list:
            if client_id == client.client_id:
                return client.copy()

        # return empty client otherwise
        return Client()

    def get_project_index(self, project=None):
        """Get the index of the project."""
        if type(project) is Project:
            for i, p in enumerate(self.project_list):
                if project.project_id() == p.project_id():
                    return i

        return False

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

    def remove_project(self, project=None, settings=None):
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

            # update the inactive_list
            self.update_inactive_list(settings=settings)

            return True
        except Exception:
            return False

    def deactivate_project(self, project=None, inactive_dir=None, settings=None):
        """Pop project and move its file to the inactive dir."""
        # create absolute path to deactivated_dir and working dir
        path = self.data_path + self.project_dir
        path_deact = path + str(inactive_dir)

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
        filename_old = path + '/' + self.us(project.project_id()) + '.flproject'
        filename_old_bu = path + '/' + self.us(project.project_id()) + '.flproject_bu'
        filename_new = path_deact + '/' + self.us(project.project_id()) + '.flproject'
        filename_new_bu = (
            path_deact + '/' + self.us(project.project_id()) + '.flproject_bu'
        )

        # move the old file to the inactive directory and pop variable from list
        try:
            # move original file
            shutil.move(filename_old, filename_new)

            # move backup only, if it exists
            if os.path.isfile(filename_old_bu):
                shutil.move(filename_old_bu, filename_new_bu)

            # pop it from list
            self.project_list.pop(self.project_list.index(project))

            # update the inactive_list
            self.update_inactive_list(settings=settings)

            return True
        except Exception:
            return False

    def activate_project(self, project=None, settings=None, inactive_list=None):
        """Add project and move its file from the inactive dir."""
        # cancel if no settings object is given
        if type(settings) is not Settings:
            return False

        # create absolute path to deactivated_dir and working dir
        path = self.data_path + self.project_dir
        path_deact = path + str(settings.inactive_dir)

        # check arguments and directory
        one_not_set = project is None or settings is None or inactive_list is None
        is_project = type(project) is Project
        is_dir = os.path.isdir(path_deact)

        # cancel if one argument is not set or project isn't Project, or dir not exists
        if one_not_set or not is_project or not is_dir:
            return False

        # generate filenames
        filename_old = path_deact + '/' + self.us(project.project_id()) + '.flproject'
        filename_old_bu = (
            path_deact + '/' + self.us(project.project_id()) + '.flproject_bu'
        )
        filename_new = path + '/' + self.us(project.project_id()) + '.flproject'
        filename_new_bu = path + '/' + self.us(project.project_id()) + '.flproject_bu'

        # move the old file to the inactive directory and add variable to list
        try:
            # add project to the active list
            added = self.add_project(project=project)

            # cancel if it did not work
            if not added:
                return False

            # remove project form inactive list
            inactive_list.project_list.pop(inactive_list.get_project_index(project))

            # move original file
            shutil.move(filename_old, filename_new)

            # move backup only if it exists
            if os.path.isfile(filename_old_bu):
                shutil.move(filename_old_bu, filename_new_bu)

            # update the inactive_list
            self.update_inactive_list(settings=settings)

            return True
        except Exception:
            return False

    def update_project(self, old_project=None, new_project=None):
        """Update old project with new project."""
        old_is_project = type(old_project) is Project
        new_is_project = type(new_project) is Project

        # cancel if these are no project
        if not old_is_project and not new_is_project:
            return False

        # try to change the title + client_id (and its files) first
        old_index = self.get_project_index(old_project)
        id_available = self.set_project_id(
            old_project=old_project,
            new_project=new_project
        )

        # only go on change remaining, if the title is possible
        if id_available:
            self.project_list[old_index] = new_project
            return True
        else:
            return False

    def set_project_id(self, old_project=None, new_project=None):
        """Try to set new project title for project."""
        # cancel if one is no project object
        old_is_project = type(old_project) is Project
        new_is_project = type(new_project) is Project

        if not old_is_project or not new_is_project:
            return False

        # check id
        id_exists = new_project.project_id() in [
            p.project_id() for p in self.project_list
        ]
        id_is_own = old_project.project_id() == new_project.project_id()
        title_is_empty = new_project.title == ''

        # cancel with true, if there's no need to change the title + client_id
        if id_is_own:
            return True

        # cancel
        #   the id already exists
        #   or the new title is empty
        if id_exists or title_is_empty:
            return False

        # rename the file
        renamed = self.rename_project_file(
            old_project=old_project,
            new_project=new_project
        )

        if renamed is False:
            return False

        # get its index
        index = self.get_project_index(old_project)

        # change the title and client of the original project to the new title
        self.project_list[index].client_id = new_project.client_id
        self.project_list[index].title = new_project.title

        # get new project and save it
        self.save_project_to_file(project=self.project_list[index])

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
                out.append(Project().from_json(js=load))

        return out

    def delete_client_file(self, client=None):
        """Delete the file for this client."""
        if type(client) is not Client:
            return False

        path = self.data_path + self.client_dir

        # generate filenames
        filename = path + '/' + self.us(client.client_id) + '.flclient'

        # check if the file exists and delete it
        if os.path.isfile(filename):
            os.remove(filename)
            return True
        else:
            return False

    def rename_client_file(self, old_client_id=None, new_client_id=None):
        """Rename client file (its ID) to new clients ID."""
        one_not_set = old_client_id is None or new_client_id is None

        # cancel if arguments are not clients
        if one_not_set:
            return False

        # generate filenames
        path = self.data_path + self.client_dir
        filename = path + '/' + self.us(old_client_id) + '.flclient'
        filename_bu = path + '/' + self.us(old_client_id) + '.flclient_bu'
        filename_new = path + '/' + self.us(new_client_id) + '.flclient'
        filename_new_bu = path + '/' + self.us(new_client_id) + '.flclient_bu'

        # check if the files exist and rename them
        if os.path.isfile(filename):
            os.rename(filename, filename_new)

        if os.path.isfile(filename_bu):
            os.rename(filename_bu, filename_new_bu)

        return True

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
        filename = path + '/' + self.us(client.client_id) + '.flclient'
        filename_bu = path + '/' + self.us(client.client_id) + '.flclient_bu'

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
        filename = path + '/' + self.us(project.project_id()) + '.flproject'

        # check if the file exists and delete it
        if os.path.isfile(filename):
            os.remove(filename)
            return True
        else:
            return False

    def rename_project_file(self, old_project=None, new_project=None):
        """Rename project file (its ID) to new projects ID."""
        old_is_project = type(old_project) is Project
        new_is_project = type(new_project) is Project

        # cancel if arguments are not projects
        if not old_is_project or not new_is_project:
            return False

        # generate filenames
        path = self.data_path + self.project_dir
        filename = path + '/' + self.us(old_project.project_id()) + '.flproject'
        filename_bu = path + '/' + self.us(old_project.project_id()) + '.flproject_bu'
        filename_new = path + '/' + self.us(new_project.project_id()) + '.flproject'
        filename_new_bu = path + '/' + self.us(new_project.project_id()) + '.flproject_bu'

        # check if the files exist and rename them
        if os.path.isfile(filename):
            os.rename(filename, filename_new)

        if os.path.isfile(filename_bu):
            os.rename(filename_bu, filename_new_bu)

        return True

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
        filename = path + '/' + self.us(project.project_id()) + '.flproject'
        filename_bu = path + '/' + self.us(project.project_id()) + '.flproject_bu'

        # if it already exists, save a backup
        if os.path.isfile(filename):
            shutil.copy2(filename, filename_bu)

        # write the file
        f = open(filename, 'w')
        f.write(project.to_json())
        f.close()

    def save_project_list_to_file(self):
        """Save projects to [data_path]/projects/[project_id].flproject."""
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

    def us(self, string=''):
        """Return string with underscores instead of whitespace."""
        return string.replace(' ', '_')

    def update_inactive_list(self, settings=None):
        """Update the own inactive_list to speeden up things in Freelance."""
        self.inactive_list = None
        return self.get_inactive_list(settings=settings)

    def get_inactive_list(self, settings=None):
        """Get inactive clients and projects and return it into new list."""
        if self.inactive_list is not None:
            return self.inactive_list

        if type(settings) is Settings:
            data_path = settings.data_path
            client_dir = self.client_dir + settings.inactive_dir
            project_dir = self.project_dir + settings.inactive_dir
            self.inactive_list = List(
                data_path=data_path,
                client_dir=client_dir,
                project_dir=project_dir
            )
            return self.inactive_list

    def get_active_and_inactive_list(self, settings=None):
        """Get inactive clients and projects and active together."""
        # get both lists
        inact_list = self.get_inactive_list(settings=settings)
        act_list = self.copy()

        # combine clients and projects
        inact_list.project_list += act_list.project_list
        inact_list.client_list += act_list.client_list

        return inact_list

    def get_unpaid_invoices(self):
        """Return list with unpaid invoices - sorted by due date."""
        unpaid = []

        # cycle through all (active) projects
        for project in self.project_list:
            # cycle through the invoices of the project
            for invoice in project.get_invoice_list():
                # append it, if it has no paid_date set (None)
                if invoice.get_paid_date() is None and invoice.get_date() is not None:
                    unpaid.append(invoice)

        # sort the invoices by due date
        unpaid = sorted(unpaid, key=lambda x: x.get_due_date())

        return unpaid
