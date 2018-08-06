"""Module holding the general functions."""

from clients.client import Client
from clients.project import Project
from datetime import date
from datetime import timedelta
from general.replacer import replacer
from general.settings import Settings
from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry
from offer.offerinvoice import Offer
from offer.offerinvoice import Invoice
import os


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
        attention=settings.defaults[lang].client_attention,
        name=settings.defaults[lang].client_name,
        family_name=settings.defaults[lang].client_family_name,
        street=settings.defaults[lang].client_street,
        post_code=settings.defaults[lang].client_post_code,
        city=settings.defaults[lang].client_city,
        tax_id=settings.defaults[lang].client_tax_id,
        language=lang,
        def_wage=settings.defaults[lang].get_project_wage(),
        def_commodity=settings.defaults[lang].commodity
    )


def NewProject(settings=None, global_list=None, client=None):
    """Return new project object according to given settings and client."""
    is_settings = type(settings) is Settings
    is_client = type(client) is Client

    # return empty project if no valid settings or client  object is given
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
        wage=client.get_def_wage(),
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
    replace_dict = replacer(
        settings=settings,
        global_list=global_list,
        client=client,
        project=project
    )

    title = settings.defaults[lang].offer_title.format(**replace_dict)
    comment = settings.defaults[lang].offer_comment.format(**replace_dict)
    comment_b = settings.defaults[lang].offer_comment_b.format(**replace_dict)

    # get other values
    date_fmt = settings.defaults[lang].date_fmt
    round_price = settings.defaults[lang].get_offer_round_price()

    # return new Offer object
    return Offer(
        title=title,
        comment=comment,
        comment_b=comment_b,
        date_fmt=date_fmt,
        date=date.today(),
        commodity=client.def_commodity,
        round_price=round_price
    )


def PresetOffer(
    offer_preset=None,
    settings=None,
    global_list=None,
    client=None,
    project=None,
    replace=False
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
    replace_dict = replacer(
        settings=settings,
        global_list=global_list,
        client=client,
        project=project,
        offerinvoice=offer_preset
    )

    title = offer_preset.title.format(**replace_dict)
    comment = offer_preset.comment.format(**replace_dict)
    comment_b = offer_preset.comment_b.format(**replace_dict)

    # dates
    off_date = offer_preset.get_date()
    if not replace and off_date is not None:
        off_date = date.today()
    elif replace and off_date is None:
        off_date = date.today()

    # get other values
    date_fmt = offer_preset.date_fmt
    wage = offer_preset.get_wage()
    commodity = offer_preset.commodity
    round_price = offer_preset.get_round_price()
    entry_list = offer_preset.get_entry_list()

    # return new Offer object
    return Offer(
        title=title,
        comment=comment,
        comment_b=comment_b,
        date_fmt=date_fmt,
        date=off_date,
        wage=wage,
        commodity=commodity,
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
    replace_dict = replacer(
        settings=settings,
        global_list=global_list,
        client=client,
        project=project
    )

    title = settings.defaults[lang].baseentry_title.format(**replace_dict)
    comment = settings.defaults[lang].baseentry_comment.format(**replace_dict)

    # get other values
    quantity = settings.defaults[lang].get_baseentry_quantity()
    quantity_format = settings.defaults[lang].baseentry_quantity_format
    time = settings.defaults[lang].get_baseentry_time()
    price = settings.defaults[lang].get_baseentry_price()

    # return entry with default values from settings default
    return BaseEntry(
        title=title,
        comment=comment,
        quantity=quantity,
        quantity_format=quantity_format,
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
    replace_dict = replacer(
        settings=settings,
        global_list=global_list,
        client=client,
        project=project
    )

    title = entry_preset.title.format(**replace_dict)
    comment = entry_preset.comment.format(**replace_dict)

    # get other values
    id = entry_preset._id
    quantity = entry_preset._quantity
    quantity_format = entry_preset.quantity_format
    quantity_b = entry_preset._quantity_b
    quantity_b_format = entry_preset.quantity_b_format
    time = entry_preset._time
    price = entry_preset._price

    # return entry with default values from settings default
    return BaseEntry(
        id=id,
        title=title,
        comment=comment,
        quantity=quantity,
        quantity_format=quantity_format,
        quantity_b=quantity_b,
        quantity_b_format=quantity_b_format,
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
    replace_dict = replacer(
        settings=settings,
        global_list=global_list,
        client=client,
        project=project
    )

    title = settings.defaults[lang].multiplyentry_title.format(**replace_dict)
    comment = settings.defaults[lang].multiplyentry_comment.format(**replace_dict)

    # get other values
    quantity = settings.defaults[lang].get_multiplyentry_quantity()
    quantity_format = settings.defaults[lang].multiplyentry_quantity_format
    hour_rate = settings.defaults[lang].get_multiplyentry_hour_rate()

    # return entry with default values from settings default
    return MultiplyEntry(
        title=title,
        comment=comment,
        quantity=quantity,
        quantity_format=quantity_format,
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
    replace_dict = replacer(
        settings=settings,
        global_list=global_list,
        client=client,
        project=project
    )

    title = entry_preset.title.format(**replace_dict)
    comment = entry_preset.comment.format(**replace_dict)

    # get other values
    id = entry_preset._id
    quantity = entry_preset._quantity
    quantity_format = entry_preset.quantity_format
    quantity_b = entry_preset._quantity_b
    quantity_b_format = entry_preset.quantity_b_format
    hour_rate = entry_preset._hour_rate

    # return entry with default values from settings default
    return MultiplyEntry(
        id=id,
        title=title,
        comment=comment,
        quantity=quantity,
        quantity_format=quantity_format,
        quantity_b=quantity_b,
        quantity_b_format=quantity_b_format,
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
    replace_dict = replacer(
        settings=settings,
        global_list=global_list,
        client=client,
        project=project
    )

    title = settings.defaults[lang].connectentry_title.format(**replace_dict)
    comment = settings.defaults[lang].connectentry_comment.format(**replace_dict)

    # get other values
    quantity = settings.defaults[lang].get_connectentry_quantity()
    quantity_format = settings.defaults[lang].connectentry_quantity_format
    is_time = settings.defaults[lang].get_connectentry_is_time()
    multiplicator = settings.defaults[lang].get_connectentry_multiplicator()

    # return entry with default values from settings default
    return ConnectEntry(
        title=title,
        comment=comment,
        quantity=quantity,
        quantity_format=quantity_format,
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
    replace_dict = replacer(
        settings=settings,
        global_list=global_list,
        client=client,
        project=project
    )

    title = entry_preset.title.format(**replace_dict)
    comment = entry_preset.comment.format(**replace_dict)

    # get other values
    id = entry_preset._id
    quantity = entry_preset._quantity
    quantity_format = entry_preset.quantity_format
    quantity_b = entry_preset._quantity_b
    quantity_b_format = entry_preset.quantity_b_format
    is_time = entry_preset._is_time
    multiplicator = entry_preset._multiplicator

    # return entry with default values from settings default
    return ConnectEntry(
        id=id,
        title=title,
        comment=comment,
        quantity=quantity,
        quantity_format=quantity_format,
        quantity_b=quantity_b,
        quantity_b_format=quantity_b_format,
        is_time=is_time,
        multiplicator=multiplicator
    )


def NewInvoice(settings=None, global_list=None, client=None, project=None):
    """Return new invoice object according to settings defaults."""
    # return empty invoice, if there is no correct settings object given
    is_settings = type(settings) is Settings
    is_client = type(client) is Client
    is_project = type(project) is Project

    if not is_settings or not is_project or not is_client:
        return Invoice()

    # get language from client
    lang = client.language

    # get replaces
    replace_dict = replacer(
        settings=settings,
        global_list=global_list,
        client=client,
        project=project
    )

    title = settings.defaults[lang].invoice_title.format(**replace_dict)
    id = settings.defaults[lang].invoice_id.format(**replace_dict)
    comment = settings.defaults[lang].invoice_comment.format(**replace_dict)
    comment_b = settings.defaults[lang].invoice_comment_b.format(**replace_dict)
    delivery = settings.defaults[lang].invoice_delivery.format(**replace_dict)
    ledger_comment = settings.defaults[lang].invoice_ledger_comment.format(**replace_dict)

    # date
    due_days = settings.defaults[lang].get_invoice_due_days()

    # get other values
    date_fmt = settings.defaults[lang].date_fmt
    round_price = settings.defaults[lang].get_invoice_round_price()

    # return new Invoice object
    return Invoice(
        title=title,
        id=id,
        comment=comment,
        comment_b=comment_b,
        date_fmt=date_fmt,
        date=date.today(),
        delivery=delivery,
        due_days=due_days,
        commodity=client.def_commodity,
        round_price=round_price,
        ledger_comment=ledger_comment
    )


def PresetInvoice(
    invoice_preset=None,
    settings=None,
    global_list=None,
    client=None,
    project=None,
    replace=False
):
    """Return new Invoice based on given invoice, but with string replacements."""
    if type(invoice_preset) is not Invoice:
        return NewInvoice(
            settings=settings,
            global_list=global_list,
            client=client,
            project=project
        )

    # get replaces
    replace_dict = replacer(
        settings=settings,
        global_list=global_list,
        client=client,
        project=project,
        offerinvoice=invoice_preset
    )

    title = invoice_preset.title.format(**replace_dict)
    id = invoice_preset.id.format(**replace_dict)
    comment = invoice_preset.comment.format(**replace_dict)
    comment_b = invoice_preset.comment_b.format(**replace_dict)
    delivery = invoice_preset.delivery.format(**replace_dict)
    ledger_comment = invoice_preset.ledger_comment.format(**replace_dict)

    # dates
    inv_date = invoice_preset.get_date()
    if not replace and inv_date is not None:
        inv_date = date.today()
    elif replace and inv_date is None:
        inv_date = date.today()

    due_days = invoice_preset.get_due_days()

    paid_date = invoice_preset.get_paid_date()
    if not replace and paid_date is not None:
        paid_date = inv_date

    # get other values
    date_fmt = invoice_preset.date_fmt
    wage = invoice_preset.get_wage()
    commodity = invoice_preset.commodity
    round_price = invoice_preset.get_round_price()
    entry_list = invoice_preset.get_entry_list()

    # return new Invoice object
    return Invoice(
        title=title,
        id=id,
        comment=comment,
        comment_b=comment_b,
        date_fmt=date_fmt,
        date=inv_date,
        delivery=delivery,
        due_days=due_days,
        paid_date=paid_date,
        wage=wage,
        commodity=commodity,
        round_price=round_price,
        entry_list=entry_list,
        ledger_comment=ledger_comment
    )
