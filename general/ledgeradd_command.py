"""Module for generating a proper ledgeradd command line output with given invoice."""

from general import check_objects


def generate_parameter(settings=None, project=None, invoice=None):
    """Generate parameter for ledgeradd according to given invoice."""
    is_settings = check_objects.is_settings(settings)
    is_project = check_objects.is_project(project)
    is_invoice = check_objects.is_invoice(invoice)

    if not is_settings or not is_project or not is_invoice:
        return False

    # also cancel if there are more than 4 entries, since the ledgeradd
    # programm can only handle 5 accounts and one has to be the receiving account
    if len(invoice.get_entry_list()) > 4:
        return False

    # of course: cancel if there are no entries at all, as well
    if len(invoice.get_entry_list()) == 0:
        return False

    # get all the data
    args = []

    # the date and state
    if invoice.get_paid_date() is None:
        args.append('-d "{}"'.format(invoice.get_date().strftime('%Y-%m-%d')))
        args.append('-aux "{}"'.format(invoice.get_date().strftime('%Y-%m-%d')))
        args.append('-u')
    else:
        args.append('-d "{}"'.format(invoice.get_date().strftime('%Y-%m-%d')))
        args.append('-aux "{}"'.format(invoice.get_paid_date().strftime('%Y-%m-%d')))

    # get the code
    if invoice.id:
        args.append('-c "{}"'.format(invoice.id))

    # get payee (project title)
    args.append('-p "{}"'.format(project.title))

    # now generate the entries

    # the client account
    client_acc = project.client_id + ':'

    # get name and price into list of tuples
    entries = []
    for e in invoice.get_entry_list():
        name = e.title
        price = e.get_price(
            entry_list=invoice.get_entry_list(),
            wage=invoice.get_wage(project=project),
            round_prive=invoice.get_round_price()
        )

        entries.append((name, str(price)))

    # account A
    if len(entries) >= 1:
        args.append('-A "{}{}" -Aa "-{}"'.format(
            client_acc,
            entries[0][0],
            entries[0][1]
        ))
    else:
        args.append('-A ""')

    # account B
    if len(entries) >= 2:
        args.append('-B "{}{}" -Ba "-{}"'.format(
            client_acc,
            entries[1][0],
            entries[1][1]
        ))
    else:
        args.append('-B ""')

    # account C
    if len(entries) >= 3:
        args.append('-C "{}{}" -Ca "-{}"'.format(
            client_acc,
            entries[2][0],
            entries[2][1]
        ))
    else:
        args.append('-C ""')

    # account D
    if len(entries) >= 4:
        args.append('-D "{}{}" -Da "-{}"'.format(
            client_acc,
            entries[3][0],
            entries[3][1]
        ))
    else:
        args.append('-D ""')

    # account E (has to be receiving account)
    args.append('-E "{}"'.format(settings.ledgeradd_receiving_account))

    # ledgeradd has to run in non-GUI, quiet and forced
    args.append('-n')
    args.append('-q')
    args.append('-F')

    # return the mighty parameter as one string
    return ' '.join(args)
