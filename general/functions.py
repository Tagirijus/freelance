"""Modul holding the general functions."""

from clients.client import Client
from clients.list import List
from clients.project import Project
from datetime import date
from general.settings import Settings
from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry
from offer.offer import Offer
import os

from general.debug import debug


class ReplacementDict(dict):
    """A dict with a __missing__ method."""

    def __missing__(self, key):
        """Return the key instead."""
        return '{' + str(key) + '}'


def can_be_dir(string):
    """
    Check if the given string could be a creatable dir or exists.

    The function checks if the string already exists and is a directory.
    It also tries to create a new folder in this folder to check, if
    the neccessary permission is granted.
    """
    try:
        # check if it already exists
        if os.path.exists(string):
            if os.path.isdir(string):
                # it already exists and is a dir
                try:
                    # try to create a dir inside it to check permission
                    os.mkdir(string + '/TAGIRIJUS_FREELANCE_CHECK')
                    os.rmdir(string + '/TAGIRIJUS_FREELANCE_CHECK')
                    # worked!
                    return True
                except Exception:
                    # no permission probably
                    return False
            else:
                # it already exists and is probably a file
                return False
        else:
            # it does not exist, try to create it
            os.mkdir(string)
            os.rmdir(string)
            return True
    except Exception:
        # no permission maybe
        return False


def move_list_entry(lis=None, index=None, direction=None):
    """Move an list entry with index in lis up/down."""
    one_not_set = lis is None or index is None or direction is None
    out_of_range = index >= len(lis)

    # cancel, if one argument is not set or offer_index is out of range
    if one_not_set or out_of_range:
        return

    # calculate new index: move up (direction == 1) or down (direction == -1)
    new_index = index + direction

    # put at beginning, if it's at the end and it's moved up
    new_index = 0 if new_index >= len(lis) else new_index

    # put at the end, if it's at the beginning and moved down
    new_index = len(lis) - 1 if new_index < 0 else new_index

    # move it!
    lis.insert(new_index, lis.pop(index))

    # return new index
    return new_index


def replacer(
    text=None,
    settings=None,
    client=None,
    project=None,
    global_list=None
):
    """Replace {...} inside text with stuff from client or project ... or the date."""
    is_settings = type(settings) is Settings
    is_client = type(client) is Client
    is_project = type(project) is Project
    is_global_list = type(global_list) is List

    # replace stuff
    replace_me = ReplacementDict()

    # simple date stuff
    replace_me['YEAR'] = date.today().strftime('%Y')
    replace_me['MONTH'] = date.today().strftime('%m')
    replace_me['DAY'] = date.today().strftime('%d')

    # global lists related
    if is_global_list and is_settings:
        # get active stuff
        active_clients = set([c.client_id for c in global_list.client_list])
        active_projects = set([p for p in global_list.project_list])

        # get inactive stuff
        inactive_clients = set([c for c in global_list.get_inactive_list(
            settings=settings
        ).client_list])
        inactive_projects = set([p for p in global_list.get_inactive_list(
            settings=settings
        ).project_list])

        # put them together to get all clients and projects (but no double entries)
        all_clients = active_clients | inactive_clients
        all_projects = active_projects | inactive_projects

        # get all offers
        all_offers = set([off for o in all_projects for off in o.get_offer_list()])

        # count clients
        replace_me['CLIENT_COUNT'] = str(len(all_clients) + 1)
        replace_me['PROJECT_COUNT'] = str(len(all_projects) + 1)
        replace_me['OFFER_COUNT'] = str(
            settings.get_offer_count_offset() + len(all_offers) + 1
        )

    # project related
    if is_project:
        replace_me['PROJECT_TITLE'] = project.title
        replace_me['PROJECT_OFFER_COUNT'] = str(len(project.get_offer_list()) + 1)

    # client related
    if is_client:
        replace_me['CLIENT_COMPANY'] = client.company
        replace_me['CLIENT_SALUT'] = client.salutation
        replace_me['CLIENT_NAME'] = client.name
        replace_me['CLIENT_FAMILY'] = client.family_name
        replace_me['CLIENT_FULLNAME'] = client.fullname()
        replace_me['CLIENT_STREET'] = client.street
        replace_me['CLIENT_POST_CODE'] = client.post_code
        replace_me['CLIENT_CITY'] = client.city
        replace_me['CLIENT_TAX_ID'] = client.tax_id

    return text.format(**replace_me)


def NewClient(settings=None, global_list=None):
    """Return new client object according to settings defaults."""
    # return empty client, if there is no correct settings object given
    if type(settings) is not Settings:
        return Client()

    # get language form settings file
    lang = settings.get_def_language()

    # get client count / id
    client_id = replacer(
        text=settings.defaults[lang].client_id,
        settings=settings,
        global_list=global_list
    )

    # return client with default values according to chosen language
    return Client(
        client_id=client_id,
        company=settings.defaults[lang].client_company,
        salutation=settings.defaults[lang].client_salutation,
        name=settings.defaults[lang].client_name,
        family_name=settings.defaults[lang].client_family_name,
        street=settings.defaults[lang].client_street,
        post_code=settings.defaults[lang].client_post_code,
        city=settings.defaults[lang].client_city,
        tax_id=settings.defaults[lang].client_tax_id,
        language=lang
    )


def NewProject(settings=None, global_list=None, client=None):
    """Return new project object according to given settings and client."""
    is_settings = type(settings) is Settings
    is_client = type(client) is Client

    # return empty project if no valid settings or client  object is given
    debug(is_settings, is_client)
    if not is_settings or not is_client:
        return Project()

    # get language from client
    lang = client.language

    # generate default title (according to replacements)
    title = replacer(
        text=settings.defaults[lang].project_title,
        settings=settings,
        global_list=global_list,
        client=client
    )

    return Project(
        client_id=client.client_id,
        title=title,
        hours_per_day=settings.defaults[lang].get_project_hours_per_day(),
        work_days=settings.defaults[lang].get_project_work_days(),
        wage=settings.defaults[lang].get_project_wage(),
        minimum_days=settings.defaults[lang].get_project_minimum_days()
    )


def NewOffer(settings=None, global_list=None, client=None, project=None):
    """Return new offer object according to settings defaults."""
    # return empty offer, if there is no correct settings object given
    is_settings = type(settings) is Settings
    is_client = type(client) is Client
    is_project = type(project) is Project

    if not is_settings or not is_project or not is_client:
        return Offer()

    # get language from client
    lang = client.language

    # get replaces
    title = replacer(
        text=settings.defaults[lang].offer_title,
        settings=settings,
        global_list=global_list,
        client=client,
        project=project
    )

    # get other values
    date_fmt = settings.defaults[lang].date_fmt
    round_price = settings.defaults[lang].get_offer_round_price()

    # return new Offer object
    return Offer(
        title=title,
        date_fmt=date_fmt,
        date=date.today(),
        round_price=round_price
    )


def PresetOffer(
    offer_preset=None,
    settings=None,
    global_list=None,
    client=None,
    project=None
):
    """Return new Offer based on given offer, but with string replacements."""
    if type(offer_preset) is not Offer:
        return NewOffer(
            settings=settings,
            global_list=global_list,
            client=client,
            project=project
        )

    # get replaces
    title = replacer(
        text=offer_preset.title,
        settings=settings,
        global_list=global_list,
        client=client,
        project=project
    )

    # get other values
    date_fmt = offer_preset.date_fmt
    off_date = offer_preset.get_date()
    wage = offer_preset.get_wage()
    round_price = offer_preset.get_round_price()
    entry_list = offer_preset.get_entry_list()

    # return new Offer object
    return Offer(
        title=title,
        date_fmt=date_fmt,
        date=off_date,
        wage=wage,
        round_price=round_price,
        entry_list=entry_list
    )


def NewBaseEntry(settings=None, global_list=None, client=None, project=None):
    """Return BaseEntry according to settings."""
    is_settings = type(settings) is Settings
    is_client = type(client) is Client

    if not is_settings or not is_client:
        return BaseEntry()

    # get language from client
    lang = client.language

    # get replaces
    title = replacer(
        text=settings.defaults[lang].baseentry_title,
        settings=settings,
        global_list=global_list,
        client=client,
        project=project
    )
    comment = replacer(
        text=settings.defaults[lang].baseentry_comment,
        settings=settings,
        global_list=global_list,
        client=client,
        project=project
    )

    # get other values
    amount = settings.defaults[lang].get_baseentry_amount()
    amount_format = settings.defaults[lang].baseentry_amount_format
    time = settings.defaults[lang].get_baseentry_time()
    price = settings.defaults[lang].get_baseentry_price()

    # return entry with default values from settings default
    return BaseEntry(
        title=title,
        comment=comment,
        amount=amount,
        amount_format=amount_format,
        time=time,
        price=price
    )


def PresetBaseEntry(
    entry_preset=None,
    settings=None,
    global_list=None,
    client=None,
    project=None
):
    """Return BaseEntry according to settings."""
    if type(entry_preset) is not BaseEntry:
        return NewBaseEntry(settings=settings, client=client, project=project)

    # get replaces
    title = replacer(
        text=entry_preset.title,
        settings=settings,
        global_list=global_list,
        client=client,
        project=project
    )
    comment = replacer(
        text=entry_preset.comment,
        settings=settings,
        global_list=global_list,
        client=client,
        project=project
    )

    # get other values
    id = entry_preset._id
    amount = entry_preset._amount
    amount_format = entry_preset.amount_format
    time = entry_preset._time
    price = entry_preset._price

    # return entry with default values from settings default
    return BaseEntry(
        id=id,
        title=title,
        comment=comment,
        amount=amount,
        amount_format=amount_format,
        time=time,
        price=price
    )


def NewMultiplyEntry(settings=None, global_list=None, client=None, project=None):
    """Return MultiplyEntry according to settings."""
    is_settings = type(settings) is Settings
    is_client = type(client) is Client

    if not is_settings or not is_client:
        return MultiplyEntry()

    # get language from client
    lang = client.language

    # get replaces
    title = replacer(
        text=settings.defaults[lang].multiplyentry_title,
        settings=settings,
        global_list=global_list,
        client=client,
        project=project
    )
    comment = replacer(
        text=settings.defaults[lang].multiplyentry_comment,
        settings=settings,
        global_list=global_list,
        client=client,
        project=project
    )

    # get other values
    amount = settings.defaults[lang].get_multiplyentry_amount()
    amount_format = settings.defaults[lang].multiplyentry_amount_format
    hour_rate = settings.defaults[lang].get_multiplyentry_hour_rate()

    # return entry with default values from settings default
    return MultiplyEntry(
        title=title,
        comment=comment,
        amount=amount,
        amount_format=amount_format,
        hour_rate=hour_rate
    )


def PresetMultiplyEntry(
    entry_preset=None,
    settings=None,
    global_list=None,
    client=None,
    project=None
):
    """Return MultiplyEntry according to settings."""
    if type(entry_preset) is not MultiplyEntry:
        return NewMultiplyEntry(settings=settings, client=client, project=project)

    # get replaces
    title = replacer(
        text=entry_preset.title,
        settings=settings,
        global_list=global_list,
        client=client,
        project=project
    )
    comment = replacer(
        text=entry_preset.comment,
        settings=settings,
        global_list=global_list,
        client=client,
        project=project
    )

    # get other values
    id = entry_preset._id
    amount = entry_preset._amount
    amount_format = entry_preset.amount_format
    hour_rate = entry_preset._hour_rate

    # return entry with default values from settings default
    return MultiplyEntry(
        id=id,
        title=title,
        comment=comment,
        amount=amount,
        amount_format=amount_format,
        hour_rate=hour_rate
    )


def NewConnectEntry(settings=None, global_list=None, client=None, project=None):
    """Return ConnectEntry according to settings."""
    is_settings = type(settings) is Settings
    is_client = type(client) is Client

    if not is_settings or not is_client:
        return ConnectEntry()

    # get language from client
    lang = client.language

    # get replaces
    title = replacer(
        text=settings.defaults[lang].connectentry_title,
        settings=settings,
        global_list=global_list,
        client=client,
        project=project
    )
    comment = replacer(
        text=settings.defaults[lang].connectentry_comment,
        settings=settings,
        global_list=global_list,
        client=client,
        project=project
    )

    # get other values
    amount = settings.defaults[lang].get_connectentry_amount()
    amount_format = settings.defaults[lang].connectentry_amount_format
    is_time = settings.defaults[lang].get_connectentry_is_time()
    multiplicator = settings.defaults[lang].get_connectentry_multiplicator()

    # return entry with default values from settings default
    return ConnectEntry(
        title=title,
        comment=comment,
        amount=amount,
        amount_format=amount_format,
        is_time=is_time,
        multiplicator=multiplicator
    )


def PresetConnectEntry(
    entry_preset=None,
    settings=None,
    global_list=None,
    client=None,
    project=None
):
    """Return ConnectEntry according to settings."""
    if type(entry_preset) is not ConnectEntry:
        return NewConnectEntry(settings=settings, client=client, project=project)

    # get replaces
    title = replacer(
        text=entry_preset.title,
        settings=settings,
        global_list=global_list,
        client=client,
        project=project
    )
    comment = replacer(
        text=entry_preset.comment,
        settings=settings,
        global_list=global_list,
        client=client,
        project=project
    )

    # get other values
    id = entry_preset._id
    amount = entry_preset._amount
    amount_format = entry_preset.amount_format
    is_time = entry_preset._is_time
    multiplicator = entry_preset._multiplicator

    # return entry with default values from settings default
    return ConnectEntry(
        id=id,
        title=title,
        comment=comment,
        amount=amount,
        amount_format=amount_format,
        is_time=is_time,
        multiplicator=multiplicator
    )
