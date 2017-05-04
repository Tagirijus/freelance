"""Form for the Defaults."""

import curses
import npyscreen
import time


class DefaultChooseList(npyscreen.MultiLineAction):
    """The list holding the choosable default entries."""

    def actionHighlighted(self, act_on_this, keypress):
        """Do something, because a key was pressed."""
        # general was chosen
        if act_on_this == 'General defaults':
            # go to the Defaults_general form
            self.parent.parentApp.setNextForm('Defaults_general')
            self.parent.parentApp.switchFormNow()

        # client and project was chosen
        elif act_on_this == 'Client and project defaults':
            # go to the Defaults_clientproject form
            self.parent.parentApp.setNextForm('Defaults_clientproject')
            self.parent.parentApp.switchFormNow()

        # entry was chosen
        elif act_on_this == 'Entry defaults':
            # go to the Defaults_clientproject form
            self.parent.parentApp.setNextForm('Defaults_entry')
            self.parent.parentApp.switchFormNow()



class DefaultsForm(npyscreen.ActionFormV2):
    """Form for editing the defaults."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(DefaultsForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel
        })

    def create(self):
        """Create widgets."""
        self.choose_list = self.add(
            DefaultChooseList,
            values=[
                'General defaults',
                'Client and project defaults',
                'Entry defaults'
            ]
        )

    def on_ok(self, keypress=None):
        """Check and set values."""
        pass

    def on_cancel(self, keypress=None):
        """Go back without changing a thing."""
        # swtich back
        self.parentApp.setNextForm('Settings')
        self.parentApp.switchFormNow()


class DefaultsGeneralForm(npyscreen.ActionFormV2):
    """Form for editing the general defaults."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(DefaultsGeneralForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel
        })

    def create(self):
        """Create widgets."""
        self.language = self.add(
            npyscreen.TitleText,
            name='Language:',
            begin_entry_at=20
        )
        self.offer_template = self.add(
            npyscreen.TitleFilenameCombo,
            name='Offer template:',
            begin_entry_at=20,
            must_exist=True
        )
        self.offer_filename = self.add(
            npyscreen.TitleText,
            name='Offer filename:',
            begin_entry_at=20
        )
        self.date_fmt = self.add(
            npyscreen.TitleText,
            name='Date format:',
            begin_entry_at=20
        )
        self.commodity = self.add(
            npyscreen.TitleText,
            name='Commodity:',
            begin_entry_at=20
        )

    def on_cancel(self, keypress=None):
        """Go back without changing a thing."""
        # swtich back
        self.parentApp.setNextForm('Defaults')
        self.parentApp.switchFormNow()


class DefaultsClientProjectForm(npyscreen.ActionFormV2):
    """Form for editing the client and project defaults."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(DefaultsClientProjectForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel
        })

    def on_cancel(self, keypress=None):
        """Go back without changing a thing."""
        # swtich back
        self.parentApp.setNextForm('Defaults')
        self.parentApp.switchFormNow()


class DefaultsEntryForm(npyscreen.ActionFormV2):
    """Form for editing the entry defaults."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(DefaultsEntryForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel
        })

    def on_cancel(self, keypress=None):
        """Go back without changing a thing."""
        # swtich back
        self.parentApp.setNextForm('Defaults')
        self.parentApp.switchFormNow()
