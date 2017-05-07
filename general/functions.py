"""Modul holding the general functions."""

from datetime import datetime
from clients.client import Client
from clients.project import Project
from general.settings import Settings


def us(string=''):
    """Return string with underscores instead of whitespace."""
    return string.replace(' ', '_')


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
    title_replacer['YEAR'] = datetime.now().strftime('%Y')
    title_replacer['MONTH'] = datetime.now().strftime('%m')
    title_replacer['DAY'] = datetime.now().strftime('%d')
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
        hours_per_day=settings.defaults[lang].project_hours_per_day,
        work_days=settings.defaults[lang].project_work_days,
        wage=settings.defaults[lang].project_wage,
        minimum_days=settings.defaults[lang].project_minimum_days
    )


def move_offer(lis=None, index=None, direction=None):
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
