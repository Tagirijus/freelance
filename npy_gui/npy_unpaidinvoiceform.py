"""List all the unpaid invoices in a list."""

from datetime import date
import npyscreen


class UnpaidInvoiceList(npyscreen.MultiLineAction):
    """The list holding the unpaid invoices."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(UnpaidInvoiceList, self).__init__(*args, **kwargs)

        # set up additional multiline options
        self.slow_scroll = True

    def actionHighlighted(self, act_on_this, keypress=None):
        """Do something, because a key was pressed."""
        # get project of actual invoice
        self.parent.parentApp.tmpProject = act_on_this.get_project(
            global_list=self.parent.parentApp.L
        )
        self.parent.parentApp.tmpProject_new = False

        # get client of actual invoice
        self.parent.parentApp.tmpClient = act_on_this.get_client(
            global_list=self.parent.parentApp.L,
            project=self.parent.parentApp.tmpProject
        )
        self.parent.parentApp.tmpClient_new = False

        # get own
        self.parent.parentApp.tmpInvoice = act_on_this
        self.parent.parentApp.tmpInvoice_new = False
        self.parent.parentApp.tmpInvoice_index = (
            self.parent.parentApp.tmpProject.get_invoice_index(
                invoice=act_on_this
            )
        )

        # switch to invoice form
        self.parent.parentApp.setNextForm('Invoice')
        self.parent.parentApp.switchFormNow()

    def update_values(self):
        """Update the values."""
        # get list of unpaid invoices - sort by due date!
        self.values = self.parent.parentApp.L.get_unpaid_invoices()

        self.display()

        # clear filter for not showing doubled entries (npyscreen bug?)
        self.clear_filter()

    def display_value(self, vl):
        """Display values."""
        # get project of actual invoice
        project = vl.get_project(global_list=self.parent.parentApp.L)

        # get client of actual invoice
        client = vl.get_client(global_list=self.parent.parentApp.L, project=project)

        # get commodity
        commodity = vl.commodity

        # get tag for urgent invoices
        urgent = '! ' if vl.get_due_date() <= date.today() else ''

        # get total sum
        price = vl.get_price_total(project=project)
        tax = vl.get_price_tax_total(project=project)
        total = '{} {}'.format(price + tax, commodity)

        # get due date
        due_date = vl.get_due_date().strftime('%Y-%m-%d')

        return '{:2} {:>9}   {:10}   {:6}  -  {}'.format(
            urgent,
            total,
            due_date,
            '(' + vl.id + ')',
            project.title
        )


class UnpaidInvoiceForm(npyscreen.ActionFormWithMenus):
    """Form for choosing a preset."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(UnpaidInvoiceForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel
        })

    def exit(self):
        """Exit the programm."""
        self.parentApp.setNextForm(None)
        self.parentApp.switchFormNow()

    def create(self):
        """Create the widgets."""
        # the menu
        self.m = self.new_menu(name='Menu')
        self.m.addItem(text='Exit', onSelect=self.exit, shortcut='e')

        # the list
        self.unpaidinvoice_list = self.add(
            UnpaidInvoiceList,
            name='Unpaid invoices'
        )

    def beforeEditing(self):
        """Load stuff into the list."""
        self.unpaidinvoice_list.update_values()

    def on_ok(self, keypress=None):
        """Do on ok.."""
        self.parentApp.switchFormPrevious()

    def on_cancel(self, keypress=None):
        """Do the same as on ok.."""
        self.on_ok()
