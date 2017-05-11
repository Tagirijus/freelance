"""Main form for Freelance."""

from clients.client import Client
import curses
from general.functions import NewClient
from general.functions import NewProject
import npyscreen
from clients.project import Project


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
        # save selection
        sel = self.cursor_line

        # get new values
        self.values = sorted(
            self.parent.parentApp.L.client_list,
            key=lambda x: x.client_id
        )
        self.display()

        # clear filter for not showing doubled entries (npyscreen bug?)
        self.clear_filter()

        # restore selection
        self.cursor_line = sel

    def display_value(self, vl):
        """Display values."""
        return '{}: {}'.format(vl.client_id, vl.fullname())

    def refresh_project_list(self):
        """Refresh project list."""
        # do it only if there are clients in the list
        if len(self.values) > 0:
            # correct cursor_line if it's now higher than length of values
            if self.cursor_line >= len(self.values):
                self.cursor_line = len(self.values) - 1

            # update the values
            self.parent.projects_box.entry_widget.update_values(
                client=self.values[self.cursor_line]
            )

            # get the nea title for the box widget
            self.parent.projects_box.name = 'Projects for {}, {}'.format(
                self.values[self.cursor_line].client_id,
                self.values[self.cursor_line].fullname()
            )

            # update the client
            client = self.values[self.cursor_line]
            self.parent.parentApp.tmpProject_client = client.copy()
            self.parent.parentApp.tmpClient = client.copy()

            # update the display
            self.parent.projects_box.display()

        # otherwise update it empty
        else:
            self.parent.projects_box.entry_widget.update_values()
            self.parent.projects_box.name = 'Projects'
            self.parent.parentApp.tmpProject_client = Client()
            self.parent.parentApp.tmpClient = Client()
            self.parent.projects_box.display()

        # clear filter for not showing doubled entries (npyscreen bug?)
        self.parent.projects_box.entry_widget.clear_filter()

    def h_cursor_line_up(self, ch):
        """Overwrite the method for key pressed up."""
        # get original method
        super(ClientList, self).h_cursor_line_up(ch)

        # append function for updating project list
        self.refresh_project_list()

    def h_cursor_line_down(self, ch):
        """Overwrite the method for key pressed up."""
        # get original method
        super(ClientList, self).h_cursor_line_down(ch)

        # append function for updating project list
        self.refresh_project_list()

    def add_client(self, keypress=None):
        """Add a new client."""
        # get default values according to def language from the settings
        self.parent.parentApp.tmpClient = NewClient(
            settings=self.parent.parentApp.S,
            global_list=self.parent.parentApp.L
        )

        self.parent.parentApp.tmpClient_new = True
        self.parent.parentApp.getForm('Client').name = 'Freelance > Client (NEW)'

        # switch to the client form
        self.editing = False
        self.parent.parentApp.setNextForm('Client')
        self.parent.parentApp.switchFormNow()

    def deactivate_client(self, keypress=None):
        """Ask to deactivate the client and do it if yes."""
        client = self.parent.parentApp.tmpProject_client
        client_str = '"{}: {}"'.format(client.client_id, client.fullname())
        really = npyscreen.notify_yes_no(
            'Really deactivate the client {} and all its projects?'.format(client_str),
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

            # ouhkaaaay
            else:
                self.update_values()
                self.refresh_project_list()

    def actionHighlighted(self, act_on_this, keypress=None):
        """Do something, because a key was pressed."""
        try:
            # get the actual client into temp client
            self.parent.parentApp.tmpClient = act_on_this.copy()
            self.parent.parentApp.tmpClient_new = False

            # rename form and switch
            title_name = '{}, {}'.format(act_on_this.client_id, act_on_this.fullname())
            self.parent.parentApp.getForm(
                'Client'
            ).name = 'Freelance > Client ({})'.format(title_name)

            # switch to the client form
            self.editing = False
            self.parent.parentApp.setNextForm('Client')
            self.parent.parentApp.switchFormNow()
        except Exception:
            npyscreen.notify_confirm(
                'Something went wrong, sorry!',
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
        # get new values
        if type(client) is Client:
            self.values = sorted(
                self.parent.parentApp.L.get_client_projects(client=client),
                key=lambda x: x.title
            )
        else:
            self.values = []

        self.display()

        # clear filter for not showing doubled entries (npyscreen bug?)
        self.clear_filter()

    def display_value(self, vl):
        """Display values."""
        return '{}'.format(vl.title)

    def add_project(self, keypress=None):
        """Add a new project."""
        # get selected client id
        client_list = self.parent.clients_box.entry_widget
        no_client = len(client_list.values) < 1

        # cancel, because no client available / selected
        if no_client:
            npyscreen.notify_confirm(
                'Create / select a client first.'
            )
            return False

        # get selected client
        try:
            client = client_list.values[client_list.cursor_line]
        except Exception:
            npyscreen.notify_confirm(
                'Could not get client.',
                form_color='WARNING'
            )
            return False

        # get default values according to language from the client and settings defaults
        self.parent.parentApp.tmpProject = NewProject(
            settings=self.parent.parentApp.S,
            global_list=self.parent.parentApp.L,
            client=client
        )

        self.parent.parentApp.tmpProject_new = True
        title_name = self.parent.parentApp.tmpProject_client.fullname() + ', NEW'
        self.parent.parentApp.getForm(
            'Project'
        ).name = 'Freelance > Project ({})'.format(title_name)

        # switch to the client form
        self.editing = False
        self.parent.parentApp.setNextForm('Project')
        self.parent.parentApp.switchFormNow()

    def deactivate_project(self, keypress=None):
        """Ask to deactivate the project and do it if yes."""
        # cancel if there are no projects
        if len(self.values) < 1:
            return False

        project = self.values[self.cursor_line]
        project_str = '"{}: {}"'.format(project.client_id, project.title)
        really = npyscreen.notify_yes_no(
            'Really deactivate the project {}?'.format(project_str),
            form_color='WARNING'
        )

        # yepp, deactivate it
        if really:
            worked = self.parent.parentApp.L.deactivate_project(
                project=self.values[self.cursor_line],
                inactive_dir=self.parent.parentApp.S.inactive_dir
            )

            # something went wrong
            if not worked:
                npyscreen.notify_confirm(
                    'Project not properly deactivated, woops!',
                    form_color='WARNING'
                )

            # ouhkaaaay
            else:
                # get selected client
                try:
                    client_list = self.parent.clients_box.entry_widget
                    client = client_list.values[client_list.cursor_line]
                except Exception:
                    npyscreen.notify_confirm(
                        'Could not get client.',
                        form_color='WARNING'
                    )
                    return False

                # refresh list
                self.update_values(client=client)

    def actionHighlighted(self, act_on_this, keypress=None):
        """Do something, because a key was pressed."""
        try:
            # get the actual project into temp project
            self.parent.parentApp.tmpProject = act_on_this.copy()
            self.parent.parentApp.tmpProject_new = False

            # rename form and switch
            title_name = '{}, {}'.format(act_on_this.client_id, act_on_this.title)
            self.parent.parentApp.getForm(
                'Project'
            ).name = 'Freelance > Project ({})'.format(title_name)

            # switch to the project form
            self.editing = False
            self.parent.parentApp.setNextForm('Project')
            self.parent.parentApp.switchFormNow()
        except Exception:
            npyscreen.notify_confirm(
                'Something went wrong, sorry!',
                form_color='WARNING'
            )


class ProjectListBox(npyscreen.BoxTitle):
    """Box holding the ProjectList."""

    _contained_widget = ProjectList


class MainForm(npyscreen.FormBaseNewWithMenus):
    """Main form."""

    def add_client(self):
        """Add a client."""
        self.clients_box.entry_widget.add_client()

    def deact_client(self):
        """Deactivate a client."""
        self.clients_box.entry_widget.deactivate_client()

    def add_project(self):
        """Add a project."""
        self.projects_box.entry_widget.add_project()

    def deact_project(self):
        """Deactivate a project."""
        self.projects_box.entry_widget.deactivate_project()

    def switch_to_inact(self):
        """Switch to help form."""
        self.parentApp.setNextForm('Inactive')
        self.parentApp.switchFormNow()

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
        self.m.addItem(text='Add client', onSelect=self.add_client, shortcut='c')
        self.m.addItem(text='Deactivate client', onSelect=self.deact_client, shortcut='C')
        self.m.addItem(text='Add project', onSelect=self.add_project, shortcut='p')
        self.m.addItem(
            text='Deactivate project', onSelect=self.deact_project, shortcut='P'
        )
        self.m.addItem(text='Show inactive', onSelect=self.switch_to_inact, shortcut='i')
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

        # update projects (contains the method .update_values())
        self.clients_box.entry_widget.refresh_project_list()
