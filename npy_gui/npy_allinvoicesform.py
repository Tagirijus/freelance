"""List all the unpaid invoices in a list."""

from datetime import date
import npyscreen


class AllInvoicesList(npyscreen.MultiLineAction):
    """The list holding the unpaid invoices."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(AllInvoicesList, self).__init__(*args, **kwargs)

        # set up additional multiline options
        self.slow_scroll = True

    def update_values(self):
        """Update the values."""
        # get inactive and active as new list combined
        self.parent.the_list = self.parent.parentApp.L.get_active_and_inactive_list(
            settings=self.parent.parentApp.S
        )

        all_projects = self.parent.the_list.project_list

        # get list of unpaid invoices - sort by date reversed!
        self.values = list(
            set([inv for i in all_projects for inv in i.get_invoice_list()])
        )
        self.values = sorted(self.values, key=lambda x: x.get_date(), reverse=True)

        self.display()

        # clear filter for not showing doubled entries (npyscreen bug?)
        self.clear_filter()

    def display_value(self, vl):
        """Display values."""
        # get project of actual invoice
        project = vl.get_project(global_list=self.parent.the_list)

        # get client of actual invoice
        client = vl.get_client(global_list=self.parent.the_list, project=project)

        # get commodity
        commodity = vl.commodity

        # get tag for unpaid invoices
        unpaid = '*' if vl.get_paid_date() is None else ''

        # get tag for urgent invoices
        urgent = (
            '!'
            if vl.get_due_date() <= date.today()
            and unpaid == '*'
            else ' '
        )

        # combine urgent and unpaid
        urgent_unpaid = '{}{}'.format(urgent, unpaid)

        # get total sum
        price = vl.get_price_total(project=project)
        tax = vl.get_price_tax_total(project=project)
        total = '{} {}'.format(price + tax, commodity)

        # get date
        the_date = vl.get_date().strftime('%Y-%m-%d')

        return '{:2} {:>9}   {:10}   {:6}  -  {}'.format(
            urgent_unpaid,
            total,
            the_date,
            '(' + vl.id + ')',
            project.title
        )


class AllInvoicesForm(npyscreen.ActionFormWithMenus):
    """Form for choosing a preset."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(AllInvoicesForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel
        })

    def switch_to_help(self):
        """Switch to help form."""
        self.parentApp.load_helptext('help_allinvoices.txt')
        self.parentApp.setNextForm('Help')
        self.parentApp.switchFormNow()

    def exit(self):
        """Exit the programm."""
        self.parentApp.setNextForm(None)
        self.parentApp.switchFormNow()

    def create(self):
        """Create the widgets."""
        # the menu
        self.m = self.new_menu(name='Menu')
        self.m.addItem(text='Help', onSelect=self.switch_to_help, shortcut='h')
        self.m.addItem(text='Exit', onSelect=self.exit, shortcut='e')

        # the list
        self.allinvoices_list = self.add(
            AllInvoicesList,
            name='All invoices'
        )

    def beforeEditing(self):
        """Load stuff into the list."""
        self.allinvoices_list.update_values()

    def on_ok(self, keypress=None):
        """Do on ok.."""
        self.parentApp.switchFormPrevious()

    def on_cancel(self, keypress=None):
        """Do the same as on ok.."""
        self.on_ok()
