"""
Module for the replacer function.

I seperated it from the functions module to not have
circular dependencies issues, since functions AND offer
export need it.
"""

from datetime import date
from general import check_objects


class ReplacementDict(dict):
    """A dict with a __missing__ method."""

    def __missing__(self, key):
        """Return the key instead."""
        return '{' + str(key).replace('#', '') + '}'


def replacer(
    text=None,
    settings=None,
    global_list=None,
    client=None,
    project=None,
    offerinvoice=None
):
    """
    Replace {...} inside text with stuff from client or project ... or the date.

    If no text is given, the function will return the replacement dict instead.
    Otherwise the given text will be returned with replaced values.
    """
    is_settings = check_objects.is_settings(settings)
    is_client = check_objects.is_client(client)
    is_project = check_objects.is_project(project)
    is_offerinvoice = (
        check_objects.is_offer(offerinvoice) or
        check_objects.is_invoice(offerinvoice)
    )
    is_global_list = check_objects.is_list(global_list)

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

        # get all invoices
        all_invoices = set([inv for i in all_projects for inv in i.get_invoice_list()])

        # general count stuff
        replace_me['CLIENT_COUNT'] = str(len(all_clients) + 1)
        replace_me['PROJECT_COUNT'] = str(len(all_projects) + 1)
        replace_me['OFFER_COUNT'] = str(
            settings.get_offer_count_offset() + len(all_offers) + 1
        )

        # try to get highest invoice id, if it's number
        try:
            ids = [0 if inv.id == '' else int(inv.id) for inv in all_invoices]
            highest = max(ids)
            replace_me['INVOICE_COUNT'] = str(
                highest + 1
            )

        # otherwise just calculate it with the settings invoice count offset
        except Exception as e:
            replace_me['INVOICE_COUNT'] = str(
                settings.get_invoice_count_offset() + len(all_invoices) + 1
            ) + str(e)

    # project related
    if is_project:
        replace_me['PROJECT_TITLE'] = project.title
        replace_me['PROJECT_OFFER_COUNT'] = str(len(project.get_offer_list()) + 1)
        replace_me['PROJECT_INVOICE_COUNT'] = str(len(project.get_invoice_list()) + 1)

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

    # offer / invoice related
    if is_offerinvoice and is_project:
        # general offer / invoice stuff
        replace_me['TITLE'] = offerinvoice.title

        replace_me['ID'] = offerinvoice.id

        replace_me['COMMENT'] = offerinvoice.comment

        # time related offer / invoice stuff
        if offerinvoice.date_fmt != '':
            replace_me['DATE'] = offerinvoice._date.strftime(offerinvoice.date_fmt)
        else:
            replace_me['DATE'] = offerinvoice._date

        replace_me['FINISH_DATE'] = offerinvoice.get_finish_date(project=project)

        replace_me['TIME_TOTAL'] = offerinvoice.get_time_total()

        # financial offer / invoice stuff
        if is_client and is_settings:
            commodity = settings.defaults[client.language].commodity
        elif not is_client and is_settings:
            commodity = settings.defaults['en'].commodity
        else:
            commodity = '$'

        replace_me['COMMODITY'] = commodity

        replace_me['WAGE'] = '{} {}/h'.format(
            offerinvoice.get_wage(project=project),
            commodity
        )

        price_total = offerinvoice.get_price_total(
            wage=offerinvoice.get_wage(project=project),
            project=project,
            round_price=offerinvoice.get_round_price()
        )
        replace_me['PRICE_TOTAL'] = '{} {}'.format(
            price_total,
            commodity
        )

        tax_total = offerinvoice.get_price_total(
            wage=offerinvoice.get_wage(project=project),
            project=project,
            tax=True,
            round_price=offerinvoice.get_round_price()
        )
        replace_me['TAX_TOTAL'] = '{} {}'.format(
            tax_total,
            commodity
        )

        replace_me['PRICE_TAX_TOTAL'] = '{} {}'.format(
            price_total + tax_total,
            commodity
        )

    if text is None:
        return replace_me
    else:
        return text.format(**replace_me)
