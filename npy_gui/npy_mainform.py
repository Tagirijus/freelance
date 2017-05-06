"""Main form for Freelance."""

from clients.client import Client
import curses
import npyscreen
import time


class ClientList(npyscreen.MultiLineAction):
    """List of the clients."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(ClientList, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            curses.KEY_IC: self.add_client,
            curses.KEY_DC: self.deactivate_client,
            curses.KEY_RIGHT: self.h_exit_right  # switch to project list
        })

        # set up additional multiline options
        self.slow_scroll = True

    def update_values(self):
        """Update the values."""
        self.values = self.parent.parentApp.L.client_list
        self.display()

    def display_value(self, vl):
        """Display values."""
        return '{}: {}'.format(vl.client_id, vl.fullname())

    def h_cursor_line_up(self, ch):
        """Overwrite the method for key pressed up."""
        # get original method
        super(ClientList, self).h_cursor_line_up(ch)

        # append function for updating project list
        if len(self.parent.parentApp.L.client_list) > 0:
            self.parent.parentApp.getForm(
                'MAIN'
            ).projects_box.entry_widget.update_values(
                client=self.parent.parentApp.L.client_list[self.cursor_line]
            )

    def h_cursor_line_down(self, ch):
        """Overwrite the method for key pressed up."""
        # get original method
        super(ClientList, self).h_cursor_line_down(ch)

        # append function for updating project list
        if len(self.parent.parentApp.L.client_list) > 0:
            self.parent.parentApp.getForm(
                'MAIN'
            ).projects_box.entry_widget.update_values(
                client=self.parent.parentApp.L.client_list[self.cursor_line]
            )

    def add_client(self, keypress):
        """Add a new client."""
        # get default values according to def language from the settings
        try:
            lang = self.parent.parentApp.S.def_language
            self.parent.parentApp.tmpClient = Client(
                company=self.parent.parentApp.S.defaults[lang].client_company,
                salutation=self.parent.parentApp.S.defaults[lang].client_salutation,
                name=self.parent.parentApp.S.defaults[lang].client_name,
                family_name=self.parent.parentApp.S.defaults[lang].client_family_name,
                street=self.parent.parentApp.S.defaults[lang].client_street,
                post_code=self.parent.parentApp.S.defaults[lang].client_post_code,
                city=self.parent.parentApp.S.defaults[lang].client_city,
                tax_id=self.parent.parentApp.S.defaults[lang].client_tax_id,
                language=self.parent.parentApp.S.defaults[lang].client_language
            )
        except Exception:
            # fallback if language does not exist (should not happen)
            self.parent.parentApp.tmpClient = Client()
        self.parent.parentApp.tmpClient_new = True
        self.parent.parentApp.getForm('Client').name = 'Freelance > Client (new)'

        # switch to the client form
        self.editing = False
        self.parent.parentApp.setNextForm('Client')
        self.parent.parentApp.switchFormNow()

    def deactivate_client(self, keypress):
        """Ask to delete the client and do it if yes."""
        really = npyscreen.notify_yes_no(
            'Really deactivate the client and all its projects?',
            form_color='WARNING'
        )

        # yepp, deactivate it
        if really:
            worked = self.parent.parentApp.L.deactivate_client(
                client=self.values[self.cursor_line],
                inactive_dir=self.parent.parentApp.S.inactive_dir
            )

            # something went wrong
            if not worked:
                npyscreen.notify_confirm(
                    'Client not properly deactivated, woops!',
                    form_color='WARNING'
                )

    def actionHighlighted(self, act_on_this, keypress):
        """Do something, because a key was pressed."""
        try:
            # get the actual client into temp client
            self.parent.parentApp.tmpClient = act_on_this.copy()
            self.parent.parentApp.tmpClient_new = False

            # switch to the client form
            self.editing = False
            self.parent.parentApp.setNextForm('Client')
            self.parent.parentApp.switchFormNow()
        except Exception:
            npyscreen.notify_confirm(
                'Somethign went wrong, sorry!',
                form_color='WARNING'
            )


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
            curses.KEY_DC: self.deactivate_project,
            curses.KEY_LEFT: self.h_exit_left  # switch to client list
        })

        # set up additional multiline options
        self.slow_scroll = True

    def update_values(self, client=None):
        """Update values according to client."""
        if type(client) is Client:
            self.values = self.parent.parentApp.L.get_client_projects(client=client)
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

    def deactivate_project(self, keypress):
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

    def switch_to_help(self):
        """Switch to help form."""
        self.parentApp.load_helptext('help_main.txt')
        self.parentApp.setNextForm('Help')
        self.parentApp.switchFormNow()

    def switch_to_settings(self):
        """Switch to the settigns form."""
        self.parentApp.setNextForm('Settings')
        self.parentApp.switchFormNow()

    def exit(self):
        """Exit the programm."""
        self.parentApp.setNextForm(None)
        self.parentApp.switchFormNow()

    def create(self):
        """Initialize the form with its widgets."""
        # create the menu
        self.m = self.new_menu(name='Menu')
        self.m.addItem(text='Create offer', shortcut='o')
        self.m.addItem(text='Help', onSelect=self.switch_to_help, shortcut='h')
        self.m.addItem(text='Settings', onSelect=self.switch_to_settings, shortcut='s')
        self.m.addItem(text='Exit', onSelect=self.exit, shortcut='e')

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
        # also set old selection again
        cursor_save = self.clients_box.entry_widget.cursor_line
        self.clients_box.entry_widget.clear_filter()
        self.clients_box.entry_widget.cursor_line = cursor_save

        # update projects
        # check if there are clients in the list
        clients_count = len(self.clients_box.entry_widget.values)
        if clients_count > 0:
            # select the last selected client, if len fits
            clients_selected = self.clients_box.entry_widget.cursor_line
            if clients_selected < clients_count:
                self.projects_box.entry_widget.update_values(
                    client=self.parentApp.L.client_list[clients_selected]
                )
            # or select the last, if index was too high before
            else:
                self.projects_box.entry_widget.update_values(
                    client=self.parentApp.L.client_list[clients_count - 1]
                )
        # no clients, so no projects
        else:
            self.projects_box.entry_widget.update_values()
        # clear filter to not show doubled entries ... npyscreen bug?
        self.projects_box.entry_widget.clear_filter()
