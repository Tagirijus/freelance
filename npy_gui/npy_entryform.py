"""Form for the entries."""

from general.functions import PresetBaseEntry
from general.functions import PresetMultiplyEntry
from general.functions import PresetConnectEntry
import npyscreen


class TitleMultiLineEdit(npyscreen.TitleText):
    """Titled MultiLineEdit."""

    _entry_type = npyscreen.MultiLineEdit
    scroll_exit = True

    def reformat(self):
        """Reformat the content."""
        self.entry_widget.full_reformat()


class BaseEntryForm(npyscreen.ActionFormWithMenus):
    """Form for editing the BaseEntry."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(BaseEntryForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel,
            '^L': self.load_preset,
            '^F': self.clear_widget
        })

    def clear_widget(self, keypress=None):
        """Clear widget."""
        self.get_widget(self.editw).value = ''

    def change_type(self):
        """Change the type of the entry."""
        self.values_to_tmp()
        self.parentApp.tmpEntry_change_type = True
        self.parentApp.setNextForm('EntryChoose')
        self.parentApp.switchFormNow()

    def replace_str(self):
        """Replace the strings."""
        self.values_to_tmp()

        self.parentApp.tmpEntry = PresetBaseEntry(
            entry_preset=self.parentApp.tmpEntry,
            settings=self.parentApp.S,
            global_list=self.parentApp.L,
            client=self.parentApp.tmpClient,
            project=self.parentApp.tmpProject
        )

        self.beforeEditing()

    def load_preset(self, keypress=None):
        """Load entry from presets."""
        self.values_to_tmp()
        self.parentApp.P_what = 'entry'
        self.parentApp.setNextForm('Presets')
        self.parentApp.switchFormNow()

    def save_preset(self):
        """Save entry to presets."""
        self.values_to_tmp()

        name = npyscreen.notify_input(
            'Name for the BaseEntry preset:'
        )

        if name:
            if self.parentApp.tmpEntry_offer_invoice == 'offer':
                added = self.parentApp.P.add_offer_entry(
                    entry=self.parentApp.tmpEntry.copy(),
                    name=name
                )
            else:
                added = self.parentApp.P.add_invoice_entry(
                    entry=self.parentApp.tmpEntry.copy(),
                    name=name
                )

            if not added:
                npyscreen.notify_confirm(
                    'BaseEntry not added. It probably already exists.',
                    form_color='DANGER'
                )

    def switch_to_help(self):
        """Switch to the help screen."""
        self.values_to_tmp()
        self.parentApp.load_helptext('help_baseentry.txt')
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
        self.m.addItem(text='Change type', onSelect=self.change_type, shortcut='t')
        self.m.addItem(text='Replace strings', onSelect=self.replace_str, shortcut='r')
        self.m.addItem(text='Load preset', onSelect=self.load_preset, shortcut='p')
        self.m.addItem(text='Save as preset', onSelect=self.save_preset, shortcut='P')
        self.m.addItem(text='Help', onSelect=self.switch_to_help, shortcut='h')
        self.m.addItem(text='Exit', onSelect=self.exit, shortcut='e')

        # create the input widgets
        self.title = self.add(
            npyscreen.TitleText,
            name='Title:',
            begin_entry_at=20
        )
        self.comment = self.add(
            TitleMultiLineEdit,
            name='Comment:',
            begin_entry_at=20,
            max_height=2
        )
        self.quantity = self.add(
            npyscreen.TitleText,
            name='Quantity:',
            begin_entry_at=20
        )
        self.quantity_format = self.add(
            npyscreen.TitleText,
            name='Quantity format:',
            begin_entry_at=20
        )
        self.quantity_b = self.add(
            npyscreen.TitleText,
            name='Quantity B:',
            begin_entry_at=20
        )
        self.quantity_b_format = self.add(
            npyscreen.TitleText,
            name='Quantity B format:',
            begin_entry_at=20
        )
        self.tax = self.add(
            npyscreen.TitleText,
            name='Tax rate:',
            begin_entry_at=20
        )
        self.time = self.add(
            npyscreen.TitleText,
            name='Time:',
            begin_entry_at=20
        )
        self.price = self.add(
            npyscreen.TitleText,
            name='Price (w/o tax):',
            begin_entry_at=20
        )

    def beforeEditing(self):
        """Get values from temp object."""
        self.title.value = self.parentApp.tmpEntry.title
        self.comment.value = self.parentApp.tmpEntry.comment
        self.comment.reformat()
        self.quantity.value = str(self.parentApp.tmpEntry.get_quantity())
        self.quantity_format.value = self.parentApp.tmpEntry.quantity_format
        self.quantity_b.value = str(self.parentApp.tmpEntry.get_quantity_b())
        self.quantity_b_format.value = self.parentApp.tmpEntry.quantity_b_format
        self.tax.value = str(self.parentApp.tmpEntry.get_tax_percent())
        self.time.value = str(self.parentApp.tmpEntry.get_time_raw())
        self.price.value = str(self.parentApp.tmpEntry.get_price_raw())

        # get actual caption for form
        if self.parentApp.tmpEntry_offer_invoice == 'offer':
            offerinvoice_title = self.parentApp.tmpOffer.title
        else:
            offerinvoice_title = self.parentApp.tmpInvoice.title

        self.name = '{} > Base entry ({})'.format(
            offerinvoice_title,
            self.parentApp.tmpEntry.title
        )

    def values_to_tmp(self, save=False):
        """Store values to temp variable."""
        # get values into tmp object
        self.parentApp.tmpEntry.title = self.title.value
        self.parentApp.tmpEntry.comment = self.comment.value.replace('\n', ' ')
        self.parentApp.tmpEntry.set_quantity(self.quantity.value)
        self.parentApp.tmpEntry.quantity_format = self.quantity_format.value
        self.parentApp.tmpEntry.set_quantity_b(self.quantity_b.value)
        self.parentApp.tmpEntry.quantity_b_format = self.quantity_b_format.value
        self.parentApp.tmpEntry.set_tax(self.tax.value)
        self.parentApp.tmpEntry.set_time(self.time.value)
        self.parentApp.tmpEntry.set_price(self.price.value)

        # save or not?
        if not save:
            return False

        # get the selected offer
        if self.parentApp.tmpEntry_offer_invoice == 'offer':
            offerinvoice = self.parentApp.tmpOffer
        else:
            offerinvoice = self.parentApp.tmpInvoice

        # it is a new entry
        if self.parentApp.tmpEntry_new:
            # append the entry to this project
            offerinvoice.append(
                entry=self.parentApp.tmpEntry
            )

            # update the _new boolean and get the new index
            self.parentApp.tmpEntry_new = False
            self.parentApp.tmpEntry_index = len(offerinvoice.get_entry_list()) - 1

            return True

        # existing entry just gets modified
        else:
            # get its id and modify it, if it exists
            if self.parentApp.tmpEntry_index < len(offerinvoice.get_entry_list()):
                offerinvoice.get_entry_list()[
                    self.parentApp.tmpEntry_index
                ] = self.parentApp.tmpEntry
                return True
            else:
                # entry index is out of range
                npyscreen.notify_confirm(
                    'Entry was not found.',
                    form_color='WARNING'
                )
                return False

    def on_ok(self, keypress=None):
        """Check values and store them."""
        allright = self.values_to_tmp(save=True)

        # check if it's allright and switch form then
        if allright:
            # get the selected offer
            project = self.parentApp.tmpProject

            # save the file
            self.parentApp.L.save_project_to_file(
                project=project
            )

            # switch back
            if self.parentApp.tmpEntry_offer_invoice == 'offer':
                self.parentApp.setNextForm('Offer')
                self.parentApp.switchFormNow()
            else:
                self.parentApp.setNextForm('Invoice')
                self.parentApp.switchFormNow()
        else:
            npyscreen.notify_confirm(
                'Something went wrong while adding or modifying the base entry!',
                form_color='WARNING'
            )

    def on_cancel(self, keypress=None):
        """Cancel and switch form."""
        if self.parentApp.tmpEntry_offer_invoice == 'offer':
            self.parentApp.setNextForm('Offer')
            self.parentApp.switchFormNow()
        else:
            self.parentApp.setNextForm('Invoice')
            self.parentApp.switchFormNow()


class MultiplyEntryForm(npyscreen.ActionFormWithMenus):
    """Form for editing the BaseEntry."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(MultiplyEntryForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel,
            '^L': self.load_preset,
            '^F': self.clear_widget
        })

    def clear_widget(self, keypress=None):
        """Clear widget."""
        self.get_widget(self.editw).value = ''

    def change_type(self):
        """Change the type of the entry."""
        self.values_to_tmp()
        self.parentApp.tmpEntry_change_type = True
        self.parentApp.setNextForm('EntryChoose')
        self.parentApp.switchFormNow()

    def replace_str(self):
        """Replace the strings."""
        self.values_to_tmp()

        self.parentApp.tmpEntry = PresetMultiplyEntry(
            entry_preset=self.parentApp.tmpEntry,
            settings=self.parentApp.S,
            global_list=self.parentApp.L,
            client=self.parentApp.tmpClient,
            project=self.parentApp.tmpProject
        )

        self.beforeEditing()

    def load_preset(self, keypress=None):
        """Load entry from presets."""
        self.values_to_tmp()
        self.parentApp.P_what = 'entry'
        self.parentApp.setNextForm('Presets')
        self.parentApp.switchFormNow()

    def save_preset(self):
        """Save entry to presets."""
        self.values_to_tmp()

        name = npyscreen.notify_input(
            'Name for the MultiplyEntry preset:'
        )

        if name:
            if self.parentApp.tmpEntry_offer_invoice == 'offer':
                added = self.parentApp.P.add_offer_entry(
                    entry=self.parentApp.tmpEntry.copy(),
                    name=name
                )
            else:
                added = self.parentApp.P.add_invoice_entry(
                    entry=self.parentApp.tmpEntry.copy(),
                    name=name
                )

            if not added:
                npyscreen.notify_confirm(
                    'MultiplyEntry not added. It probably already exists.',
                    form_color='DANGER'
                )

    def switch_to_help(self):
        """Switch to the help screen."""
        self.values_to_tmp()
        self.parentApp.load_helptext('help_multiplyentry.txt')
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
        self.m.addItem(text='Change type', onSelect=self.change_type, shortcut='t')
        self.m.addItem(text='Replace strings', onSelect=self.replace_str, shortcut='r')
        self.m.addItem(text='Load preset', onSelect=self.load_preset, shortcut='p')
        self.m.addItem(text='Save as preset', onSelect=self.save_preset, shortcut='P')
        self.m.addItem(text='Help', onSelect=self.switch_to_help, shortcut='h')
        self.m.addItem(text='Exit', onSelect=self.exit, shortcut='e')

        # create the input widgets
        self.title = self.add(
            npyscreen.TitleText,
            name='Title:',
            begin_entry_at=20
        )
        self.comment = self.add(
            TitleMultiLineEdit,
            name='Comment:',
            begin_entry_at=20,
            max_height=2
        )
        self.quantity = self.add(
            npyscreen.TitleText,
            name='Quantity:',
            begin_entry_at=20
        )
        self.quantity_format = self.add(
            npyscreen.TitleText,
            name='Quantity format:',
            begin_entry_at=20
        )
        self.quantity_b = self.add(
            npyscreen.TitleText,
            name='Quantity B:',
            begin_entry_at=20
        )
        self.quantity_b_format = self.add(
            npyscreen.TitleText,
            name='Quantity B format:',
            begin_entry_at=20
        )
        self.tax = self.add(
            npyscreen.TitleText,
            name='Tax rate:',
            begin_entry_at=20
        )
        self.hour_rate = self.add(
            npyscreen.TitleText,
            name='Hour rate:',
            begin_entry_at=20
        )

    def beforeEditing(self):
        """Get values from temp object."""
        self.title.value = self.parentApp.tmpEntry.title
        self.comment.value = self.parentApp.tmpEntry.comment
        self.comment.reformat()
        self.quantity.value = str(self.parentApp.tmpEntry.get_quantity())
        self.quantity_format.value = self.parentApp.tmpEntry.quantity_format
        self.quantity_b.value = str(self.parentApp.tmpEntry.get_quantity_b())
        self.quantity_b_format.value = self.parentApp.tmpEntry.quantity_b_format
        self.tax.value = str(self.parentApp.tmpEntry.get_tax_percent())
        self.hour_rate.value = str(self.parentApp.tmpEntry.get_hour_rate())

        # get actual caption for form
        if self.parentApp.tmpEntry_offer_invoice == 'offer':
            offerinvoice_title = self.parentApp.tmpOffer.title
        else:
            offerinvoice_title = self.parentApp.tmpInvoice.title
        self.name = '{} > Multiply entry ({})'.format(
            offerinvoice_title,
            self.parentApp.tmpEntry.title
        )

    def values_to_tmp(self, save=False):
        """Store values to temp variable."""
        # get values into tmp object
        self.parentApp.tmpEntry.title = self.title.value
        self.parentApp.tmpEntry.comment = self.comment.value.replace('\n', ' ')
        self.parentApp.tmpEntry.set_quantity(self.quantity.value)
        self.parentApp.tmpEntry.quantity_format = self.quantity_format.value
        self.parentApp.tmpEntry.set_quantity_b(self.quantity_b.value)
        self.parentApp.tmpEntry.quantity_b_format = self.quantity_b_format.value
        self.parentApp.tmpEntry.set_tax(self.tax.value)
        self.parentApp.tmpEntry.set_hour_rate(self.hour_rate.value)

        # save or not?
        if not save:
            return False

        # get the selected offer
        if self.parentApp.tmpEntry_offer_invoice == 'offer':
            offerinvoice = self.parentApp.tmpOffer
        else:
            offerinvoice = self.parentApp.tmpInvoice

        # it is a new entry
        if self.parentApp.tmpEntry_new:
            # append the entry to this project
            offerinvoice.append(
                entry=self.parentApp.tmpEntry
            )

            # update the _new boolean and get the new index
            self.parentApp.tmpEntry_new = False
            self.parentApp.tmpEntry_index = len(offerinvoice.get_entry_list()) - 1

            return True

        # existing entry just gets modified
        else:
            # get its id and modify it, if it exists
            if self.parentApp.tmpEntry_index < len(offerinvoice.get_entry_list()):
                offerinvoice.get_entry_list()[
                    self.parentApp.tmpEntry_index
                ] = self.parentApp.tmpEntry
                return True
            else:
                # entry index is out of range
                npyscreen.notify_confirm(
                    'Entry was not found.',
                    form_color='WARNING'
                )
                return False

    def on_ok(self, keypress=None):
        """Check values and store them."""
        allright = self.values_to_tmp(save=True)

        # check if it's allright and switch form then
        if allright:
            # get the selected offer
            project = self.parentApp.tmpProject

            # save the file
            self.parentApp.L.save_project_to_file(
                project=project
            )

            # switch back
            if self.parentApp.tmpEntry_offer_invoice == 'offer':
                self.parentApp.setNextForm('Offer')
                self.parentApp.switchFormNow()
            else:
                self.parentApp.setNextForm('Invoice')
                self.parentApp.switchFormNow()
        else:
            npyscreen.notify_confirm(
                'Something went wrong while adding or modifying the multiply entry!',
                form_color='WARNING'
            )

    def on_cancel(self, keypress=None):
        """Cancel and switch form."""
        if self.parentApp.tmpEntry_offer_invoice == 'offer':
            self.parentApp.setNextForm('Offer')
            self.parentApp.switchFormNow()
        else:
            self.parentApp.setNextForm('Invoice')
            self.parentApp.switchFormNow()


class ConnectEntryForm(npyscreen.ActionFormWithMenus):
    """Form for editing the BaseEntry."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(ConnectEntryForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel,
            '^L': self.load_preset,
            '^F': self.clear_widget
        })

    def clear_widget(self, keypress=None):
        """Clear widget."""
        self.get_widget(self.editw).value = ''

    def change_type(self):
        """Change the type of the entry."""
        self.values_to_tmp()
        self.parentApp.tmpEntry_change_type = True
        self.parentApp.setNextForm('EntryChoose')
        self.parentApp.switchFormNow()

    def replace_str(self):
        """Replace the strings."""
        self.values_to_tmp()

        self.parentApp.tmpEntry = PresetConnectEntry(
            entry_preset=self.parentApp.tmpEntry,
            settings=self.parentApp.S,
            global_list=self.parentApp.L,
            client=self.parentApp.tmpClient,
            project=self.parentApp.tmpProject
        )

        self.beforeEditing()

    def load_preset(self, keypress=None):
        """Load entry from presets."""
        self.values_to_tmp()
        self.parentApp.P_what = 'entry'
        self.parentApp.setNextForm('Presets')
        self.parentApp.switchFormNow()

    def save_preset(self):
        """Save entry to presets."""
        self.values_to_tmp()

        name = npyscreen.notify_input(
            'Name for the ConnectEntry preset:'
        )

        if name:
            if self.parentApp.tmpEntry_offer_invoice == 'offer':
                added = self.parentApp.P.add_offer_entry(
                    entry=self.parentApp.tmpEntry.copy(),
                    name=name
                )
            else:
                added = self.parentApp.P.add_invoice_entry(
                    entry=self.parentApp.tmpEntry.copy(),
                    name=name
                )

            if not added:
                npyscreen.notify_confirm(
                    'ConnectEntry not added. It probably already exists.',
                    form_color='DANGER'
                )

    def switch_to_help(self):
        """Switch to the help screen."""
        self.values_to_tmp()
        self.parentApp.load_helptext('help_connectentry.txt')
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
        self.m.addItem(text='Change type', onSelect=self.change_type, shortcut='t')
        self.m.addItem(text='Replace strings', onSelect=self.replace_str, shortcut='r')
        self.m.addItem(text='Load preset', onSelect=self.load_preset, shortcut='p')
        self.m.addItem(text='Save as preset', onSelect=self.save_preset, shortcut='P')
        self.m.addItem(text='Help', onSelect=self.switch_to_help, shortcut='h')
        self.m.addItem(text='Exit', onSelect=self.exit, shortcut='e')

        # create the input widgets
        self.title = self.add(
            npyscreen.TitleText,
            name='Title:',
            begin_entry_at=20
        )
        self.comment = self.add(
            TitleMultiLineEdit,
            name='Comment:',
            begin_entry_at=20,
            max_height=2
        )
        self.quantity = self.add(
            npyscreen.TitleText,
            name='Quantity:',
            begin_entry_at=20
        )
        self.quantity_format = self.add(
            npyscreen.TitleText,
            name='Quantity format:',
            begin_entry_at=20
        )
        self.quantity_b = self.add(
            npyscreen.TitleText,
            name='Quantity B:',
            begin_entry_at=20
        )
        self.quantity_b_format = self.add(
            npyscreen.TitleText,
            name='Quantity B format:',
            begin_entry_at=20
        )
        self.tax = self.add(
            npyscreen.TitleText,
            name='Tax rate:',
            begin_entry_at=20
        )
        self.multiplicator = self.add(
            npyscreen.TitleText,
            name='Multiplicator:',
            begin_entry_at=20
        )
        self.is_time = self.add(
            npyscreen.TitleMultiSelect,
            name='Is time:',
            begin_entry_at=20,
            max_height=2,
            scroll_exit=True,
            values=['enabled']
        )
        self.connected = self.add(
            npyscreen.TitleMultiSelect,
            name='Connect to:',
            begin_entry_at=20,
            scroll_exit=True
        )

    def beforeEditing(self):
        """Get values from temp object."""
        self.title.value = self.parentApp.tmpEntry.title
        self.comment.value = self.parentApp.tmpEntry.comment
        self.comment.reformat()
        self.quantity.value = str(self.parentApp.tmpEntry.get_quantity())
        self.quantity_format.value = self.parentApp.tmpEntry.quantity_format
        self.quantity_b.value = str(self.parentApp.tmpEntry.get_quantity_b())
        self.quantity_b_format.value = self.parentApp.tmpEntry.quantity_b_format
        self.tax.value = str(self.parentApp.tmpEntry.get_tax_percent())
        self.multiplicator.value = str(self.parentApp.tmpEntry.get_multiplicator())
        self.is_time.value = [0] if self.parentApp.tmpEntry.get_is_time() else []

        # get all entries into connected list

        # init connected variables
        self.connected.values = []
        self.connected.value = []
        self.connected_entries = []
        connected_list = self.parentApp.tmpEntry.get_connected()

        # check if offer or invoice and get its entry_list
        if self.parentApp.tmpEntry_offer_invoice == 'offer':
            entry_list = self.parentApp.tmpOffer.get_entry_list()
        else:
            entry_list = self.parentApp.tmpInvoice.get_entry_list()

        # iterate through all entries
        for e in entry_list:
            # only append it, if it's not its own id
            if e.get_id() != self.parentApp.tmpEntry.get_id():
                # append to the widget
                self.connected.values.append(e.title)

                # check if it's connected to the actual entry
                if e.get_id() in connected_list:
                    # if true, append it's index
                    self.connected.value.append(
                        len(self.connected.values) - 1
                    )

                # append original entry also to temp list
                self.connected_entries.append(e)

        # clear filter to not show double entries (npyscreen bug)
        self.connected.entry_widget.clear_filter()

        # get actual caption for form
        if self.parentApp.tmpEntry_offer_invoice == 'offer':
            offerinvoice_title = self.parentApp.tmpOffer.title
        else:
            offerinvoice_title = self.parentApp.tmpInvoice.title
        self.name = '{} > Connect entry ({})'.format(
            offerinvoice_title,
            self.parentApp.tmpEntry.title
        )

    def values_to_tmp(self, save=False):
        """Store values to temp variable."""
        # get values into tmp object
        self.parentApp.tmpEntry.title = self.title.value
        self.parentApp.tmpEntry.comment = self.comment.value.replace('\n', ' ')
        self.parentApp.tmpEntry.set_quantity(self.quantity.value)
        self.parentApp.tmpEntry.quantity_format = self.quantity_format.value
        self.parentApp.tmpEntry.set_quantity_b(self.quantity_b.value)
        self.parentApp.tmpEntry.quantity_b_format = self.quantity_b_format.value
        self.parentApp.tmpEntry.set_tax(self.tax.value)
        self.parentApp.tmpEntry.set_multiplicator(self.multiplicator.value)
        if self.is_time.value == [0]:
            self.parentApp.tmpEntry.set_is_time(True)
        else:
            self.parentApp.tmpEntry.set_is_time(False)

        # handle the connections - first empty the connected list
        self.parentApp.tmpEntry.disconnect_all_entries()

        # now connect the entries, chosen in the connected widget
        not_possible = []
        for i in self.connected.value:
            # connect the entry
            if self.parentApp.tmpEntry_offer_invoice == 'offer':
                entry_list = self.parentApp.tmpOffer.get_entry_list()
            else:
                entry_list = self.parentApp.tmpInvoice.get_entry_list()
            connected = self.parentApp.tmpEntry.connect_entry(
                entry_list=entry_list,
                entry_id=self.connected_entries[i].get_id()
            )

            # check if its possible
            if not connected:
                not_possible.append(self.connected_entries[i].title)

        # save or not?
        if not save:
            return False

        # give message, if some connections did not work
        if len(not_possible) > 0:
            npyscreen.notify_confirm(
                'Following connections did not work: ' +
                ', '.join(not_possible),
                form_color='WARNING'
            )

        # get the selected offer
        if self.parentApp.tmpEntry_offer_invoice == 'offer':
            offerinvoice = self.parentApp.tmpOffer
        else:
            offerinvoice = self.parentApp.tmpInvoice

        # it is a new entry
        if self.parentApp.tmpEntry_new:
            # append the entry to this project
            offerinvoice.append(
                entry=self.parentApp.tmpEntry
            )

            # update the _new boolean and get the new index
            self.parentApp.tmpEntry_new = False
            self.parentApp.tmpEntry_index = len(offerinvoice.get_entry_list()) - 1

            return True

        # existing entry just gets modified
        else:
            # get its id and modify it, if it exists
            if self.parentApp.tmpEntry_index < len(offerinvoice.get_entry_list()):
                offerinvoice.get_entry_list()[
                    self.parentApp.tmpEntry_index
                ] = self.parentApp.tmpEntry
                return True
            else:
                # entry index is out of range
                npyscreen.notify_confirm(
                    'Entry was not found.',
                    form_color='WARNING'
                )
                return False

    def on_ok(self, keypress=None):
        """Check values and store them."""
        allright = self.values_to_tmp(save=True)

        # check if it's allright and switch form then
        if allright:
            # get the selected offer
            project = self.parentApp.tmpProject

            # save the file
            self.parentApp.L.save_project_to_file(
                project=project
            )

            # switch back
            if self.parentApp.tmpEntry_offer_invoice == 'offer':
                self.parentApp.setNextForm('Offer')
                self.parentApp.switchFormNow()
            else:
                self.parentApp.setNextForm('Invoice')
                self.parentApp.switchFormNow()
        else:
            npyscreen.notify_confirm(
                'Something went wrong while adding or modifying the connect entry!',
                form_color='WARNING'
            )

    def on_cancel(self, keypress=None):
        """Cancel and switch form."""
        if self.parentApp.tmpEntry_offer_invoice == 'offer':
            self.parentApp.setNextForm('Offer')
            self.parentApp.switchFormNow()
        else:
            self.parentApp.setNextForm('Invoice')
            self.parentApp.switchFormNow()
