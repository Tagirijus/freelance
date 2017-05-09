"""Modul holding the general functions."""

from clients.client import Client
from clients.project import Project
from datetime import date
from general.settings import Settings
from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry
from offer.offer import Offer
import os


def debug(text):
    """Write debug text into DEBUG.txt."""
    f = open('DEBUG.txt', 'w')
    f.write(str(text))
    f.close()


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


def us(string=''):
    """Return string with underscores instead of whitespace."""
    return string.replace(' ', '_')


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


def NewClient(settings=None):
    """Return new client object according to settings defaults."""
    # return empty client, if there is no correct settings object given
    if type(settings) is not Settings:
        return Client()

    # get language form settings file
    lang = settings.def_language

    # return client with default values according to chosen language
    return Client(
        company=settings.defaults[lang].client_company,
        salutation=settings.defaults[lang].client_salutation,
        name=settings.defaults[lang].client_name,
        family_name=settings.defaults[lang].client_family_name,
        street=settings.defaults[lang].client_street,
        post_code=settings.defaults[lang].client_post_code,
        city=settings.defaults[lang].client_city,
        tax_id=settings.defaults[lang].client_tax_id,
        language=settings.defaults[lang].client_language
    )


def NewProject(settings=None, client=None):
    """Return new project object according to given settings and client."""
    is_settings = type(settings) is Settings
    is_client = type(client) is Client

    # return empty project if no valid settings or client  object is given
    if not is_settings or not is_client:
        return Project()

    # get language from client
    lang = client.language

    # generate default title (according to replacements)
    title_replacer = {}
    title_replacer['YEAR'] = date.today().strftime('%Y')
    title_replacer['MONTH'] = date.today().strftime('%m')
    title_replacer['DAY'] = date.today().strftime('%d')
    title_replacer['CLIENT_COMPANY'] = client.company
    title_replacer['CLIENT_SALUT'] = client.salutation
    title_replacer['CLIENT_NAME'] = client.name
    title_replacer['CLIENT_FAMILY'] = client.family_name
    title_replacer['CLIENT_FULLNAME'] = client.fullname()
    title_replacer['CLIENT_STREET'] = client.street
    title_replacer['CLIENT_POST_CODE'] = client.post_code
    title_replacer['CLIENT_CITY'] = client.city
    title_replacer['CLIENT_TAX_ID'] = client.tax_id
    title = settings.defaults[lang].project_title.format(**title_replacer)

    return Project(
        client_id=client.client_id,
        title=title,
        hours_per_day=settings.defaults[lang].get_project_hours_per_day(),
        work_days=settings.defaults[lang].get_project_work_days(),
        wage=settings.defaults[lang].get_project_wage(),
        minimum_days=settings.defaults[lang].get_project_minimum_days()
    )


def NewOffer(settings=None, client=None, project=None):
    """Return new offer object according to settings defaults."""
    # return empty offer, if there is no correct settings object given
    is_settings = type(settings) is Settings
    is_client = type(client) is Client
    is_project = type(project) is Project

    if not is_settings or not is_project or not is_client:
        return Offer()

    # get language from client
    lang = client.language

    # generate default title (according to replacements)
    title_replacer = {}
    title_replacer['YEAR'] = date.today().strftime('%Y')
    title_replacer['MONTH'] = date.today().strftime('%m')
    title_replacer['DAY'] = date.today().strftime('%d')
    title_replacer['PROJECT'] = project.title
    title_replacer['CLIENT_COMPANY'] = client.company
    title_replacer['CLIENT_SALUT'] = client.salutation
    title_replacer['CLIENT_NAME'] = client.name
    title_replacer['CLIENT_FAMILY'] = client.family_name
    title_replacer['CLIENT_FULLNAME'] = client.fullname()
    title_replacer['CLIENT_STREET'] = client.street
    title_replacer['CLIENT_POST_CODE'] = client.post_code
    title_replacer['CLIENT_CITY'] = client.city
    title_replacer['CLIENT_TAX_ID'] = client.tax_id
    title = settings.defaults[lang].project_title.format(**title_replacer)

    # return offer with default values according to chosen language
    return Offer(
        title=title,
        date_fmt=settings.defaults[lang].date_fmt,
        wage=project.get_wage(),
        round_price=settings.defaults[lang].get_offer_round_price()
    )


def NewBaseEntry(settings=None, client=None):
    """Return BaseEntry according to settings."""
    is_settings = type(settings) is Settings
    is_client = type(client) is Client

    if not is_settings or not is_client:
        return BaseEntry()

    # get language from client
    lang = client.language

    # return entr with default values from settings default
    return BaseEntry(
        title=settings.defaults[lang].baseentry_title,
        comment=settings.defaults[lang].baseentry_comment,
        amount=settings.defaults[lang].get_baseentry_amount(),
        amount_format=settings.defaults[lang].baseentry_amount_format,
        time=settings.defaults[lang].get_baseentry_time(),
        price=settings.defaults[lang].get_baseentry_price()
    )


def NewMultiplyEntry(settings=None, client=None):
    """Return MultiplyEntry according to settings."""
    is_settings = type(settings) is Settings
    is_client = type(client) is Client

    if not is_settings or not is_client:
        return MultiplyEntry()

    # get language from client
    lang = client.language

    # return entr with default values from settings default
    return MultiplyEntry(
        title=settings.defaults[lang].multiplyentry_title,
        comment=settings.defaults[lang].multiplyentry_comment,
        amount=settings.defaults[lang].get_multiplyentry_amount(),
        amount_format=settings.defaults[lang].multiplyentry_amount_format,
        hour_rate=settings.defaults[lang].get_multiplyentry_hour_rate()
    )


def NewConnectEntry(settings=None, client=None):
    """Return ConnectEntry according to settings."""
    is_settings = type(settings) is Settings
    is_client = type(client) is Client

    if not is_settings or not is_client:
        return ConnectEntry()

    # get language from client
    lang = client.language

    # return entr with default values from settings default
    return ConnectEntry(
        title=settings.defaults[lang].connectentry_title,
        comment=settings.defaults[lang].connectentry_comment,
        amount=settings.defaults[lang].get_connectentry_amount(),
        amount_format=settings.defaults[lang].connectentry_amount_format,
        is_time=settings.defaults[lang].get_connectentry_is_time(),
        multiplicator=settings.defaults[lang].get_connectentry_multiplicator()
    )
