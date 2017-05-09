"""Form for the offer."""

import curses
import npyscreen
from general.functions import move_list_entry
from general.functions import NewBaseEntry
from general.functions import NewMultiplyEntry
from general.functions import NewConnectEntry
from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry


class EntryChooseList(npyscreen.MultiLineAction):
    """The list holding the choosable types for the entries."""

    def actionHighlighted(self, act_on_this, keypress):
        """Do something, because a key was pressed."""
        # get client
        client = self.parent.parentApp.L.get_client_by_id(
            client_id=self.parent.parentApp.tmpProject.client_id
        )

        # general was chosen
        if act_on_this == 'Base entry':
            # get default BaseEntry
            self.parent.parentApp.tmpEntry = NewBaseEntry(
                settings=self.parent.parentApp.S,
                client=client
            )

            # name form
            title_str = 'Freelance > Project > Offer > Base entry ({}: {})'.format(
                self.parent.parentApp.tmpClient.client_id,
                self.parent.parentApp.tmpOffer.title
            )
            self.parent.parentApp.getForm('BaseEntry').name = title_str

            # go to the Defaults_general form
            self.parent.parentApp.setNextForm('BaseEntry')
            self.parent.parentApp.switchFormNow()

        # client and project was chosen
        elif act_on_this == 'Multiply entry':
            # get default MultiplyEntry
            self.parent.parentApp.tmpEntry = NewMultiplyEntry(
                settings=self.parent.parentApp.S,
                client=client
            )

            # name form
            title_str = 'Freelance > Project > Offer > Multiply entry ({}: {})'.format(
                self.parent.parentApp.tmpClient.client_id,
                self.parent.parentApp.tmpOffer.title
            )
            self.parent.parentApp.getForm('MultiplyEntry').name = title_str

            # go to the Defaults_clientproject form
            self.parent.parentApp.setNextForm('MultiplyEntry')
            self.parent.parentApp.switchFormNow()

        # entry was chosen
        elif act_on_this == 'Connect entry':
            # get default ConnectEntry
            self.parent.parentApp.tmpEntry = NewConnectEntry(
                settings=self.parent.parentApp.S,
                client=client
            )

            # name form
            title_str = 'Freelance > Project > Offer > Connect entry ({}: {})'.format(
                self.parent.parentApp.tmpClient.client_id,
                self.parent.parentApp.tmpOffer.title
            )
            self.parent.parentApp.getForm('ConnectEntry').name = title_str

            # go to the Defaults_clientproject form
            self.parent.parentApp.setNextForm('ConnectEntry')
            self.parent.parentApp.switchFormNow()


class EntryChooseForm(npyscreen.ActionPopup):
    """Form for choosing the entry type, when adding."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(EntryChooseForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel
        })

        self.color = 'STANDOUT'

    def create(self):
        """Create the form."""
        # create the input widgets
        self.choose_list = self.add(
            EntryChooseList,
            values=[
                'Base entry',
                'Multiply entry',
                'Connect entry'
            ]
        )

    def on_ok(self, keypress=None):
        """Go back."""
        self.parentApp.setNextForm('Offer')
        self.parentApp.switchFormNow()

    def on_cancel(self, keypress=None):
        """Do the same as in on_ok."""
        self.on_ok(keypress)


class EntryList(npyscreen.MultiLineAction):
    """List holding entries of the offer."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(EntryList, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            curses.KEY_IC: self.add_entry,
            curses.KEY_DC: self.delete_entry,
            'c': self.copy_entry,
            '+': self.move_up,
            '-': self.move_down
        })

        # set up additional multiline options
        self.slow_scroll = True
        self.scroll_exit = True

    def move_up(self, keypress=None):
        """Move selected entry up in the list."""
        lis = self.parent.parentApp.tmpOffer.get_entry_list()

        # cancel if list is < 2
        if len(lis) < 2:
            return False

        # move selected item up
        new_index = move_list_entry(
            lis=lis,
            index=self.cursor_line,
            direction=1
        )

        # update view
        self.update_values()
        self.cursor_line = new_index

    def move_down(self, keypress=None):
        """Move selected entry down in the list."""
        lis = self.parent.parentApp.tmpOffer.get_entry_list()

        # cancel if list is < 2
        if len(lis) < 2:
            return False

        # move selected item up
        new_index = move_list_entry(
            lis=lis,
            index=self.cursor_line,
            direction=-1
        )

        # update view
        self.update_values()
        self.cursor_line = new_index

    def update_values(self):
        """Update list and refresh."""
        # get values
        self.values = self.parent.parentApp.tmpOffer.get_entry_list()
        self.display()

        # clear filter for not showing doubled entries (npyscreen bug?)
        self.clear_filter()

    def display_value(self, vl):
        """Display the entries."""
        # get client
        client = self.parent.parentApp.L.get_client_by_id(
            client_id=self.parent.parentApp.tmpProject.client_id
        )
        lang = client.language

        # values
        title = vl.title[:29]
        amount = vl.get_amount_str()[:14]
        time = str(vl.get_time_zero(
            entry_list=self.parent.parentApp.tmpOffer.get_entry_list()
        ))
        price_com = self.parent.parentApp.S.defaults[lang].commodity
        price_amt = str(vl.get_price(
            entry_list=self.parent.parentApp.tmpOffer.get_entry_list(),
            wage=self.parent.parentApp.tmpProject.get_wage(),
            round_price=self.parent.parentApp.tmpOffer.get_round_price()
        ))
        price = '{} {}'.format(price_amt, price_com)
        price_tax_amt = str(vl.get_price_tax(
            entry_list=self.parent.parentApp.tmpOffer.get_entry_list(),
            wage=self.parent.parentApp.tmpProject.get_wage(),
            round_price=self.parent.parentApp.tmpOffer.get_round_price()
        ))
        price_tax = '({} {})'.format(price_tax_amt, price_com)

        return '{:30} {:15} {:9} {:>11} {:>11}'.format(
            title,
            amount,
            time,
            price,
            price_tax
        )

    def copy_entry(self, keypress=None):
        """Copy the selected entry."""
        # cancel if there is nothign to copy
        if len(self.values) < 1:
            return False

        # get entry of the selected object
        new_entry = self.values[self.cursor_line].copy()

        # add the entry to the entry_list
        self.parent.parentApp.tmpOffer.append(
            entry=new_entry
        )

        # refresh
        self.update_values()

    def add_entry(self, keypress=None):
        """Add a new entry to the offer."""
        self.parent.parentApp.tmpEntry_new = True
        self.parent.parentApp.setNextForm('EntryChoose')
        self.parent.parentApp.switchFormNow()

    def delete_entry(self, keypress=None):
        """Delete the selected entry from the offer."""
        # get the selected offer
        offer = self.parent.parentApp.tmpOffer

        # cancel if entry list is empty
        if len(offer.get_entry_list()) < 1:
            return False

        entry = offer.get_entry_list()[self.cursor_line]

        really = npyscreen.notify_yes_no(
            'Really delete entry "{}" from the offer?'.format(entry.title),
            form_color='CRITICAL'
        )

        if really:
            # delete entry
            self.parent.parentApp.tmpOffer.pop(self.cursor_line)

            # refresh widget list
            self.update_values()

    def actionHighlighted(self, act_on_this, keypress=None):
        """Do something, because a key was pressed."""
        try:
            # get the offer
            offer = self.parent.parentApp.tmpOffer

            # get the actual offer into temp offer
            self.parent.parentApp.tmpEntry = act_on_this.copy()
            self.parent.parentApp.tmpEntry_new = False
            self.parent.parentApp.tmpEntry_index = self.cursor_line
            entry = self.parent.parentApp.tmpEntry

            # get the type
            if type(entry) is BaseEntry:
                form = 'BaseEntry'
                title_type = 'Base entry'

            elif type(entry) is MultiplyEntry:
                form = 'MultiplyEntry'
                title_type = 'Multiply entry'

            elif type(entry) is ConnectEntry:
                form = 'ConnectEntry'
                title_type = 'Connect entry'

            else:
                npyscreen.notify_confirm(
                    'Entry type unknown, canceling, sorry!',
                    form_color='DANGER'
                )
                return False

            # rename form and switch
            title_name = '{}: {}'.format(offer.title, act_on_this.title)
            self.parent.parentApp.getForm(
                form
            ).name = 'Freelance > Project > Offer > {} ({})'.format(
                title_type,
                title_name
            )

            # switch to the client form
            self.editing = False
            self.parent.parentApp.setNextForm(form)
            self.parent.parentApp.switchFormNow()
        except Exception:
            npyscreen.notify_confirm(
                'Something went wrong, sorry!',
                form_color='WARNING'
            )


class EntryListBox(npyscreen.BoxTitle):
    """Box holding the EntryList."""

    _contained_widget = EntryList


class OfferForm(npyscreen.FormMultiPageActionWithMenus):
    """Form for editing the offer."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(OfferForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel
        })

    def add_entry(self):
        """Add an entry."""
        self.entries_box.entry_widget.add_entry()

    def copy_entry(self):
        """Copy the selected entry."""
        self.entries_box.entry_widget.copy_entry()

    def del_entry(self):
        """Delete an offer."""
        self.entries_box.entry_widget.delete_entry()

    def save(self):
        """Save the offer / project."""
        allright = self.values_to_tmp(save=True)

        # check if it's allright
        if allright:
            # get the selected project
            project = self.parentApp.tmpProject

            # save the file
            self.parentApp.L.save_project_to_file(
                project=project
            )
        else:
            npyscreen.notify_confirm(
                'Something went wrong while adding or modifying the offer!',
                form_color='WARNING'
            )

    def switch_to_help(self):
        """Switch to the help screen."""
        self.values_to_tmp()
        self.parentApp.load_helptext('help_offer.txt')
        self.parentApp.setNextForm('Help')
        self.parentApp.switchFormNow()

    def exit(self):
        """Exit the programm."""
        self.parentApp.setNextForm(None)
        self.parentApp.switchFormNow()

    def create(self):
        """Create the form."""
        # create the menu
        self.m = self.new_menu(name='Menu')
        self.m.addItem(text='Add entry', onSelect=self.add_entry, shortcut='a')
        self.m.addItem(text='Copy entry', onSelect=self.copy_entry, shortcut='c')
        self.m.addItem(text='Delete entry', onSelect=self.del_entry, shortcut='A')
        self.m.addItem(text='Save', onSelect=self.save, shortcut='s')
        self.m.addItem(text='Help', onSelect=self.switch_to_help, shortcut='h')
        self.m.addItem(text='Exit', onSelect=self.exit, shortcut='e')

        # create the input widgets
        entries_title = '{:—<27}{:—<16}{:—<14}{:—<13}{}'.format(
            'Entries ',
            ' Amount ',
            ' Time ',
            ' Price ',
            ' Tax'
        )
        self.entries_box = self.add_widget_intelligent(
            EntryListBox,
            name=entries_title,
            max_height=10
        )

        # create the info text section
        col_a = 35
        col_b = 51
        col_c = 61
        col_d = 73

        self.info_title = self.add_widget_intelligent(
            npyscreen.FixedText,
            value='Sum:',
            editable=False,
            relx=col_a,
            rely=12
        )
        self.info_time = self.add_widget_intelligent(
            npyscreen.FixedText,
            editable=False,
            relx=col_b,
            rely=12
        )
        self.info_price = self.add_widget_intelligent(
            npyscreen.FixedText,
            editable=False,
            relx=col_c,
            rely=12
        )
        self.info_tax = self.add_widget_intelligent(
            npyscreen.FixedText,
            editable=False,
            relx=col_d,
            rely=12
        )
        self.info_total_title = self.add_widget_intelligent(
            npyscreen.FixedText,
            value='Total:',
            editable=False,
            relx=col_a,
            rely=12
        )
        self.info_price_total = self.add_widget_intelligent(
            npyscreen.FixedText,
            editable=False,
            relx=col_c,
            rely=13
        )
        self.info_finish_title = self.add_widget_intelligent(
            npyscreen.FixedText,
            value='Finish date:',
            editable=False,
            relx=col_a,
            rely=15
        )
        self.info_date = self.add_widget_intelligent(
            npyscreen.FixedText,
            editable=False,
            relx=col_b,
            rely=15
        )
        self.info_wage_title = self.add_widget_intelligent(
            npyscreen.FixedText,
            value='Wage / h:',
            editable=False,
            relx=col_a,
            rely=16
        )
        self.info_wage = self.add_widget_intelligent(
            npyscreen.FixedText,
            editable=False,
            relx=col_c,
            rely=16
        )
        self.info_wage_tax = self.add_widget_intelligent(
            npyscreen.FixedText,
            editable=False,
            relx=col_d,
            rely=16
        )
        self.seperation = self.add_widget_intelligent(
            npyscreen.FixedText,
            value='_' * 500,
            editable=False
        )

        # create additional widgets
        self.title = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Title:',
            begin_entry_at=20
        )
        self.date = self.add_widget_intelligent(
            npyscreen.TitleDateCombo,
            name='Date:',
            begin_entry_at=20
        )
        self.date_fmt = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Date fmt:',
            begin_entry_at=20
        )
        self.wage = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Wage:',
            begin_entry_at=20
        )
        self.round_price = self.add_widget_intelligent(
            npyscreen.TitleMultiSelect,
            name='Round price:',
            begin_entry_at=20,
            max_height=2,
            scroll_exit=True,
            values=['enabled']
        )

    def update_info(self):
        """Update info for the offer - summerize etc."""
        # get client and commodity for info text preparation
        client = self.parentApp.L.get_client_by_id(
            client_id=self.parentApp.tmpProject.client_id
        )
        lang = client.language
        price_com = self.parentApp.S.defaults[lang].commodity

        # update info texts / summerizing stuff etc.
        time = self.parentApp.tmpOffer.get_time_total()

        price_val = self.parentApp.tmpOffer.get_price_total(
            wage=self.parentApp.tmpProject.get_wage(),
            round_price=self.parentApp.tmpOffer.get_round_price()
        )
        price = '{} {}'.format(
            price_val,
            price_com
        )

        tax_val = self.parentApp.tmpOffer.get_price_tax_total(
            wage=self.parentApp.tmpProject.get_wage(),
            round_price=self.parentApp.tmpOffer.get_round_price()
        )
        tax = '({} {})'.format(
            tax_val,
            price_com
        )

        price_total = '{} {}'.format(
            price_val + tax_val,
            price_com
        )

        date = 'dd.mm.yyyy'  # work in progress

        wage_price_val = self.parentApp.tmpOffer.get_hourly_wage(
            wage=self.parentApp.tmpProject.get_wage(),
            round_price=self.parentApp.tmpOffer.get_round_price()
        )
        wage_price = '{} {}'.format(
            wage_price_val,
            price_com
        )

        wage_tax_val = self.parentApp.tmpOffer.get_hourly_wage(
            wage=self.parentApp.tmpProject.get_wage(),
            tax=True,
            round_price=self.parentApp.tmpOffer.get_round_price()
        )
        wage_tax = '({} {})'.format(
            wage_tax_val,
            price_com
        )

        self.info_time.value = time
        self.info_price.value = '{:>11}'.format(price[:11])
        self.info_tax.value = '{:>11}'.format(tax[:11])
        self.info_price_total.value = '{:>11}'.format(price_total[:11])
        self.info_date.value = date
        self.info_wage.value = '{:>11}'.format(wage_price[:11])
        self.info_wage_tax.value = '{:>11}'.format(wage_tax[:11])

    def beforeEditing(self):
        """Get values from temp object."""
        self.entries_box.entry_widget.update_values()
        self.title.value = self.parentApp.tmpOffer.title
        self.date.value = self.parentApp.tmpOffer.get_date()
        self.date_fmt.value = self.parentApp.tmpOffer.date_fmt
        self.wage.value = str(self.parentApp.tmpOffer.get_wage())
        self.round_price.value = [0] if self.parentApp.tmpOffer.get_round_price() else []

        self.update_info()

    def values_to_tmp(self, save=False):
        """Store values to temp variable."""
        # get values into tmp object
        self.parentApp.tmpOffer.set_entry_list(
            self.entries_box.entry_widget.values
        )
        self.parentApp.tmpOffer.title = self.title.value
        self.parentApp.tmpOffer.set_date(self.date.value)
        self.parentApp.tmpOffer.date_fmt = self.date_fmt.value
        self.parentApp.tmpOffer.set_wage(self.wage.value)
        if self.round_price.value == [0]:
            self.parentApp.tmpOffer.set_round_price(True)
        else:
            self.parentApp.tmpOffer.set_round_price(False)

        # save or not?
        if not save:
            return False

        # get the selected project
        project = self.parentApp.tmpProject

        # it is a new offer
        if self.parentApp.tmpOffer_new:
            # append the offer to this project
            project.append_offer(
                offer=self.parentApp.tmpOffer
            )

            # update the _new boolean and get the new index
            self.parentApp.tmpOffer_new = False
            self.parentApp.tmpOffer_index = len(project.get_offer_list()) - 1

            return True

        # existing offer just gets modified
        else:
            # get its id and modify it, if it exists
            if self.parentApp.tmpOffer_index < len(project.get_offer_list()):
                project.get_offer_list()[
                    self.parentApp.tmpOffer_index
                ] = self.parentApp.tmpOffer
                return True
            else:
                # offer index is out of range
                npyscreen.notify_confirm(
                    'Offer was not found.',
                    form_color='WARNING'
                )
                return False

    def on_ok(self, keypress=None):
        """Check values and store them."""
        allright = self.values_to_tmp(save=True)

        # check if it's allright and switch form then
        if allright:
            # get the selected project
            project = self.parentApp.tmpProject

            # save the file
            self.parentApp.L.save_project_to_file(
                project=project
            )

            # switch back
            self.parentApp.setNextForm('Project')
            self.parentApp.switchFormNow()
        else:
            npyscreen.notify_confirm(
                'Something went wrong while adding or modifying the offer!',
                form_color='WARNING'
            )

    def on_cancel(self, keypress=None):
        """Cancel and switch form."""
        self.parentApp.setNextForm('Project')
        self.parentApp.switchFormNow()
