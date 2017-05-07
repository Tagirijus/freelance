"""Form for the entries."""

import npyscreen


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
            npyscreen.TitleText,
            name='Comment:',
            begin_entry_at=20
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
        self.time = self.add(
            npyscreen.TitleText,
            name='Time:',
            begin_entry_at=20
        )
        self.price = self.add(
            npyscreen.TitleText,
            name='Price:',
            begin_entry_at=20
        )

    def beforeEditing(self):
        """Get values from temp object."""
        self.title.value = self.parentApp.tmpEntry.title
        self.comment.value = self.parentApp.tmpEntry.comment
        self.amount.value = str(self.parentApp.tmpEntry.get_amount())
        self.amount_format.value = self.parentApp.tmpEntry.amount_format
        self.time.value = str(self.parentApp.tmpEntry.get_time())
        self.price.value = str(self.parentApp.tmpEntry.get_price())

    def values_to_tmp(self, save=False):
        """Store values to temp variable."""
        # get values into tmp object
        self.parentApp.tmpEntry.title = self.title.value
        self.parentApp.tmpEntry.comment = self.comment.value
        self.parentApp.tmpEntry.set_amount(self.amount.value)
        self.parentApp.tmpEntry.amount_format = self.amount_format.value
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
            return True

        # existing entry just gets modified
        else:
            # get its id and modify it, if it exists
            if self.parentApp.tmpEntry_index < len(offer.entry_list):
                offer.entry_list[
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
            npyscreen.TitleText,
            name='Comment:',
            begin_entry_at=20
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
        self.hour_rate = self.add(
            npyscreen.TitleText,
            name='Hour rate:',
            begin_entry_at=20
        )

    def beforeEditing(self):
        """Get values from temp object."""
        self.title.value = self.parentApp.tmpEntry.title
        self.comment.value = self.parentApp.tmpEntry.comment
        self.amount.value = str(self.parentApp.tmpEntry.get_amount())
        self.amount_format.value = self.parentApp.tmpEntry.amount_format
        self.hour_rate.value = str(self.parentApp.tmpEntry.get_hour_rate())

    def values_to_tmp(self, save=False):
        """Store values to temp variable."""
        # get values into tmp object
        self.parentApp.tmpEntry.title = self.title.value
        self.parentApp.tmpEntry.comment = self.comment.value
        self.parentApp.tmpEntry.set_amount(self.amount.value)
        self.parentApp.tmpEntry.amount_format = self.amount_format.value
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
            return True

        # existing entry just gets modified
        else:
            # get its id and modify it, if it exists
            if self.parentApp.tmpEntry_index < len(offer.entry_list):
                offer.entry_list[
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
            npyscreen.TitleText,
            name='Comment:',
            begin_entry_at=20
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
        self.multiplicator = self.add(
            npyscreen.TitleText,
            name='Multiplicator:',
            begin_entry_at=20
        )
        self.is_time = self.add(
            npyscreen.TitleSelectOne,
            name='Is time:',
            begin_entry_at=20,
            values=['enabled'],
            value=[0]
        )

    def beforeEditing(self):
        """Get values from temp object."""
        self.title.value = self.parentApp.tmpEntry.title
        self.comment.value = self.parentApp.tmpEntry.comment
        self.amount.value = str(self.parentApp.tmpEntry.get_amount())
        self.amount_format.value = self.parentApp.tmpEntry.amount_format
        self.multiplicator.value = str(self.parentApp.tmpEntry.get_multiplicator())
        self.is_time.value = [0] if self.parentApp.tmpEntry.get_is_time() else []

    def values_to_tmp(self, save=False):
        """Store values to temp variable."""
        # get values into tmp object
        self.parentApp.tmpEntry.title = self.title.value
        self.parentApp.tmpEntry.comment = self.comment.value
        self.parentApp.tmpEntry.set_amount(self.amount.value)
        self.parentApp.tmpEntry.amount_format = self.amount_format.value
        self.parentApp.tmpEntry.set_multiplicator(self.multiplicator.value)
        if self.is_time.value == [0]:
            self.parentApp.tmpEntry.set_is_time(True)
        else:
            self.parentApp.tmpEntry.set_is_time(False)

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
            return True

        # existing entry just gets modified
        else:
            # get its id and modify it, if it exists
            if self.parentApp.tmpEntry_index < len(offer.entry_list):
                offer.entry_list[
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
