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
from offer.quantitytime import QuantityTime
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

    Returns a dict like this: {ACCOUNT_NAME: HOURS_AS_DECIMAL}
    Returns the total time and its account as well, if the other accounts
    to not sum up to the total time.
    """
    if not type(ledger_output_lines) is list:
        return False

    # init output dict
    out = {}

    # check counting
    total = decimal.Decimal(0)
    total_key = ''
    amount = decimal.Decimal(0)

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

            # add the time checking
            total_key = account

        # just get it as the account name
        else:
            account = left

        # get the seconds from the right site
        try:
            seconds = int(right[:-1])

            # add the time checking
            if total_key != '' and total == 0:
                total = decimal.Decimal(seconds)
            else:
                amount += decimal.Decimal(seconds)
        except Exception:
            # did not work, continue
            continue

        # convert the seconds to Decimal hours
        hours = decimal.Decimal(seconds) / decimal.Decimal(3600)

        # append it to the output
        out[account] = hours

    # delete the total account, if the other sum up correctly
    if total == amount:
        del out[total_key]

    return out


def get_invoice_entries_from_time_journal(
    settings=None,
    global_list=None,
    presets=None,
    client=None,
    project=None,
    invoice=None
):
    """Return list with invoice entries from ledger time journal."""
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
        name_splitted = t.lower().split(' ') + ['auto']
        for x in presets.invoice_entry_list:
            name_in_presets = [
                i for i in name_splitted
                if i in x['name'].lower()
            ]

            if len(name_in_presets) > 1:
                base = x['item']
                base.title = t
                base.set_hour_rate(1)
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
        entries.append(base.copy())

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

    # it's a multiply entry: try to convert given quantity to QuantityTime and string

    # first split the given quantity
    s = quantity.split(' ')

    # quantity string given as well
    if len(s) > 1:
        # set new quantity format
        entry.quantity_format = '{s} ' + ' '.join(s[1:])

    # only one thign entered
    else:
        # set new quantity format
        entry.quantity_format = '{s}'

    # get the quantity number
    quantity_number = QuantityTime(s[0])

    # first given thing is a number > 0
    if quantity_number > 0:

        # calculate the new hour rate
        hour_rate = entry.get_quantity() / quantity_number

        # set new hour rate
        entry.set_hour_rate(hour_rate)

        # set new quantity
        entry.set_quantity(quantity_number)

    # it's something else, set quantity_format from argument and leave quantity
    else:
        entry.quantity_format = quantity

    return entry
