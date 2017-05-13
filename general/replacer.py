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
        return '{' + str(key) + '}'


def replacer(
    text=None,
    settings=None,
    client=None,
    project=None,
    global_list=None
):
    """
    Replace {...} inside text with stuff from client or project ... or the date.

    If no text is given, the function will return the replacement dict instead.
    Otherwise the given text will be returned with replaced values.
    """
    is_settings = check_objects.is_settings(settings)
    is_client = check_objects.is_client(client)
    is_project = check_objects.is_project(project)
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

        # count clients
        replace_me['CLIENT_COUNT'] = str(len(all_clients) + 1)
        replace_me['PROJECT_COUNT'] = str(len(all_projects) + 1)
        replace_me['OFFER_COUNT'] = str(
            settings.get_offer_count_offset() + len(all_offers) + 1
        )
        replace_me['INVOICE_COUNT'] = str(
            settings.get_invoice_count_offset() + len(all_invoices) + 1
        )

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

    if text is None:
        return replace_me
    else:
        return text.format(**replace_me)