"""Form for the entries."""

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
            '^Q': self.on_cancel
        })

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
        self.amount = self.add(
            npyscreen.TitleText,
            name='Amount:',
            begin_entry_at=20
        )
        self.amount_format = self.add(
            npyscreen.TitleText,
            name='Amount format:',
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
        self.amount.value = str(self.parentApp.tmpEntry.get_amount())
        self.amount_format.value = self.parentApp.tmpEntry.amount_format
        self.tax.value = str(self.parentApp.tmpEntry.get_tax_percent())
        self.time.value = str(self.parentApp.tmpEntry.get_time_raw())
        self.price.value = str(self.parentApp.tmpEntry.get_price_raw())

    def values_to_tmp(self, save=False):
        """Store values to temp variable."""
        # get values into tmp object
        self.parentApp.tmpEntry.title = self.title.value
        self.parentApp.tmpEntry.comment = self.comment.value.replace('\n', ' ')
        self.parentApp.tmpEntry.set_amount(self.amount.value)
        self.parentApp.tmpEntry.amount_format = self.amount_format.value
        self.parentApp.tmpEntry.set_tax(self.tax.value)
        self.parentApp.tmpEntry.set_time(self.time.value)
        self.parentApp.tmpEntry.set_price(self.price.value)

        # save or not?
        if not save:
            return False

        # get the selected offer
        offer = self.parentApp.tmpOffer

        # it is a new entry
        if self.parentApp.tmpEntry_new:
            # append the entry to this project
            offer.append(
                entry=self.parentApp.tmpEntry
            )

            # update the _new boolean and get the new index
            self.parentApp.tmpEntry_new = False
            self.parentApp.tmpEntry_index = len(offer.get_entry_list()) - 1

            return True

        # existing entry just gets modified
        else:
            # get its id and modify it, if it exists
            if self.parentApp.tmpEntry_index < len(offer.get_entry_list()):
                offer.get_entry_list()[
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
            self.parentApp.setNextForm('Offer')
            self.parentApp.switchFormNow()
        else:
            npyscreen.notify_confirm(
                'Something went wrong while adding or modifying the entry!',
                form_color='WARNING'
            )

    def on_cancel(self, keypress=None):
        """Cancel and switch form."""
        self.parentApp.setNextForm('Offer')
        self.parentApp.switchFormNow()


class MultiplyEntryForm(npyscreen.ActionFormWithMenus):
    """Form for editing the BaseEntry."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(MultiplyEntryForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel
        })

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
        self.amount = self.add(
            npyscreen.TitleText,
            name='Amount:',
            begin_entry_at=20
        )
        self.amount_format = self.add(
            npyscreen.TitleText,
            name='Amount format:',
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
        self.amount.value = str(self.parentApp.tmpEntry.get_amount())
        self.amount_format.value = self.parentApp.tmpEntry.amount_format
        self.tax.value = str(self.parentApp.tmpEntry.get_tax_percent())
        self.hour_rate.value = str(self.parentApp.tmpEntry.get_hour_rate())

    def values_to_tmp(self, save=False):
        """Store values to temp variable."""
        # get values into tmp object
        self.parentApp.tmpEntry.title = self.title.value
        self.parentApp.tmpEntry.comment = self.comment.value.replace('\n', ' ')
        self.parentApp.tmpEntry.set_amount(self.amount.value)
        self.parentApp.tmpEntry.amount_format = self.amount_format.value
        self.parentApp.tmpEntry.set_tax(self.tax.value)
        self.parentApp.tmpEntry.set_hour_rate(self.hour_rate.value)

        # save or not?
        if not save:
            return False

        # get the selected offer
        offer = self.parentApp.tmpOffer

        # it is a new entry
        if self.parentApp.tmpEntry_new:
            # append the entry to this project
            offer.append(
                entry=self.parentApp.tmpEntry
            )

            # update the _new boolean and get the new index
            self.parentApp.tmpEntry_new = False
            self.parentApp.tmpEntry_index = len(offer.get_entry_list()) - 1

            return True

        # existing entry just gets modified
        else:
            # get its id and modify it, if it exists
            if self.parentApp.tmpEntry_index < len(offer.get_entry_list()):
                offer.get_entry_list()[
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
            self.parentApp.setNextForm('Offer')
            self.parentApp.switchFormNow()
        else:
            npyscreen.notify_confirm(
                'Something went wrong while adding or modifying the entry!',
                form_color='WARNING'
            )

    def on_cancel(self, keypress=None):
        """Cancel and switch form."""
        self.parentApp.setNextForm('Offer')
        self.parentApp.switchFormNow()


class ConnectEntryForm(npyscreen.ActionFormWithMenus):
    """Form for editing the BaseEntry."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(ConnectEntryForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel
        })

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
        self.amount = self.add(
            npyscreen.TitleText,
            name='Amount:',
            begin_entry_at=20
        )
        self.amount_format = self.add(
            npyscreen.TitleText,
            name='Amount format:',
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
        self.amount.value = str(self.parentApp.tmpEntry.get_amount())
        self.amount_format.value = self.parentApp.tmpEntry.amount_format
        self.tax.value = str(self.parentApp.tmpEntry.get_tax_percent())
        self.multiplicator.value = str(self.parentApp.tmpEntry.get_multiplicator())
        self.is_time.value = [0] if self.parentApp.tmpEntry.get_is_time() else []

        # get all entries into connected list

        # init connected variables
        self.connected.values = []
        self.connected.value = []
        self.connected_entries = []
        connected_list = self.parentApp.tmpEntry.get_connected()

        # iterate through all entries
        for e in self.parentApp.tmpOffer.get_entry_list():
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

    def values_to_tmp(self, save=False):
        """Store values to temp variable."""
        # get values into tmp object
        self.parentApp.tmpEntry.title = self.title.value
        self.parentApp.tmpEntry.comment = self.comment.value.replace('\n', ' ')
        self.parentApp.tmpEntry.set_amount(self.amount.value)
        self.parentApp.tmpEntry.amount_format = self.amount_format.value
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
            connected = self.parentApp.tmpEntry.connect_entry(
                entry_list=self.parentApp.tmpOffer.get_entry_list(),
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
        offer = self.parentApp.tmpOffer

        # it is a new entry
        if self.parentApp.tmpEntry_new:
            # append the entry to this project
            offer.append(
                entry=self.parentApp.tmpEntry
            )

            # update the _new boolean and get the new index
            self.parentApp.tmpEntry_new = False
            self.parentApp.tmpEntry_index = len(offer.get_entry_list()) - 1

            return True

        # existing entry just gets modified
        else:
            # get its id and modify it, if it exists
            if self.parentApp.tmpEntry_index < len(offer.get_entry_list()):
                offer.get_entry_list()[
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
            self.parentApp.setNextForm('Offer')
            self.parentApp.switchFormNow()
        else:
            npyscreen.notify_confirm(
                'Something went wrong while adding or modifying the entry!',
                form_color='WARNING'
            )

    def on_cancel(self, keypress=None):
        """Cancel and switch form."""
        self.parentApp.setNextForm('Offer')
        self.parentApp.switchFormNow()
