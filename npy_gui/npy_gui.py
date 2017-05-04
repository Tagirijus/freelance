"""The GUI for the Freelance programm - written with npyscreen."""

from clients.client import Client
# from clients.project import Project
from clients.list import List
# from clients.list import get_inactive_list
# from clients.list import activate_project
import curses
# from datetime import datetime
from general.preset import Preset
from general.settings import Settings
import npyscreen
# from offer.offer import Offer
# from offer.entries import BaseEntry
# from offer.entries import MultiplyEntry
# from offer.entries import ConnectEntry
import os
import time

S = Settings()
L = List(data_path=S.data_path)
P = Preset(data_path=S.data_path)


def can_be_dir(string):
    """Check if the given string could be a creatable dir or exists."""
    try:
        # check if it already exists
        if os.path.exists(string):
            if os.path.isdir(string):
                # it already exists and is a dir
                return True
            else:
                # it already exists, but is a file
                return False

        # it does not exist, try to create it
        os.mkdir(string)
        os.rmdir(string)
        return True
    except Exception:
        return False


class ClientList(npyscreen.MultiLineAction):
    """List of the clients."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(ClientList, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            curses.KEY_IC: self.add_client,
            curses.KEY_DC: self.delete_client,
            curses.KEY_RIGHT: self.h_exit_right  # switch to project list
        })

        # set up additional multiline options
        self.slow_scroll = True

    def update_values(self):
        """Update the values."""
        self.values = L.client_list
        self.display()

    def display_value(self, vl):
        """Display values."""
        return '{}: {}'.format(vl.client_id, vl.fullname())

    def h_cursor_line_up(self, ch):
        """Overwrite the method for key pressed up."""
        # get original method
        super(ClientList, self).h_cursor_line_up(ch)

        # append function for updating project list
        if len(L.client_list) > 0:
            self.parent.parentApp.getForm(
                'MAIN'
            ).projects_box.entry_widget.update_values(
                client=L.client_list[self.cursor_line]
            )

    def h_cursor_line_down(self, ch):
        """Overwrite the method for key pressed up."""
        # get original method
        super(ClientList, self).h_cursor_line_down(ch)

        # append function for updating project list
        if len(L.client_list) > 0:
            self.parent.parentApp.getForm(
                'MAIN'
            ).projects_box.entry_widget.update_values(
                client=L.client_list[self.cursor_line]
            )

    def add_client(self, keypress):
        """Add a new client."""
        npyscreen.notify('EINF was pressed (client)!')
        time.sleep(1)

    def delete_client(self, keypress):
        """Ask to delete the client and do it if yes."""
        npyscreen.notify('DEL was pressed (client)!')
        time.sleep(1)

    def actionHighlighted(self, act_on_this, keypress):
        """Do something, because a key was pressed."""
        npyscreen.notify(act_on_this.fullname() + ' chosen!')
        time.sleep(1)


class ClientListBox(npyscreen.BoxTitle):
    """Box holding the ClientList."""

    _contained_widget = ClientList


class ProjectList(npyscreen.MultiLineAction):
    """List of the projects."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(ProjectList, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            curses.KEY_IC: self.add_project,
            curses.KEY_DC: self.delete_project,
            curses.KEY_LEFT: self.h_exit_left  # switch to client list
        })

        # set up additional multiline options
        self.slow_scroll = True

    def update_values(self, client=None):
        """Update values according to client."""
        if type(client) is Client:
            self.values = L.get_client_projects(client=client)
        else:
            self.values = []
        self.display()

    def display_value(self, vl):
        """Display values."""
        return '{}'.format(vl.title)

    def add_project(self, keypress):
        """Add a new project."""
        npyscreen.notify('EINF was pressed!')
        time.sleep(1)

    def delete_project(self, keypress):
        """Ask to delete the project and do it if yes."""
        npyscreen.notify('DEL was pressed!')
        time.sleep(1)

    def actionHighlighted(self, act_on_this, keypress):
        """Do something, because a key was pressed."""
        npyscreen.notify(act_on_this.title + ' chosen!')
        time.sleep(1)


class ProjectListBox(npyscreen.BoxTitle):
    """Box holding the ProjectList."""

    _contained_widget = ProjectList


class MainForm(npyscreen.FormBaseNewWithMenus):
    """Main form."""

    def exit(self, keypress=None):
        """Exit the programm."""
        self.parentApp.setNextForm(None)
        self.parentApp.switchFormNow()

    def create(self):
        """Initialize the form with its widgets."""
        # set up key shortcuts
        self.add_handlers({
            curses.ascii.ESC: self.exit
        })

        # create the menu
        self.m1 = self.new_menu(name='Menu')
        self.m1.addItem(text='Create offer', shortcut='o')
        self.m1.addItem(text='Help', onSelect=self.switch_to_help, shortcut='h')
        self.m1.addItem(text='Settings', onSelect=self.switch_to_settings, shortcut='s')
        self.m1.addItem(text='Exit', onSelect=self.exit, shortcut='e')

        # create the box with the client list
        self.clients_box = self.add(
            ClientListBox,
            name='Clients',
            max_width=30
        )

        # create the box with the project list and update the list
        self.projects_box = self.add(
            ProjectListBox,
            name='Projects',
            relx=32,
            rely=2
        )

    def beforeEditing(self):
        """Get correct lists for clients and projects."""
        # update clients
        self.clients_box.entry_widget.update_values()
        # clear filter to not show doubled entries ... npyscreen bug?
        self.clients_box.entry_widget.clear_filter()

        # update projects
        # check if there are clients in the list
        clients_count = len(self.clients_box.entry_widget.values)
        if clients_count > 0:
            # select the last selected client, if len fits
            clients_selected = self.clients_box.entry_widget.cursor_line
            if clients_selected < clients_count:
                self.projects_box.entry_widget.update_values(
                    client=L.client_list[clients_selected]
                )
            # or select the last, if index was too high before
            else:
                self.projects_box.entry_widget.update_values(
                    client=L.client_list[clients_count - 1]
                )
        # no clients, so no projects
        else:
            self.projects_box.entry_widget.update_values()

    def switch_to_help(self, keypress=None):
        """Switch to help form."""
        self.parentApp.setNextForm('Help')
        self.parentApp.switchFormNow()

    def switch_to_settings(self, keypress=None):
        """Switch to the settigns form."""
        self.parentApp.setNextForm('Settings')
        self.parentApp.switchFormNow()


class HelpForm(npyscreen.Form):
    """The help form."""

    def create(self):
        """Create the form."""
        # create help text (load form file if possible)
        # check if the file exists
        if os.path.isfile(S.BASE_PATH + '/npy_gui/help.txt'):
            f = open(S.BASE_PATH + '/npy_gui/help.txt', 'r')
            helptext = f.read()
            f.close()
        else:
            helptext = 'Helpfile not found ... sorry! Time to learn by doing!'

        # create a textfield which holds the text
        helpfield = self.add(npyscreen.Pager)
        helpfield.values = helptext.split('\n')
        helpfield.autowrap = True

    def afterEditing(self):
        """Return to main page."""
        self.parentApp.setNextForm('MAIN')
        self.parentApp.switchFormNow()


class DefaultListAction(npyscreen.MultiLineAction):
    """The list for default objects."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(DefaultListAction, self).__init__(*args, **kwargs)

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
        npyscreen.notify(act_on_this + ' chosen (default)!')
        time.sleep(1)


class DefaultList(npyscreen.TitleMultiLine):
    """Inherit from TitleMultiLine, but get MultiLineAction."""

    _entry_type = DefaultListAction


class SettingsForm(npyscreen.ActionForm):
    """Settings form."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(SettingsForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel
        })

    def create(self):
        """Create the form."""
        self.data_path = self.add(
            npyscreen.TitleFilename,
            name='Data path:'
        )
        self.def_language = self.add(
            npyscreen.TitleSelectOne,
            name='Def. lang:',
            max_height=4,
            scroll_exit=True,
            values=['en', 'de']
        )
        self.inactive_dir = self.add(
            npyscreen.TitleText,
            name='Inactive dir:'
        )
        self.keep_offer_preset_date = self.add(
            npyscreen.TitleMultiSelect,
            name='Offer:',
            max_height=2,
            scroll_exit=True,
            values=['Keep offer date']
        )
        self.defaults = self.add(
            DefaultList,
            name='Defaults:',
            max_height=4,
            scroll_exit=True
        )

    def beforeEditing(self):
        """Get values from settings object."""
        self.data_path.value = S.data_path
        self.def_language.values = S.languages
        self.def_language.value = self.def_language.values.index(S.def_language)
        self.inactive_dir.value = S.inactive_dir
        self.keep_offer_preset_date.value = [0] if S.keep_offer_preset_date else []
        self.defaults.values = S.languages

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
        inactive_dir_correct = can_be_dir(S.data_path + inactive_dir)

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
                # no, I will go bakc to main screen
                self.editing = False
                # swtich back
                self.parentApp.setNextForm('MAIN')
                self.parentApp.switchFormNow()

        # it is creatable, set new values to settings object
        else:
            # new values
            S.data_path = data_path
            S.def_language = def_language
            S.inactive_dir = inactive_dir
            S.keep_offer_preset_date = keep_offer_preset_date

            # stor it and reload list and presets
            S.save_settings_to_file()
            L.reload(data_path=S.data_path)
            P.reload(data_path=S.data_path)

            # exit form
            self.editing = False
            # swtich back
            self.parentApp.setNextForm('MAIN')
            self.parentApp.switchFormNow()

    def on_cancel(self, keypress=None):
        """Go back without changing a thing."""
        # swtich back
        self.parentApp.setNextForm('MAIN')
        self.parentApp.switchFormNow()


class FreelanceApplication(npyscreen.NPSAppManaged):
    """The main application object."""

    def onStart(self):
        """Create all the forms, which are needed."""
        self.addForm('MAIN', MainForm, name='Freelance')
        self.addForm('Help', HelpForm, name='Freelance - Help')
        self.addForm('Settings', SettingsForm, name='Freelance - Settings')
