"""Load and save functions."""

import json
from clients.project import Project
from offer.offer import Offer
from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry


def load_offer_from_json(js=None):
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
