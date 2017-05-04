"""Form for the settings."""

import curses
from general.default import Default
import npyscreen
from npy_gui.npy_functions import can_be_dir
import time


class DefaultsListAction(npyscreen.MultiLineAction):
    """The list for default objects."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(DefaultsListAction, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            curses.KEY_IC: self.add_lang,
            curses.KEY_DC: self.delete_lang
        })

    def display_value(self, vl):
        """Display the value."""
        return '[{}]'.format(vl)

    def add_lang(self, keypress):
        """Add a new language and edit it (switch to form)."""
        npyscreen.notify('Add (default)!')
        time.sleep(1)

    def delete_lang(self, keypress):
        """Ask and delete language if yes."""
        really = npyscreen.notify_yes_no(
            'Really delete this default pack?',
            title='Deleting default pack!',
            form_color='DANGER'
        )
        if really:
            npyscreen.notify('Deleted (default)!')
            time.sleep(1)
        else:
            npyscreen.notify('Not deleted (default)!')
            time.sleep(1)

    def actionHighlighted(self, act_on_this, keypress):
        """Do something, because a key was pressed."""
        # get the chosen default
        if act_on_this in self.parent.parentApp.S.defaults.keys():
            self.parent.parentApp.tmpDefault = self.parent.parentApp.S.defaults[
                act_on_this
            ]
        # or chose a new one, if something went wrong
        else:
            self.parent.parentApp.tmpDefault = Default()

        # switch to the default form
        self.parent.parentApp.setNextForm('Defaults')
        self.parent.parentApp.switchFormNow()


class TitleDefaultsList(npyscreen.TitleMultiLine):
    """Inherit from TitleMultiLine, but get MultiLineAction."""

    _entry_type = DefaultsListAction


class SettingsForm(npyscreen.ActionFormWithMenus):
    """Settings form."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(SettingsForm, self).__init__(*args, **kwargs)

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
        """Create the form."""
        # create the menu
        self.m = self.new_menu(name='Menu')
        self.m.addItem(text='Help', onSelect=self.switch_to_help, shortcut='h')
        self.m.addItem(text='Exit', onSelect=self.exit, shortcut='e')

        # create input widgets
        self.data_path = self.add(
            npyscreen.TitleFilename,
            name='Data path:',
            begin_entry_at=20
        )
        self.def_language = self.add(
            npyscreen.TitleSelectOne,
            name='Default language:',
            begin_entry_at=20,
            max_height=4,
            scroll_exit=True
        )
        self.inactive_dir = self.add(
            npyscreen.TitleText,
            name='Inactive dir:',
            begin_entry_at=20
        )
        self.keep_offer_preset_date = self.add(
            npyscreen.TitleMultiSelect,
            name='Offer:',
            begin_entry_at=20,
            max_height=2,
            scroll_exit=True,
            values=['Keep offer date']
        )
        self.defaults = self.add(
            TitleDefaultsList,
            name='Defaults:',
            begin_entry_at=20,
            max_height=4,
            scroll_exit=True
        )

    def switch_to_help(self):
        """Switch to the help screen."""
        self.parentApp.load_helptext('help_settings.txt')
        self.parentApp.setNextForm('Help')
        self.parentApp.switchFormNow()

    def beforeEditing(self):
        """Get values from settings object."""
        self.data_path.value = self.parentApp.S.data_path
        self.def_language.values = self.parentApp.S.languages
        self.def_language.value = self.def_language.values.index(
            self.parentApp.S.def_language
        )
        self.inactive_dir.value = self.parentApp.S.inactive_dir
        self.keep_offer_preset_date.value = (
            [0] if self.parentApp.S.keep_offer_preset_date else []
        )
        self.defaults.values = self.parentApp.S.languages

    def on_ok(self, keypress=None):
        """Do something because user pressed ok."""
        # get values into temp variables
        data_path = self.data_path.value.rstrip('/')
        def_language = self.def_language.values[self.def_language.value[0]]
        inactive_dir = self.inactive_dir.value
        keep_offer_preset_date = (True if self.keep_offer_preset_date.value == [0]
                                  else False)

        # check correctness of values
        data_path_correct = can_be_dir(data_path)
        inactive_dir_correct = can_be_dir(self.parentApp.S.data_path + inactive_dir)

        # some dir is not creatable
        if not data_path_correct or not inactive_dir_correct:
            message = npyscreen.notify_ok_cancel(
                ('Data path and/or inactive dir are no valid folder names! '
                 'Please change them!'),
                title='Wrong folder names!',
                form_color='WARNING'
            )
            if message:
                # ok, I will edit them again
                self.editing = True
            else:
                # no, I will go back to main screen
                self.editing = False
                # swtich back
                self.parentApp.setNextForm('MAIN')
                self.parentApp.switchFormNow()

        # it is creatable, set new values to settings object
        else:
            # new values
            self.parentApp.S.data_path = data_path
            self.parentApp.S.def_language = def_language
            self.parentApp.S.inactive_dir = inactive_dir
            self.parentApp.S.keep_offer_preset_date = keep_offer_preset_date

            # stor it and reload list and presets
            self.parentApp.S.save_settings_to_file()
            self.parentApp.L.reload(data_path=self.parentApp.S.data_path)
            self.parentApp.P.reload(data_path=self.parentApp.S.data_path)

            # exit form
            self.editing = False
            # swtich back
            self.parentApp.setNextForm('MAIN')
            self.parentApp.switchFormNow()

    def on_cancel(self, keypress=None):
        """Go back without changing a thing."""
        # exit form
        self.editing = False
        # swtich back
        self.parentApp.setNextForm('MAIN')
        self.parentApp.switchFormNow()
