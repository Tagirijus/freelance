"""Form for the offer."""

import curses
import npyscreen
from general.functions import move_list_entry
from general.functions import NewBaseEntry
from general.functions import NewMultiplyEntry
from general.functions import NewConnectEntry
from general.functions import PresetOffer
from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry


class EntryChooseList(npyscreen.MultiLineAction):
    """The list holding the choosable types for the entries."""

    def actionHighlighted(self, act_on_this, keypress):
        """Do something, because a key was pressed."""
        if self.parent.parentApp.tmpEntry_offer_invoice == 'offer':
            offerinvoice = self.parent.parentApp.tmpOffer
        else:
            offerinvoice = self.parent.parentApp.tmpOffer

        # general was chosen
        if act_on_this == 'Base entry':

            # new or type change?
            if self.parent.parentApp.tmpEntry_change_type:

                # entry will be changed into other type
                self.parent.parentApp.tmpEntry_change_type = False
                new_entry = self.parent.parentApp.tmpEntry.return_changed_type(
                    into='BaseEntry',
                    entry_list=offerinvoice.get_entry_list(),
                    wage=offerinvoice.get_wage(
                        project=self.parent.parentApp.tmpProject
                    ),
                    project=self.parent.parentApp.tmpProject,
                    round_price=offerinvoice.get_round_price()
                )

            else:

                # get default BaseEntry
                new_entry = NewBaseEntry(
                    settings=self.parent.parentApp.S,
                    global_list=self.parent.parentApp.L,
                    client=self.parent.parentApp.tmpClient,
                    project=self.parent.parentApp.tmpProject
                )

            # finally get the new entry into temp
            self.parent.parentApp.tmpEntry = new_entry

            # go to the Defaults_general form
            self.parent.parentApp.setNextForm('BaseEntry')
            self.parent.parentApp.switchFormNow()

        # client and project was chosen
        elif act_on_this == 'Multiply entry':

            # new or type change?
            if self.parent.parentApp.tmpEntry_change_type:

                # entry will be changed into other type
                self.parent.parentApp.tmpEntry_change_type = False
                new_entry = self.parent.parentApp.tmpEntry.return_changed_type(
                    into='MultiplyEntry',
                    entry_list=offerinvoice.get_entry_list(),
                    wage=offerinvoice.get_wage(
                        project=self.parent.parentApp.tmpProject
                    ),
                    project=self.parent.parentApp.tmpProject,
                    round_price=offerinvoice.get_round_price()
                )

            else:

                # get default MultiplyEntry
                new_entry = NewMultiplyEntry(
                    settings=self.parent.parentApp.S,
                    global_list=self.parent.parentApp.L,
                    client=self.parent.parentApp.tmpClient,
                    project=self.parent.parentApp.tmpProject
                )

            # finally get the new entry into temp
            self.parent.parentApp.tmpEntry = new_entry

            # go to the Defaults_clientproject form
            self.parent.parentApp.setNextForm('MultiplyEntry')
            self.parent.parentApp.switchFormNow()

        # entry was chosen
        elif act_on_this == 'Connect entry':

            # new or type change?
            if self.parent.parentApp.tmpEntry_change_type:

                # entry will be changed into other type
                self.parent.parentApp.tmpEntry_change_type = False
                new_entry = self.parent.parentApp.tmpEntry.return_changed_type(
                    into='ConnectEntry',
                    entry_list=offerinvoice.get_entry_list(),
                    wage=offerinvoice.get_wage(
                        project=self.parent.parentApp.tmpProject
                    ),
                    project=self.parent.parentApp.tmpProject,
                    round_price=offerinvoice.get_round_price()
                )

            else:

                # get default ConnectEntry
                new_entry = NewConnectEntry(
                    settings=self.parent.parentApp.S,
                    global_list=self.parent.parentApp.L,
                    client=self.parent.parentApp.tmpClient,
                    project=self.parent.parentApp.tmpProject
                )

            # finally get the new entry into temp
            self.parent.parentApp.tmpEntry = new_entry

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
        self.parentApp.switchFormPrevious()

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
        title = vl.title[:29]

        price_com = self.parent.parentApp.S.defaults[
            self.parent.parentApp.tmpClient.language
        ].commodity

        amount = vl.get_amount_str()[:14]

        time = str(vl.get_time_zero(
            entry_list=self.parent.parentApp.tmpOffer.get_entry_list()
        ))

        price_amt = str(vl.get_price(
            entry_list=self.parent.parentApp.tmpOffer.get_entry_list(),
            wage=self.parent.parentApp.tmpOffer.get_wage(
                project=self.parent.parentApp.tmpProject,
            ),
            round_price=self.parent.parentApp.tmpOffer.get_round_price()
        ))

        price = '{} {}'.format(price_amt, price_com)

        price_tax_amt = str(vl.get_price_tax(
            entry_list=self.parent.parentApp.tmpOffer.get_entry_list(),
            wage=self.parent.parentApp.tmpOffer.get_wage(
                project=self.parent.parentApp.tmpProject,
            ),
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
        new_entry = self.values[self.cursor_line].copy(keep_id=False)

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
            self.parent.values_to_tmp()

            # get the actual offer into temp offer
            self.parent.parentApp.tmpEntry = act_on_this.copy()
            self.parent.parentApp.tmpEntry_new = False
            self.parent.parentApp.tmpEntry_index = self.cursor_line
            entry = self.parent.parentApp.tmpEntry

            # get the type
            if type(entry) is BaseEntry:
                form = 'BaseEntry'

            elif type(entry) is MultiplyEntry:
                form = 'MultiplyEntry'

            elif type(entry) is ConnectEntry:
                form = 'ConnectEntry'

            else:
                npyscreen.notify_confirm(
                    'Entry type unknown, canceling, sorry!',
                    form_color='DANGER'
                )
                return False

            # switch to the client form
            self.editing = False
            self.parent.parentApp.setNextForm(form)
            self.parent.parentApp.switchFormNow()
        except Exception as e:
            npyscreen.notify_confirm(
                'Something went wrong, sorry!' +
                'Error: ' + str(e),
                form_color='WARNING'
            )


class EntryListBox(npyscreen.BoxTitle):
    """Box holding the EntryList."""

    _contained_widget = EntryList


class TitleTextRefresh(npyscreen.TitleText):
    """TitleText which refreshes info view after leaving widget."""

    def when_value_edited(self):
        """Refresh info, when cursors moves."""
        self.parent.values_to_tmp()
        self.parent.update_info()


class TitleDateComboRefresh(npyscreen.TitleDateCombo):
    """TitleDateCombo which refreshes info view after leaving widget."""

    def when_value_edited(self):
        """Refresh info, when cursors moves."""
        self.parent.values_to_tmp()
        self.parent.update_info()


class TitleMultiSelectRefresh(npyscreen.TitleMultiSelect):
    """TitleMultiSelect which refreshes info view after leaving widget."""

    def when_value_edited(self):
        """Refresh info, when cursors moves."""
        self.parent.values_to_tmp()
        self.parent.update_info()


class TitleMultiLineEdit(npyscreen.TitleText):
    """Titled MultiLineEdit."""

    _entry_type = npyscreen.MultiLineEdit
    scroll_exit = True

    def reformat(self):
        """Reformat the content."""
        self.entry_widget.full_reformat()


class OfferForm(npyscreen.FormMultiPageActionWithMenus):
    """Form for editing the offer."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(OfferForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel,
            '^L': self.load_preset
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

    def replace_str(self):
        """Replace the strings."""
        self.values_to_tmp()

        self.parentApp.tmpOffer = PresetOffer(
            offer_preset=self.parentApp.tmpOffer,
            settings=self.parentApp.S,
            global_list=self.parentApp.L,
            client=self.parentApp.tmpClient,
            project=self.parentApp.tmpProject
        )

        self.beforeEditing()

    def load_preset(self, keypress=None):
        """Load offer from presets."""
        self.values_to_tmp()
        self.parentApp.P_what = 'offer'
        self.parentApp.setNextForm('Presets')
        self.parentApp.switchFormNow()

    def save_preset(self):
        """Save offer to presets."""
        self.values_to_tmp()

        name = npyscreen.notify_input(
            'Name for the offer preset:'
        )

        if name is not False:
            added = self.parentApp.P.add_offer(
                offer=self.parentApp.tmpOffer.copy(),
                name=name
            )

            npyscreen.notify_confirm(str(self.parentApp.P.offer_list))

            if not added:
                npyscreen.notify_confirm(
                    'Offer not added. It probably already exists.',
                    form_color='DANGER'
                )

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

    def export(self):
        """Export the offer."""
        self.values_to_tmp()
        self.parentApp.setNextForm('Export')
        self.parentApp.switchFormNow()

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
        self.m.addItem(text='Replace strings', onSelect=self.replace_str, shortcut='r')
        self.m.addItem(text='Load preset', onSelect=self.load_preset, shortcut='p')
        self.m.addItem(text='Save as preset', onSelect=self.save_preset, shortcut='P')
        self.m.addItem(text='Save', onSelect=self.save, shortcut='s')
        self.m.addItem(text='Export', onSelect=self.export, shortcut='^X')
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
            max_height=9
        )

        # create the info text section
        row_a = 11
        row_b = 12
        row_c = 13
        row_d = 14
        col_a = 35
        col_b = 51
        col_c = 61
        col_d = 73

        self.info_total_title = self.add_widget_intelligent(
            npyscreen.FixedText,
            value='Total:',
            editable=False,
            relx=col_a,
            rely=row_a
        )
        self.info_time = self.add_widget_intelligent(
            npyscreen.FixedText,
            editable=False,
            relx=col_b,
            rely=row_a
        )
        self.info_price = self.add_widget_intelligent(
            npyscreen.FixedText,
            editable=False,
            relx=col_c,
            rely=row_a
        )
        self.info_tax = self.add_widget_intelligent(
            npyscreen.FixedText,
            editable=False,
            relx=col_d,
            rely=row_a
        )
        self.info_price_total = self.add_widget_intelligent(
            npyscreen.TextTokens,
            editable=False,
            relx=col_c,
            rely=row_b
        )
        self.info_price_total.important = True
        self.info_finish_title = self.add_widget_intelligent(
            npyscreen.FixedText,
            value='Finish date:',
            editable=False,
            relx=col_a,
            rely=row_c
        )
        self.info_date = self.add_widget_intelligent(
            npyscreen.FixedText,
            editable=False,
            relx=col_b,
            rely=row_c
        )
        self.info_wage_title = self.add_widget_intelligent(
            npyscreen.FixedText,
            value='Wage / h:',
            editable=False,
            relx=col_a,
            rely=row_d
        )
        self.info_wage = self.add_widget_intelligent(
            npyscreen.FixedText,
            editable=False,
            relx=col_c,
            rely=row_d
        )
        self.info_wage_tax = self.add_widget_intelligent(
            npyscreen.FixedText,
            editable=False,
            relx=col_d,
            rely=row_d
        )
        self.seperation = self.add_widget_intelligent(
            npyscreen.FixedText,
            value='—' * 500,
            editable=False
        )

        # create additional widgets
        self.title = self.add_widget_intelligent(
            TitleTextRefresh,
            name='Title:',
            begin_entry_at=20
        )
        self.comment = self.add_widget_intelligent(
            TitleMultiLineEdit,
            name='Comment:',
            begin_entry_at=20,
            max_height=2,
            value=''
        )
        self.comment_b = self.add_widget_intelligent(
            TitleMultiLineEdit,
            name='Comment B:',
            begin_entry_at=20,
            max_height=2,
            value=''
        )
        self.date = self.add_widget_intelligent(
            TitleDateComboRefresh,
            name='Date:',
            begin_entry_at=20,
            max_width=59
        )
        self.date_fmt = self.add_widget_intelligent(
            TitleTextRefresh,
            name='Date fmt:',
            begin_entry_at=12,
            relx=60,
            rely=self.date.rely
        )
        self.wage = self.add_widget_intelligent(
            TitleTextRefresh,
            name='Wage:',
            begin_entry_at=20
        )
        self.round_price = self.add_widget_intelligent(
            TitleMultiSelectRefresh,
            name='Round price:',
            begin_entry_at=20,
            max_height=2,
            scroll_exit=True,
            values=['enabled']
        )

    def update_info(self):
        """Update info for the offer - summerize etc."""
        # get commodity for info text preparation
        price_com = self.parentApp.S.defaults[
            self.parentApp.tmpClient.language
        ].commodity

        # update info texts / summerizing stuff etc.
        time = self.parentApp.tmpOffer.get_time_total()

        price_val = self.parentApp.tmpOffer.get_price_total(
            project=self.parentApp.tmpProject
        )
        price = '{} {}'.format(
            price_val,
            price_com
        )

        tax_val = self.parentApp.tmpOffer.get_price_tax_total(
            project=self.parentApp.tmpProject
        )
        tax = '({} {})'.format(
            tax_val,
            price_com
        )

        price_total = '{} {}'.format(
            price_val + tax_val,
            price_com
        )

        date = self.parentApp.tmpOffer.get_finish_date(
            project=self.parentApp.tmpProject
        ).strftime('%d.%m.%Y')

        wage_price_val = self.parentApp.tmpOffer.get_hourly_wage(
            project=self.parentApp.tmpProject
        )
        wage_price = '{} {}'.format(
            wage_price_val,
            price_com
        )

        wage_tax_val = self.parentApp.tmpOffer.get_hourly_wage(
            project=self.parentApp.tmpProject,
            tax=True
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
        self.parentApp.tmpEntry_offer_invoice = 'offer'

        self.entries_box.entry_widget.update_values()
        self.title.value = self.parentApp.tmpOffer.title
        self.comment.value = self.parentApp.tmpOffer.comment
        self.comment.reformat()
        self.comment_b.value = self.parentApp.tmpOffer.comment_b
        self.comment_b.reformat()
        self.date.value = self.parentApp.tmpOffer.get_date()
        self.date_fmt.value = self.parentApp.tmpOffer.date_fmt
        self.wage.value = str(self.parentApp.tmpOffer.get_wage())
        self.round_price.value = [0] if self.parentApp.tmpOffer.get_round_price() else []

        self.update_info()

        # get actual caption for form
        self.name = '{} > {} > {}'.format(
            self.parentApp.tmpClient.fullname(),
            self.parentApp.tmpProject.title,
            self.parentApp.tmpOffer.title
        )

    def values_to_tmp(self, save=False):
        """Store values to temp variable."""
        # get values into tmp object
        self.parentApp.tmpOffer.set_entry_list(
            self.entries_box.entry_widget.values
        )
        self.parentApp.tmpOffer.title = self.title.value
        self.parentApp.tmpOffer.comment = self.comment.value.replace('\n', ' ')
        self.parentApp.tmpOffer.comment_b = self.comment_b.value.replace('\n', ' ')
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
