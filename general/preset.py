"""Class for preset management."""

from datetime import datetime
import json
from offer.offer import Offer
from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry
import os
import shutil


def us(string=''):
    """Return string with underscores instead of whitespace."""
    return string.replace(' ', '_')


class Preset(object):
    """Preset class for loading and saving presets."""

    def __init__(
        self,
        data_path=None,
        offer_dir='/presets_offer',
        offer_list=None,
        entry_dir='/presets_entry',
        entry_list=None
    ):
        """Initialize the class."""
        self.data_path = data_path

        is_dir = os.path.isdir(str(self.data_path))
        if not is_dir:
            raise IOError

        self.offer_dir = offer_dir
        self.offer_list = (self.load_offer_list_from_file() if offer_list is None
                           else offer_list)

        self.entry_dir = entry_dir
        self.entry_list = (self.load_entry_list_from_file() if entry_list is None
                           else entry_list)

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

    def load_offer_list_from_file(self):
        """Load the offers from file and return offer_list."""
        path = self.data_path + self.offer_dir

        # check if the data_path/offer_presets directory exists and cancel otherwise
        if not os.path.isdir(str(path)):
            return []

        # cycle through the files and append them converted from json to the list
        out = []
        for file in sorted(os.listdir(path)):
            if file.endswith('.floffer'):
                # load the file
                f = open(path + '/' + file, 'r')
                load = f.read()
                f.close()

                # convert file content to offer object and append it
                out.append(self.load_offer_from_json(js=load))

        return out

    def add_offer(self, offer=None):
        """Add an offer preset."""
        is_offer = type(offer) is Offer
        title_exists = offer.title in [o.title for o in self.offer_list]

        # cancel if it's no offer or the title already exists in the presets
        if not is_offer or title_exists:
            return False

        # add the offer
        self.offer_list.append(offer)
        self.save_offer_to_file(offer=offer)
        return True

    def save_offer_to_file(self, offer=None):
        """Save single offer to file."""
        if type(offer) is not Offer:
            return False

        path = self.data_path + self.offer_dir

        # create dir if it does not exist
        is_dir = os.path.isdir(str(path))
        is_file = os.path.isfile(str(path))
        if not is_dir and not is_file:
            os.mkdir(path)

        # generate filenames
        filename = path + '/' + us(offer.title) + '.floffer'
        filename_bu = path + '/' + us(offer.title) + '.floffer_bu'

        # if it already exists, save a backup
        if os.path.isfile(filename):
            shutil.copy2(filename, filename_bu)

        # write the file
        f = open(filename, 'w')
        f.write(offer.to_json(indent=2))
        f.close()

    def remove_offer(self, offer=None):
        """Remove offer, if it exists."""
        is_offer = type(offer) is Offer
        title_exists = offer.title in [o.title for o in self.offer_list]

        # cancel if it's no offer or its title does not exist
        if not is_offer or not title_exists:
            return False

        # try to remove the offer
        try:
            self.offer_list.pop(self.offer_list.index(offer))
            self.delete_offer_file(offer=offer)
            return True
        except Exception:
            return False

    def load_entry_list_from_file(self):
        """Load the entrys from file and return entry_list."""
        path = self.data_path + self.entry_dir

        # check if the data_path/entry_presets directory exists and cancel otherwise
        if not os.path.isdir(str(path)):
            return []

        # cycle through the files and append them converted from json to the list
        out = []
        for file in sorted(os.listdir(path)):
            if file.endswith('.flentry'):
                # load the file
                f = open(path + '/' + file, 'r')
                load = f.read()
                f.close()

                # check entry type and append it
                js_tmp = json.loads(load)

                if 'type' in js_tmp.keys():
                    # it's BaseEntry - convert it from json and append it
                    if js_tmp['type'] == 'BaseEntry':
                        out.append(BaseEntry().from_json(js=js_tmp))

                    # it's MultiplyEntry - convert it from json and append it
                    elif js_tmp['type'] == 'MultiplyEntry':
                        out.append(MultiplyEntry().from_json(js=js_tmp))

                    # it's ConnectEntry - convert it from json and append it
                    elif js_tmp['type'] == 'ConnectEntry':
                        out.append(ConnectEntry().from_json(js=js_tmp))

        return out

    def add_entry(self, entry=None):
        """Add an entry preset."""
        is_entry = (type(entry) is BaseEntry or type(entry) is MultiplyEntry or
                    type(entry) is ConnectEntry)
        title_exists = entry.title in [e.title for e in self.entry_list]

        # cancel if it's no entry or the title already exists in the presets
        if not is_entry or title_exists:
            return False

        # add the entry
        self.entry_list.append(entry)
        self.save_entry_to_file(entry=entry)
        return True

    def save_entry_to_file(self, entry=None):
        """Save single entry to file."""
        is_entry = (type(entry) is BaseEntry or type(entry) is MultiplyEntry or
                    type(entry) is ConnectEntry)

        if not is_entry:
            return False

        path = self.data_path + self.entry_dir

        # create dir if it does not exist
        is_dir = os.path.isdir(str(path))
        is_file = os.path.isfile(str(path))
        if not is_dir and not is_file:
            os.mkdir(path)

        # generate filenames
        filename = path + '/' + us(entry.title) + '.flentry'
        filename_bu = path + '/' + us(entry.title) + '.flentry_bu'

        # if it already exists, save a backup
        if os.path.isfile(filename):
            shutil.copy2(filename, filename_bu)

        # write the file
        f = open(filename, 'w')
        f.write(entry.to_json())
        f.close()

    def remove_entry(self, entry=None):
        """Remove entry, if it exists."""
        is_entry = (type(entry) is BaseEntry or type(entry) is MultiplyEntry or
                    type(entry) is ConnectEntry)
        title_exists = entry.title in [e.title for e in self.entry_list]

        # cancel if it's no entry or its title does not exist
        if not is_entry or not title_exists:
            return False

        # try to remove the entry
        try:
            self.entry_list.pop(self.entry_list.index(entry))
            self.delete_entry_file(entry=entry)
            return True
        except Exception:
            return False

    def save_offer_list_to_file(self):
        """Save offer list to file."""
        for offer in self.offer_list:
            self.save_offer_to_file(offer=offer)

    def save_entry_list_to_file(self):
        """Save entry list to file."""
        for entry in self.entry_list:
            self.save_entry_to_file(entry=entry)

    def save_all(self):
        """Save all presets."""
        self.save_offer_list_to_file()
        self.save_entry_list_to_file()

    def reload(self, data_path=None):
        """Reload the presets."""
        is_dir = os.path.isdir(str(data_path))

        if not is_dir:
            raise IOError

        self.data_path = data_path
        self.offer_list = self.load_offer_list_from_file()
        self.entry_list = self.load_entry_list_from_file()