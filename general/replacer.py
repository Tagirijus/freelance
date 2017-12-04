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
        return '{' + str(key).replace('#', '', 1) + '}'


def code_str(text):
    """
    Code string so that it has correct newlines etc.

    There must be a better solution, but maybe I am too dumb here ...
    This function encodes to utf8, decodes with 'unicode_escape'. This way
    the exported string with the secretary module has correct newlines, tabs, etc.
    Unfortunately it also destroys the german umlauts. So my (probably very BAD)
    workaround is just to replace the wrong string with the correct umlaut string
    again, duh! (:

    ... help me .... :D
    """
    text = text.encode('utf8').decode('unicode_escape')
    text = text.replace('Ã¼', 'ü')
    text = text.replace('Ã¶', 'ö')
    text = text.replace('Ã¤', 'ä')
    text = text.replace('Ã', 'Ü')
    text = text.replace('Ã', 'Ö')
    text = text.replace('Ã', 'Ä')
    text = text.replace('Ã', 'ß')
    text = text.replace('Ã©', 'é')
    text = text.replace('Ã¨', 'è')
    text = text.replace('Ã', 'É')
    text = text.replace('Ã', 'È')
    return text


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
    is_global_list = check_objects.is_list(global_list)
    is_client = check_objects.is_client(client)
    is_project = check_objects.is_project(project)
    is_offerinvoice = (
        check_objects.is_offer(offerinvoice) or
        check_objects.is_invoice(offerinvoice)
    )

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
        replace_me['INVOICE_COUNT'] = str(
            settings.get_invoice_count_offset() + len(all_invoices) + 1
        )

        # try to get highest invoice id from existing ID strings
        got_ids = [0]
        for inv_id in [inv.id for inv in all_invoices]:
            try:
                got_ids.append(int(inv_id))
            except Exception:
                pass

        replace_me['INVOICE_COUNT_B'] = str(
            max(got_ids) + 1
        )

    # project related
    if is_project:
        replace_me['PROJECT_TITLE'] = project.title
        replace_me['PROJECT_OFFER_COUNT'] = str(len(project.get_offer_list()) + 1)
        replace_me['PROJECT_INVOICE_COUNT'] = str(len(project.get_invoice_list()) + 1)

    # client related
    if is_client:
        replace_me['CLIENT_ID'] = (
            code_str(client.client_id)
        )
        replace_me['CLIENT_COMPANY'] = (
            code_str(client.company)
        )
        replace_me['CLIENT_COMPANY_B'] = (
            code_str(client.company_b)
        )
        replace_me['CLIENT_ATTN'] = (
            code_str(client.attention)
        )
        replace_me['CLIENT_SALUT'] = (
            code_str(client.salutation)
        )
        replace_me['CLIENT_NAME'] = (
            code_str(client.name)
        )
        replace_me['CLIENT_FAMILY'] = (
            code_str(client.family_name)
        )
        replace_me['CLIENT_FULLNAME'] = (
            code_str(client.fullname())
        )
        replace_me['CLIENT_STREET'] = (
            code_str(client.street)
        )
        replace_me['CLIENT_POST_CODE'] = (
            code_str(client.post_code)
        )
        replace_me['CLIENT_CITY'] = (
            code_str(client.city)
        )
        replace_me['CLIENT_COUNTRY'] = (
            code_str(client.country)
        )
        replace_me['CLIENT_TAX_ID'] = (
            code_str(client.tax_id)
        )
        replace_me['CLIENT_ADDITIONAL_A'] = (
            code_str(client.additional_a)
        )
        replace_me['CLIENT_ADDITIONAL_B'] = (
            code_str(client.additional_b)
        )
        replace_me['CLIENT_ADDITIONAL_C'] = (
            code_str(client.additional_c)
        )

    # offer / invoice related
    if is_offerinvoice and is_project:
        # general offer / invoice stuff
        replace_me['TITLE'] = offerinvoice.title

        replace_me['ID'] = offerinvoice.id

        replace_me['COMMENT'] = offerinvoice.comment
        replace_me['COMMENT_B'] = offerinvoice.comment_b

        # dates

        # date is not None
        if offerinvoice.get_date() is not None:
            replace_me['DATE'] = offerinvoice.get_date().strftime(
                offerinvoice.date_fmt
            )
        else:
            replace_me['DATE'] = '-'

        # due date is not None
        if offerinvoice.get_due_date() is not None:
            replace_me['DUE_DATE'] = offerinvoice.get_due_date().strftime(
                offerinvoice.date_fmt
            )
        else:
            replace_me['DUE_DATE'] = '-'

        # get due days as well
        replace_me['DUE_DAYS'] = offerinvoice.get_due_days()

        # paid date is not None
        if offerinvoice.get_paid_date() is not None:
            replace_me['PAID_DATE'] = offerinvoice.get_paid_date().strftime(
                offerinvoice.date_fmt
            )
        else:
            replace_me['PAID_DATE'] = '-'

        # finish date
        replace_me['FINISH_DATE'] = offerinvoice.get_finish_date(
            project=project
        ).strftime(offerinvoice.date_fmt)

        # finish days
        replace_me['FINISH_DAYS'] = offerinvoice.get_finish_days(
            project=project
        )

        # delivery date
        replace_me['DELIVERY'] = offerinvoice.delivery

        # time related offer / invoice stuff
        replace_me['TIME_TOTAL'] = offerinvoice.get_time_total()

        replace_me['COMMODITY'] = offerinvoice.commodity

        replace_me['WAGE'] = '{} {}/h'.format(
            offerinvoice.get_wage(project=project),
            replace_me['COMMODITY']
        )

        price_total = offerinvoice.get_price_total(
            wage=offerinvoice.get_wage(project=project),
            project=project,
            round_price=offerinvoice.get_round_price()
        )
        replace_me['PRICE_TOTAL'] = '{} {}'.format(
            price_total,
            replace_me['COMMODITY']
        )

        tax_total = offerinvoice.get_price_tax_total(
            wage=offerinvoice.get_wage(project=project),
            project=project,
            round_price=offerinvoice.get_round_price()
        )
        replace_me['TAX_TOTAL'] = '{} {}'.format(
            tax_total,
            replace_me['COMMODITY']
        )

        replace_me['HAS_TAX'] = str(tax_total > 0)

        replace_me['PRICE_TAX_TOTAL'] = '{} {}'.format(
            price_total + tax_total,
            replace_me['COMMODITY']
        )

    if text is None:
        return replace_me
    else:
        return text.format(**replace_me)
