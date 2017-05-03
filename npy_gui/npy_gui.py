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

        self.update_values()

    def update_values(self):
        """Update the values."""
        self.values = L.client_list

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

        if len(L.client_list) > 0:
            self.update_values(client=L.client_list[0])

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
        self.m1.addItem(text='Help', onSelect=self.show_help, shortcut='h')
        self.m1.addItem(text='Settings', shortcut='s')
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

    def show_help(self, keypress=None):
        """Switch to help form."""
        self.parentApp.setNextForm('Help')
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
        helpfield = self.add(npyscreen.MultiLineEdit)
        helpfield.value = helptext
        helpfield.full_reformat()

    def afterEditing(self):
        """Return to main page."""
        self.parentApp.setNextForm('MAIN')
        self.parentApp.switchFormNow()


class FreelanceApplication(npyscreen.NPSAppManaged):
    """The main application object."""

    def onStart(self):
        """Create all the forms, which are needed."""
        self.addForm('MAIN', MainForm, name='Freelance')
        self.addForm('Help', HelpForm, name='Freelance - Help')
