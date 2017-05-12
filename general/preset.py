"""Class for preset management."""

import json
from offer.offerinvoice import Offer
from offer.offerinvoice import Invoice
from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry
import os
import shutil

from general.debug import debug


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
                out.append(Offer().from_json(js=load))

        return out

    def load_invoice_list_from_file(self):
        """Load the invoices from file and return invoice_list."""
        path = self.data_path + self.invoice_dir

        # check if the data_path/invoice_presets directory exists and cancel otherwise
        if not os.path.isdir(str(path)):
            return []

        # cycle through the files and append them converted from json to the list
        out = []
        for file in sorted(os.listdir(path)):
            if file.endswith('.flinvoice'):
                # load the file
                f = open(path + '/' + file, 'r')
                load = f.read()
                f.close()

                # convert file content to invoice object and append it
                out.append(Invoice().from_json(js=load))

        return out

    def add_offer(self, offer=None):
        """Add an offer preset."""
        is_offer = type(offer) is Offer
        title_exists = offer.title in [o.title for o in self.offer_list]
        title_empty = offer.title == ''

        # cancel if it's no offer or the title already exists in the presets
        if not is_offer or title_exists or title_empty:
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
        filename = path + '/' + self.us(offer.title) + '.floffer'
        filename_bu = path + '/' + self.us(offer.title) + '.floffer_bu'

        # if it exists, delete
        if os.path.isfile(filename):
            shutil.copy2(filename, filename_bu)

        # write the file
        f = open(filename, 'w')
        f.write(offer.to_json(indent=2))
        f.close()

    def delete_offer_file(self, offer=None):
        """Delete single offer file."""
        is_offer = type(offer) is Offer

        if not is_offer:
            return False

        path = self.data_path + self.offer_dir

        # generate filenames
        filename = path + '/' + self.us(offer.title) + '.floffer'

        # if it exists, delete
        if os.path.isfile(filename):
            os.remove(filename)
            return True
        else:
            return False

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

    def rename_offer(self, old_offer_title=None, new_offer_title=None):
        """Try to rename the offer with the given title."""
        offer_found = old_offer_title in [o.title for o in self.offer_list]

        if not offer_found:
            return False

        # get copy of offer object
        offer_old = None
        offer_copy = None
        for o in self.offer_list:
            if o.title == old_offer_title:
                offer_old = o
                offer_copy = o.copy()
                break

        # rename it and try to add it
        offer_copy.title = new_offer_title

        added = self.add_offer(offer=offer_copy)

        if not added:
            return False

        # delete the old one
        self.remove_offer(offer=offer_old)

        return True

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
        title_empty = entry.title == ''

        # cancel if it's no entry or the title already exists in the presets
        if not is_entry or title_exists or title_empty:
            return False

        # clear connected list, since it's just supposed to be a preset for this entry
        if type(entry) is ConnectEntry:
            entry.disconnect_all_entries()

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
        filename = path + '/' + self.us(entry.title) + '.flentry'
        filename_bu = path + '/' + self.us(entry.title) + '.flentry_bu'

        # if it already exists, save a backup
        if os.path.isfile(filename):
            shutil.copy2(filename, filename_bu)

        # write the file
        f = open(filename, 'w')
        f.write(entry.to_json())
        f.close()

    def delete_entry_file(self, entry=None):
        """Delete single entry file."""
        is_entry = (type(entry) is BaseEntry or type(entry) is MultiplyEntry or
                    type(entry) is ConnectEntry)

        if not is_entry:
            return False

        path = self.data_path + self.entry_dir

        # generate filenames
        filename = path + '/' + self.us(entry.title) + '.flentry'

        # if it exists, delete
        if os.path.isfile(filename):
            os.remove(filename)
            return True
        else:
            return False

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

    def rename_entry(self, old_entry_title=None, new_entry_title=None):
        """Try to rename the entry with the given title."""
        entry_found = old_entry_title in [e.title for e in self.entry_list]

        if not entry_found:
            return False

        # get copy of entry object
        entry_old = None
        entry_copy = None
        for e in self.entry_list:
            if e.title == old_entry_title:
                entry_old = e
                entry_copy = e.copy()
                break

        # rename it and try to add it
        entry_copy.title = new_entry_title

        added = self.add_entry(entry=entry_copy)

        if not added:
            return False

        # delete the old one
        self.remove_entry(entry=entry_old)

        return True

    def add_invoice(self, invoice=None):
        """Add an invoice preset."""
        is_invoice = type(invoice) is Invoice
        title_exists = invoice.title in [o.title for o in self.invoice_list]
        title_empty = invoice.title == ''

        # cancel if it's no invoice or the title already exists in the presets
        if not is_invoice or title_exists or title_empty:
            return False

        # add the invoice
        self.invoice_list.append(invoice)
        self.save_invoice_to_file(invoice=invoice)
        return True

    def save_invoice_to_file(self, invoice=None):
        """Save single invoice to file."""
        if type(invoice) is not Invoice:
            return False

        path = self.data_path + self.invoice_dir

        # create dir if it does not exist
        is_dir = os.path.isdir(str(path))
        is_file = os.path.isfile(str(path))
        if not is_dir and not is_file:
            os.mkdir(path)

        # generate filenames
        filename = path + '/' + self.us(invoice.title) + '.flinvoice'
        filename_bu = path + '/' + self.us(invoice.title) + '.flinvoice_bu'

        # if it already exists, save a backup
        if os.path.isfile(filename):
            shutil.copy2(filename, filename_bu)

        # write the file
        f = open(filename, 'w')
        f.write(invoice.to_json(indent=2))
        f.close()

    def delete_invoice_file(self, invoice=None):
        """Delete single invoice file."""
        is_invoice = type(invoice) is Offer

        if not is_invoice:
            return False

        path = self.data_path + self.invoice_dir

        # generate filenames
        filename = path + '/' + self.us(invoice.title) + '.flinvoice'

        # if it already exists, save a backup
        if os.path.isfile(filename):
            os.remove(filename)
            return True
        else:
            return False

    def remove_invoice(self, invoice=None):
        """Remove invoice, if it exists."""
        is_invoice = type(invoice) is Invoice
        title_exists = invoice.title in [o.title for o in self.invoice_list]

        # cancel if it's no invoice or its title does not exist
        if not is_invoice or not title_exists:
            return False

        # try to remove the invoice
        try:
            self.invoice_list.pop(self.invoice_list.index(invoice))
            self.delete_invoice_file(invoice=invoice)
            return True
        except Exception:
            return False

    def rename_invoice(self, old_invoice_title=None, new_invoice_title=None):
        """Try to rename the invoice with the given title."""
        invoice_found = old_invoice_title in [o.title for o in self.invoice_list]

        if not invoice_found:
            return False

        # get copy of invoice object
        invoice_old = None
        invoice_copy = None
        for o in self.invoice_list:
            if o.title == old_invoice_title:
                invoice_old = o
                invoice_copy = o.copy()
                break

        # rename it and try to add it
        invoice_copy.title = new_invoice_title

        added = self.add_invoice(invoice=invoice_copy)

        if not added:
            return False

        # delete the old one
        self.remove_invoice(invoice=invoice_old)

        return True

    def save_offer_list_to_file(self):
        """Save offer list to file."""
        for offer in self.offer_list:
            self.save_offer_to_file(offer=offer)

    def save_entry_list_to_file(self):
        """Save entry list to file."""
        for entry in self.entry_list:
            self.save_entry_to_file(entry=entry)

    def save_invoice_list_to_file(self):
        """Save invoice list to file."""
        for invoice in self.invoice_list:
            self.save_invoice_to_file(invoice=invoice)

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
