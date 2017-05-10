"""Form for the settings."""

import curses
from general.default import Default
import npyscreen
from general.functions import can_be_dir


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

    def add_lang(self, keypress=None):
        """Add a new language and edit it (switch to form)."""
        self.parent.parentApp.tmpDefault = Default()
        self.parent.parentApp.tmpDefault_new = True

        # generate name for form
        tit = 'Freelance > Settings > Defaults ({})'
        self.parent.parentApp.getForm('Defaults').name = tit.format(
            self.parent.parentApp.tmpDefault.language
        )

        # switch to the default form
        self.parent.parentApp.setNextForm('Defaults')
        self.parent.parentApp.switchFormNow()

    def delete_lang(self, keypress):
        """Ask and delete language if yes."""
        try:
            what = self.values[self.cursor_line]
            is_en = what == 'en'
        except Exception:
            is_en = True

        # cancel if it's "en", which cannot be deleted
        if is_en:
            npyscreen.notify_confirm(
                '"en" cannot be deleted, sorry.',
                form_color='WARNING'
            )
            return False

        # it's seomthing else, go on
        really = npyscreen.notify_yes_no(
            'Really delete the \'' + what + '\' pack?',
            title='Deleting default pack!',
            form_color='DANGER'
        )
        if really:
            # yes, delete it
            deleted = self.parent.parentApp.S.remove_default(
                language=what,
                client_list=self.parent.parentApp.L.client_list
            )

            if deleted:
                # save the stuff into the files
                self.parent.parentApp.S.save_settings_to_file()
                self.parent.parentApp.L.save_client_list_to_file()

                # adjust the widget list of this form and refresh
                sel_value = self.parent.def_language.value[0]
                len_values = len(self.parent.parentApp.S.defaults)

                if sel_value >= len_values:
                    try:
                        new_val = self.def_language.values.index('en')
                        self.parent.def_language.value[0] = new_val
                    except Exception:
                        self.parent.def_language.value[0] = 0
                self.parent.display()
                return True
            else:
                # could not delete it .. don't know why
                npyscreen.notify_confirm(
                    'Could not delete it, sorry.',
                    form_color='WARNING'
                )
                return False
        else:
            # no, don't
            return False

    def actionHighlighted(self, act_on_this, keypress):
        """Do something, because a key was pressed."""
        # get the chosen default
        if act_on_this in self.parent.parentApp.S.defaults.keys():
            self.parent.parentApp.tmpDefault = self.parent.parentApp.S.defaults[
                act_on_this
            ].copy()
            self.parent.parentApp.tmpDefault_new = False
        # or chose a new one, if something went wrong
        else:
            self.parent.parentApp.tmpDefault = Default()
            self.parent.parentApp.tmpDefault_new = True

        # generate name for form
        tit = 'Freelance > Settings > Defaults ({})'
        self.parent.parentApp.getForm('Defaults').name = tit.format(
            self.parent.parentApp.tmpDefault.language
        )

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

    def add_lang(self):
        """Add language."""
        self.defaults.entry_widget.add_lang()

    def switch_to_help(self):
        """Switch to the help screen."""
        self.parentApp.load_helptext('help_settings.txt')
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
        self.m.addItem(text='Add language', onSelect=self.add_lang, shortcut='a')
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
            scroll_exit=True,
            value=[0]
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

    def beforeEditing(self):
        """Get values from settings object."""
        self.data_path.value = self.parentApp.S.data_path
        self.def_language.values = self.parentApp.S.get_languages()
        self.def_language.value[0] = self.def_language.values.index(
            self.parentApp.S.get_def_language()
        )
        self.inactive_dir.value = self.parentApp.S.inactive_dir
        self.keep_offer_preset_date.value = (
            [0] if self.parentApp.S.get_keep_offer_preset_date() else []
        )
        self.defaults.values = self.parentApp.S.get_languages()

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
        inactive_dir_correct = can_be_dir(self.parentApp.S.BASE_PATH + inactive_dir)

        # some dir is not creatable
        if not data_path_correct or not inactive_dir_correct:
            # what exactly is incorrect?
            if not data_path_correct and inactive_dir_correct:
                # only data_path is incorrect
                message_text = (
                    'Data path is no valid folder name! Please change it!'
                )
            elif data_path_correct and not inactive_dir_correct:
                # only inactive dir is incorrect
                message_text = (
                    'Inactive dir is no valid folder name! Please change it!'
                )
            elif not data_path_correct and not inactive_dir_correct:
                # both are incorrect
                message_text = (
                    'Data path and inactive dir do not have valid folder names! ' +
                    'Please change it!'
                )
            else:
                message_text = (
                    'Somethign is not right with the folder names ...'
                )

            # show the message
            message = npyscreen.notify_ok_cancel(
                message_text,
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
            self.parentApp.S.set_def_language(def_language)
            self.parentApp.S.inactive_dir = inactive_dir
            self.parentApp.S.set_keep_offer_preset_date(keep_offer_preset_date)

            # store it and reload list and presets
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
