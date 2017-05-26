"""Module for generating a proper ledgeradd command line output with given invoice."""

from general import check_objects


def generate_parameter(single_account='', settings=None, project=None, invoice=None):
    """Generate parameter for ledgeradd according to given invoice."""
    is_settings = check_objects.is_settings(settings)
    is_project = check_objects.is_project(project)
    is_invoice = check_objects.is_invoice(invoice)

    if not is_settings or not is_project or not is_invoice:
        return False

    # cancel if there are no entries
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

    # now generate the entries / postings / accounts

    # the client account
    client_acc = project.client_id + ':'

    # the tax account
    tax_acc = settings.ledgeradd_tax_account + ':'

    # get name and price into list of tuples, if single_account == ''
    entries = []
    if single_account == '':
        for e in invoice.get_entry_list():
            name = e.title
            price = e.get_price(
                entry_list=invoice.get_entry_list(),
                wage=invoice.get_wage(project=project),
                round_prive=invoice.get_round_price()
            )

            entries.append(
                (
                    '{}{}'.format(
                        client_acc,
                        name
                    ),
                    str(price)
                )
            )

            # also add a posting for the tax, if it exists

            tax = e.get_price_tax(
                entry_list=invoice.get_entry_list(),
                wage=invoice.get_wage(project=project),
                round_prive=invoice.get_round_price()
            )

            if tax != 0:
                # append a posting for tax as well
                entries.append(
                    (
                        '{}{}{}'.format(
                            client_acc,
                            name,
                            tax_acc
                        ),
                        str(tax)
                    )
                )

    # otherwise get only name from single_account and price of whole invoice
    else:
        entries.append(
            (
                '{}{}'.format(
                    client_acc,
                    single_account
                ),
                str(invoice.get_price_total(
                    wage=invoice.get_wage(project=project),
                    project=project,
                    round_price=invoice.get_round_price()
                ))
            )
        )

        # also add tax, if it exists

        tax_total = invoice.get_price_total(
            wage=invoice.get_wage(project=project),
            project=project,
            round_price=invoice.get_round_price()
        )

        if tax_total != 0:
            entries.append(
                (
                    '{}{}{}'.format(
                        client_acc,
                        single_account,
                        tax_acc
                    ),
                    str(tax_total)
                )
            )

    # append the parameter for the account
    for e in entries:
        args.append('-acc "{}" "{}"'.format(e[0], e[1]))

    # append the receiving account
    args.append('-acc "{}"'.format(settings.ledgeradd_receiving_account))

    # ledgeradd has to run in non-GUI, quiet and forced
    args.append('-n')
    args.append('-q')
    args.append('-f')

    # return the mighty parameter as one string
    return ' '.join(args)
