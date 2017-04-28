"""The class holding informatin about the client and the client_list."""

import json
import os
import shutil


class Client(object):
    """This class holds the detailed client information."""

    def __init__(
        self,
        client_id=None,
        client_list=None,
        company=None,
        salutation=None,
        name=None,
        family_name=None,
        street=None,
        post_code=None,
        city=None,
        tax_id=None,
        language=None
    ):
        """Initialize the class."""
        self._client_id = ''                        # set default
        self.set_client_id(client_id, client_list)  # try to set argument
        self.company = '' if company is None else str(company)
        self.salutation = '' if salutation is None else str(salutation)
        self.name = '' if name is None else str(name)
        self.family_name = '' if family_name is None else str(family_name)
        self.street = '' if street is None else str(street)
        self.post_code = '' if post_code is None else str(post_code)
        self.city = '' if city is None else str(city)
        self.tax_id = '' if tax_id is None else str(tax_id)
        self.language = '' if language is None else str(language)

    def get_project_list(self, project_list=None):
        """Get project_list for client from global project_list."""
        if type(project_list) is list:
            return [p for p in project_list if p.get_client_id() == self.get_client_id()]
        else:
            return []

    def set_client_id(self, value, client_list=None):
        """Try to set client_id if it's not in the client_list already."""
        if client_list is None:
            self._client_id = str(value)
            return True
        if type(client_list) is list:
            if not str(value) in [i.get_client_id() for i in client_list]:
                self._client_id = str(value)
                return True
        return False

    def get_client_id(self):
        """Get client_id."""
        if self._client_id == '':
            return 'no_id'
        else:
            return self._client_id

    def get_projects(self, project_list):
        """Get list of projects for only that client."""
        out = []
        for project in project_list:
            try:
                if project.client_id == self.client_id:
                    out.append(project)
            except Exception:
                pass

        return out

    def to_json(self, indent=2):
        """Convert variables data to json format."""
        out = {}

        # fetch all variables
        out['type'] = self.__class__.__name__
        out['client_id'] = self.get_client_id()
        out['company'] = self.company
        out['salutation'] = self.salutation
        out['name'] = self.name
        out['family_name'] = self.family_name
        out['street'] = self.street
        out['post_code'] = self.post_code
        out['city'] = self.city
        out['tax_id'] = self.tax_id
        out['language'] = self.language

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

        # create new entry object from json
        if 'client_id' in js.keys():
            client_id = js['client_id']
        else:
            client_id = None

        if 'company' in js.keys():
            company = js['company']
        else:
            company = None

        if 'salutation' in js.keys():
            salutation = js['salutation']
        else:
            salutation = None

        if 'name' in js.keys():
            name = js['name']
        else:
            name = None

        if 'family_name' in js.keys():
            family_name = js['family_name']
        else:
            family_name = None

        if 'street' in js.keys():
            street = js['street']
        else:
            street = None

        if 'post_code' in js.keys():
            post_code = js['post_code']
        else:
            post_code = None

        if 'city' in js.keys():
            city = js['city']
        else:
            city = None

        if 'tax_id' in js.keys():
            tax_id = js['tax_id']
        else:
            tax_id = None

        if 'language' in js.keys():
            language = js['language']
        else:
            language = None

        # return new object
        return cls(
            client_id=client_id,
            company=company,
            salutation=salutation,
            name=name,
            family_name=family_name,
            street=street,
            post_code=post_code,
            city=city,
            tax_id=tax_id,
            language=language
        )


class ClientList(object):
    """The list holding the client objects."""

    def __init__(
        self,
        data_path=None,
        client_list=None
    ):
        """Initialize the class."""
        self.data_path = data_path
        self._client_list = self.load_from_file()
        self.set_client_list(client_list)

    def append(self, client=None):
        """Append a client, if its id does not exists already."""
        if type(client) is not Client:
            return

        # check if ID does not exist and append it only then
        if not client.get_client_id() in self.get_all_ids():
            self._client_list.append(client)

    def pop(self, index):
        """Pop client with the given index from list."""
        if index < len(self._client_list):
            self._client_list.pop(index)

    def move(self, entry_index=None, direction=None):
        """Move an entry with entry_index in client_list up/down."""
        if entry_index is None or direction is None:
            return

        # cancel, if entry_index is out of range
        if entry_index >= len(self._client_list):
            return

        # calculate new index: move up (direction == 1) or down (direction == -1)
        new_index = entry_index + direction

        # put at beginning, if it's at the end and it's moved up
        if new_index >= len(self._client_list):
            new_index = 0

        # put at the end, if it's at the beginning and moved down
        if new_index < 0:
            new_index = len(self._client_list) - 1

        # move it!
        self._client_list.insert(new_index, self._client_list.pop(entry_index))

    def get_all_ids(self):
        """Get all client IDs."""
        return [client_id.get_client_id() for client_id in self._client_list]

    def set_client_list(self, client_list=None):
        """Try to set client list."""
        if type(client_list) is list:
            # each type inside list has to be Client object
            for i in client_list:
                if type(i) is not Client:
                    return

            # done and correct, set it
            self._client_list = client_list

    def get_client_list(self):
        """Get the client list."""
        return self._client_list

    def save_to_file(self, data_path=None):
        """Save clients from client_list to [data_path]/clients/[client_id].flclient."""
        if data_path is None:
            if self.data_path is None:
                return False
            else:
                data_path = self.data_path

        # check if client directory exists and create one if needed
        if not os.path.isdir(data_path + '/clients'):
            os.mkdir(data_path + '/clients')

        # cycle through clients and save each client into its own file
        for client in self.get_client_list():
            # cancel this entry, if it's no Client object
            if type(client) is not Client:
                continue

            # generate filenames
            filename = data_path + '/clients/' + client.get_client_id() + '.flclient'
            filename_bu = (data_path + '/clients/' + client.get_client_id() +
                           '.flclient_bu')

            # if it already exists, save a backup
            if os.path.isfile(filename):
                shutil.copy2(filename, filename_bu)

            # write the file
            f = open(filename, 'w')
            f.write(client.to_json())
            f.close()
        return True

    def load_from_file(self, data_path=None):
        """Load the clients from file and return client_list."""
        if data_path is None:
            if self.data_path is None:
                return []
            else:
                data_path = self.data_path

        path = data_path + '/clients/'

        # check if the data_path/clients directory exists and cancel otherwise
        if not os.path.isdir(path):
            return []

        # cycle through the files and append them converted from json to the list
        out = []
        for file in sorted(os.listdir(path)):
            if file.endswith('.flclient'):
                # load the file
                f = open(path + file, 'r')
                load = f.read()
                f.close()

                # convert file content to Client object and append it
                out.append(Client().from_json(js=load))

        return out
