"""Class for preset management."""

import json
from offer.offerinvoice import Offer
from offer.offerinvoice import Invoice
from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry
import os
import shutil


class Preset(object):
    """Preset class for loading and saving presets."""

    def __init__(
        self,
        data_path=None,
        offer_dir='/presets_offer',
        offer_list=None,
        entry_dir='/presets_entry',
        entry_list=None,
        invoice_dir='/presets_invoice',
        invoice_list=None
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

        self.invoice_dir = invoice_dir
        self.invoice_list = (self.load_invoice_list_from_file() if invoice_list is None
                             else invoice_list)

    def add_offer(self, offer=None, name=None):
        """Add an offer preset."""
        added = self.add_item(
            item_list=self.offer_list,
            item=offer,
            name=name
        )

        if added:
            return self.save_offer_to_file(name=name)
        else:
            return added

    def save_offer_to_file(self, name=None):
        """Save single offer to file."""
        return self.save_item_to_file(
            item_list=self.offer_list,
            path=self.data_path + self.offer_dir,
            ending='.floffer',
            name=name
        )

    def delete_offer_file(self, name=None):
        """Delete single offer file."""
        return self.delete_item_file(
            item_list=self.offer_list,
            path=self.data_path + self.offer_dir,
            ending='.floffer',
            name=name
        )

    def remove_offer(self, name=None):
        """Remove offer, if it exists."""
        return self.remove_item(
            item_list=self.offer_list,
            path=self.data_path + self.offer_dir,
            ending='.floffer',
            name=name
        )

    def rename_offer(self, old_name=None, new_name=None):
        """Try to rename the offer with the given title."""
        return self.rename_item(
            item_list=self.offer_list,
            old_item_name=old_name,
            new_item_name=new_name
        )

    def add_entry(self, entry=None, name=None):
        """Add an entry preset."""
        added = self.add_item(
            item_list=self.entry_list,
            item=entry,
            name=name
        )

        if added:
            return self.save_entry_to_file(name=name)
        else:
            return added

    def save_entry_to_file(self, name=None):
        """Save single entry to file."""
        return self.save_item_to_file(
            item_list=self.entry_list,
            path=self.data_path + self.entry_dir,
            ending='.flentry',
            name=name
        )

    def delete_entry_file(self, name=None):
        """Delete single entry file."""
        return self.delete_item_file(
            item_list=self.entry_list,
            path=self.data_path + self.entry_dir,
            ending='.flentry',
            name=name
        )

    def remove_entry(self, name=None):
        """Remove entry, if it exists."""
        return self.remove_item(
            item_list=self.entry_list,
            path=self.data_path + self.entry_dir,
            ending='.flentry',
            name=name
        )

    def rename_entry(self, old_name=None, new_name=None):
        """Try to rename the entry with the given title."""
        return self.rename_item(
            item_list=self.entry_list,
            old_item_name=old_name,
            new_item_name=new_name
        )

    def add_invoice(self, invoice=None, name=None):
        """Add an invoice preset."""
        added = self.add_item(
            item_list=self.invoice_list,
            item=invoice,
            name=name
        )

        if added:
            return self.save_invoice_to_file(name=name)
        else:
            return added

    def save_invoice_to_file(self, name=None):
        """Save single invoice to file."""
        return self.save_item_to_file(
            item_list=self.invoice_list,
            path=self.data_path + self.invoice_dir,
            ending='.flinvoice',
            name=name
        )

    def delete_invoice_file(self, name=None):
        """Delete single invoice file."""
        return self.delete_item_file(
            item_list=self.invoice_list,
            path=self.data_path + self.invoice_dir,
            ending='.flinvoice',
            name=name
        )

    def remove_invoice(self, name=None):
        """Remove invoice, if it exists."""
        return self.remove_item(
            item_list=self.invoice_list,
            path=self.data_path + self.invoice_dir,
            ending='.flinvoice',
            name=name
        )

    def rename_invoice(self, old_name=None, new_name=None):
        """Try to rename the invoice with the given title."""
        return self.rename_item(
            item_list=self.invoice_list,
            old_item_name=old_name,
            new_item_name=new_name
        )

    def add_item(self, item_list=None, item=None, name=None):
        """Add an invoice preset."""
        is_item = (
            type(item) is Offer or
            type(item) is Invoice or
            type(item) is BaseEntry or
            type(item) is MultiplyEntry or
            type(item) is ConnectEntry
        )

        name_exists = str(name) in [i['name'] for i in item_list]

        # cancel if it's no invoice or the title already exists in the presets
        if not is_item or name_exists:
            return False

        # add the item
        item_list.append({
            'item': item,
            'name': str(name)
        })

        return True

    def save_item_to_file(self, item_list=None, path=None, ending=None, name=None):
        """Save the item to the file."""
        # try to get item or cancel
        try:
            for i in item_list:
                # found the name
                if i['name'] == str(name):
                    # assign the item to the variable
                    item = i
                    break
        except Exception:
            return False

        # create dir if it does not exist
        is_dir = os.path.isdir(str(path))
        is_file = os.path.isfile(str(path))
        if not is_dir and not is_file:
            os.mkdir(path)

        # generate filenames
        filename = path + '/' + self.us(str(name)) + ending
        filename_bu = path + '/' + self.us(str(name)) + ending + '_bu'

        # if it already exists, save a backup
        if os.path.isfile(filename):
            shutil.copy2(filename, filename_bu)

        try:
            # generate file content
            content = item.copy()
            content['item'] = content['item'].to_dict()

            # write the file
            with open(filename, 'w') as f:
                f.write(json.dumps(content, indent=2))

            return True
        except Exception:
            return False

    def load_item_from_file(self, filename=None):
        """Load the item from the file."""
        filename = str(filename)

        # cancel if the file does not exist
        if not os.path.isfile(filename):
            return False

        # try to load the file
        try:
            with open(filename, 'r') as f:
                dic = json.load(f)
        except Exception:
            return False

        # get type
        typ = False
        if 'item' in dic.keys():
            if 'type' in dic['item'].keys():
                typ = dic['item']['type']

        # has no type, so cancel
        if not typ:
            return False

        # convert item json to Offer
        if typ == 'Offer':
            dic['item'] = Offer().from_json(js=dic['item'])

        # convert item json to Invoice
        elif typ == 'Invoice':
            dic['item'] = Invoice().from_json(js=dic['item'])

        # convert item json to BaseEntry
        elif typ == 'BaseEntry':
            dic['item'] = BaseEntry().from_json(js=dic['item'])

        # convert item json to MultiplyEntry
        elif typ == 'MultiplyEntry':
            dic['item'] = MultiplyEntry().from_json(js=dic['item'])

        # convert item json to ConnectEntry
        elif typ == 'ConnectEntry':
            dic['item'] = ConnectEntry().from_json(js=dic['item'])

        # otherwise cancel
        else:
            return False

        return dic

    def delete_item_file(self, item_list=None, path=None, ending=None, name=None):
        """Delete single offer file."""
        # cancel if name does not exist in list
        try:
            if str(name) not in [i['name'] for i in item_list]:
                return False
        except Exception:
            return False

        # generate filenames
        filename = path + '/' + self.us(str(name)) + ending
        filename_bu = path + '/' + self.us(str(name)) + ending + '_bu'

        # if it exists, backup and delete
        if os.path.isfile(filename):
            shutil.copy2(filename, filename_bu)
            os.remove(filename)
            return True
        else:
            return False

    def remove_item(self, item_list=None, path=None, ending=None, name=None):
        """Remove item from list and delete file."""
        # get index or cancel if name does not exist
        try:
            index = -1
            for i, n in enumerate(item_list):
                if n['name'] == str(name):
                    index = i
                    break
            if index < 0:
                return False
        except Exception:
            return False

        # try to remove the item
        try:
            # delete its file
            check = self.delete_item_file(
                item_list=item_list,
                path=path,
                ending=ending,
                name=name
            )

            # pop it from the list
            item_list.pop(index)

            # return if it went ok or not
            return check

        # fallback canceling
        except Exception:
            return False

    def rename_item(self, item_list=None, old_item_name=None, new_item_name=None):
        """Try to rename the item with the given name."""
        # get index of original or cancel
        try:
            index = -1
            for i, item in enumerate(item_list):
                if str(old_item_name) == item['name']:
                    index = i
                    break
            if index < 0:
                return False
        except Exception:
            return False

        # add a new preset with the old item
        added = self.add_item(
            item_list=item_list,
            item=item_list[index]['item'],
            name=str(new_item_name)
        )

        # could not add it, since it already exists
        if not added:
            return False

        # added, now remove the old one
        return self.remove_item(
            item_list=item_list,
            name=old_item_name
        )

    def load_item_list_from_file(self, path=None, ending=None):
        """Load item list from file and return list."""
        # check if the directory exists and cancel otherwise
        if not os.path.isdir(str(path)):
            return []

        # cycle through the files and append them converted from json to the list
        out = []
        for file in sorted(os.listdir(path)):
            if file.endswith(ending):
                # load and convert file content to item and append it
                out.append(
                    self.load_item_from_file(filename=os.path.join(path, file))
                )

        # return filtered list - filter out the failed loaded data
        return list(filter(lambda x: x is not False, out))

    def save_offer_list_to_file(self):
        """Save offer list to file."""
        for i in self.offer_list:
            self.save_offer_to_file(name=i['name'])

    def load_offer_list_from_file(self):
        """Load the offers from file and return offer_list."""
        return self.load_item_list_from_file(
            path=self.data_path + self.offer_dir,
            ending='.floffer'
        )

    def save_entry_list_to_file(self):
        """Save entry list to file."""
        for i in self.entry_list:
            self.save_entry_to_file(name=i['name'])

    def load_entry_list_from_file(self):
        """Load the entrys from file and return entry_list."""
        return self.load_item_list_from_file(
            path=self.data_path + self.entry_dir,
            ending='.flentry'
        )

    def save_invoice_list_to_file(self):
        """Save invoice list to file."""
        for i in self.invoice_list:
            self.save_invoice_to_file(name=i['name'])

    def load_invoice_list_from_file(self):
        """Load the invoices from file and return invoice_list."""
        return self.load_item_list_from_file(
            path=self.data_path + self.invoice_dir,
            ending='.flinvoice'
        )

    def save_all(self):
        """Save all presets."""
        self.save_offer_list_to_file()
        self.save_entry_list_to_file()
        self.save_invoice_list_to_file()

    def reload(self, data_path=None):
        """Reload the presets."""
        is_dir = os.path.isdir(str(data_path))

        if not is_dir:
            raise IOError

        self.data_path = data_path
        self.offer_list = self.load_offer_list_from_file()
        self.entry_list = self.load_entry_list_from_file()
        self.invoice_list = self.load_invoice_list_from_file()

    def us(self, string=''):
        """Return string with underscores instead of whitespace."""
        return string.replace(' ', '_')
