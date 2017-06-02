"""
Module for fetching ledger time track data and converting them to invoices.

In this module I get the ledger balance output for a time journal by using
os.popen() instead of a native python ledger module (which does not exist
for python3, afaik). This may not be the best and cleanest solution, but
it works somehow.
"""

import decimal
from general import check_objects
from general.functions import NewMultiplyEntry
from offer.entries import MultiplyEntry
from offer.offerquantitytime import OfferQuantityTime
import os


def get_ledger_output(settings=None, project_title=None):
    """Return string holding the ledger output."""
    is_settings = check_objects.is_settings(settings)
    project_title = str(project_title)

    if not is_settings:
        return ''

    # get the ledger command from the settings
    command = settings.ledger_time_command

    # the format for the ledger output
    ledger_output_format = (
        "%(partial_account != \"\" ? partial_account + \"---\" + display_total"
        " + \"\\n\" : \"\")"
    )

    # addition to the ledger command
    command_add = (
        ' --format \'{}\' b "{}"'.format(ledger_output_format, project_title)
    )

    return os.popen(command + command_add).read().splitlines()


def get_time_entries(ledger_output_lines=None):
    """
    Try to fetch the time entries from ledger output string.

    returns a dict like this: {ACCOUNT_NAME: HOURS_AS_DECIMAL}
    """
    if not type(ledger_output_lines) is list:
        return False

    # init output dict
    out = {}

    # go through the lines
    for line in ledger_output_lines:

        # left site
        try:
            left = line.split('---')[0]
        except Exception:
            # continue if this line is not splitable
            continue

        # right site
        try:
            right = line.split('---')[1]
        except Exception:
            # continue if this line is not splitable
            continue

        # get the account name from main account
        if ':' in left:
            account = left.split(':')[-1]

        # just get it as the account name
        else:
            account = left

        # get the seconds from the right site
        try:
            seconds = int(right[:-1])
        except Exception:
            # did not work, continue
            continue

        # convert the seconds to Decimal hours
        hours = decimal.Decimal(seconds) / decimal.Decimal(3600)

        # append it to the output
        out[account] = hours

    return out


def get_invoice_entries_from_time_journal(
    settings=None,
    global_list=None,
    presets=None,
    client=None,
    project=None,
    invoice=None
):
    """Add invoice entries from ledger time journal."""
    is_settings = check_objects.is_settings(settings)
    is_list = check_objects.is_list(global_list)
    is_presets = check_objects.is_preset(presets)
    is_client = check_objects.is_client(client)
    is_project = check_objects.is_project(project)
    is_invoice = check_objects.is_invoice(invoice)

    if (
        not is_settings or
        not is_list or
        not is_presets or
        not is_client or
        not is_project or
        not is_invoice
    ):
        return False

    # get a dict holding the time account names and its Decimal hours
    time = get_time_entries(
        ledger_output_lines=get_ledger_output(
            settings=settings,
            project_title=project.title
        )
    )

    if time is False:
        return False

    # generate a list of entries
    entries = []
    for t in time:

        # get the base for the time account

        # search the time entry account name in the presets,
        # which also have 'AUTO' in their name
        base = False
        for x in presets.invoice_entry_list:
            if 'AUTO' in x['name'] and t in x['name']:
                base = x['item']
                break

        # not found: generate a new multiplyentry
        if base is False:
            base = NewMultiplyEntry(
                settings=settings,
                global_list=global_list,
                client=client,
                project=project
            )

            # set values
            base.title = t
            base.set_hour_rate(1)

        # set the entry's quantity to the hours form the time entry
        base.set_quantity(time[t])

        # append it to the entries
        entries.append(base)

    return entries


def update_entry(entry=None, quantity=None):
    """Try to return new entry with updated quantity etc."""
    is_entry = check_objects.is_entry(entry)
    quantity = str(quantity)

    if not is_entry:
        return entry

    # it's no MultiplyEntry
    if type(entry) is not MultiplyEntry:
        entry.quantity_format = quantity
        return entry

    # it's a multiply entry: try to convert given quantity to OfferQuantityTime and string

    # first split the given quantity
    s = quantity.split(' ')

    # cancel if there are less than two
    if len(s) < 2:
        entry.quantity_format = quantity
        return entry

    # get the quantity number
    quantity_number = OfferQuantityTime(s[0])

    # get the quantity format
    quantity_format = ' '.join(s[1:])