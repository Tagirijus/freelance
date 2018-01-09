"""Form for deactivated clients and projects."""

import curses
import npyscreen


class ClientList(npyscreen.MultiLineAction):
    """List of the clients."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(ClientList, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            curses.KEY_DC: self.delete_client,
            curses.KEY_RIGHT: self.h_exit_right  # switch to project list
        })

        # set up additional multiline options
        self.slow_scroll = True

    def update_values(self):
        """Update the values."""
        self.values = sorted(
            self.parent.iL.client_list,
            key=lambda x: x.client_id
        )
        self.display()

    def display_value(self, vl):
        """Display values."""
        return '{}: {}'.format(vl.client_id, vl.fullname())

    def delete_client(self, keypress):
        """Ask to deactivate the client and do it if yes."""
        really = npyscreen.notify_yes_no(
            'This will DELETE the client file! Sure?',
            form_color='CRITICAL'
        )

        # yepp, delete it
        if really:
            worked = self.parent.iL.remove_client(
                client=self.values[self.cursor_line],
                settings=self.parent.parentApp.S,
            )

            # something went wrong
            if not worked:
                npyscreen.notify_confirm(
                    'Client not properly deleted, woops!',
                    form_color='WARNING'
                )

            # ouhkaaaay
            else:
                self.update_values()

    def actionHighlighted(self, act_on_this, keypress):
        """Add the selected client to the active clients list."""
        # get the actual client into temp client
        tmp_client = act_on_this.copy()

        # ask, if the user is sure
        really = npyscreen.notify_yes_no(
            'Really add ' + tmp_client.client_id + ': ' + tmp_client.fullname() +
            ' to the active clients?'
        )

        # yes, add it
        if really:
            add_worked = self.parent.parentApp.L.activate_client(
                client=tmp_client,
                settings=self.parent.parentApp.S,
                inactive_list=self.parent.iL
            )

            # it did not work!
            if not add_worked:
                npyscreen.notify_confirm(
                    'Something went wrong. Maybe client already exists?',
                    form_color='WARNING'
                )
                return False
            else:
                # it did work, update values
                self.update_values()
                return True
        else:
            return False


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
            curses.KEY_DC: self.delete_project,
            curses.KEY_LEFT: self.h_exit_left  # switch to client list
        })

        # set up additional multiline options
        self.slow_scroll = True

    def update_values(self):
        """Update the values."""
        self.values = sorted(
            self.parent.iL.project_list,
            key=lambda x: x.project_id()
        )
        self.display()

    def display_value(self, vl):
        """Display values."""
        return '{}: {}'.format(vl.client_id, vl.title)

    def delete_project(self, keypress):
        """Ask to deactivate the client and do it if yes."""
        really = npyscreen.notify_yes_no(
            'This will DELETE the project file! Sure?',
            form_color='CRITICAL'
        )

        # yepp, delete it
        if really:
            worked = self.parent.iL.remove_project(
                project=self.values[self.cursor_line],
                settings=self.parent.parentApp.S,
            )

            # something went wrong
            if not worked:
                npyscreen.notify_confirm(
                    'Project not properly deleted, woops!',
                    form_color='WARNING'
                )

            # ouhkaaaay
            else:
                self.update_values()

    def actionHighlighted(self, act_on_this, keypress):
        """Add the selected project to the active projects list."""
        # get the actual project into temp project
        tmp_project = act_on_this.copy()

        # ask, if the user is sure
        really = npyscreen.notify_yes_no(
            'Really add ' + tmp_project.client_id + ': ' + tmp_project.title +
            'to the active projects?'
        )

        # yes, add it
        if really:
            add_worked = self.parent.parentApp.L.activate_project(
                project=tmp_project,
                settings=self.parent.parentApp.S,
                inactive_list=self.parent.iL
            )

            # it did not work!
            if not add_worked:
                npyscreen.notify_confirm(
                    'Something went wrong. Maybe project already exists? ' +
                    'Or its client is inactive?',
                    form_color='WARNING'
                )
                return False
            else:
                # it did work, update values
                self.update_values()
                return True
        else:
            return False


class ProjectListBox(npyscreen.BoxTitle):
    """Box holding the ProjectList."""

    _contained_widget = ProjectList


class InactiveForm(npyscreen.ActionFormWithMenus):
    """Inactive form."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(InactiveForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel
        })

    def switch_to_help(self):
        """Switch to help form."""
        self.parentApp.load_helptext('help_inactive.txt')
        self.parentApp.setNextForm('Help')
        self.parentApp.switchFormNow()

    def exit(self):
        """Exit the programm."""
        self.parentApp.setNextForm(None)
        self.parentApp.switchFormNow()

    def create(self):
        """Initialize the form with its widgets."""
        # create the menu
        self.m = self.new_menu(name='Menu')
        self.m.addItem(text='Help', onSelect=self.switch_to_help, shortcut='h')
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
        # get the inactive list from inactive folders
        self.parentApp.L.update_inactive_list(settings=self.parentApp.S)
        self.iL = self.parentApp.L.get_inactive_list(settings=self.parentApp.S)

        # save old selection
        cursor_save_c = self.clients_box.entry_widget.cursor_line
        cursor_save_p = self.projects_box.entry_widget.cursor_line

        # update clients
        self.clients_box.entry_widget.update_values()

        # clear filter to not show doubled entries ... npyscreen bug?
        self.clients_box.entry_widget.clear_filter()

        # get old selection back
        self.clients_box.entry_widget.cursor_line = cursor_save_c

        # --- now the same for the projects ---

        # update projects
        self.projects_box.entry_widget.update_values()

        # clear filter to not show doubled entries ... npyscreen bug?
        self.projects_box.entry_widget.clear_filter()

        # get old selection back
        self.projects_box.entry_widget.cursor_line = cursor_save_p

    def on_ok(self, keypress=None):
        """Do the same as in on_cancel."""
        self.on_cancel()

    def on_cancel(self, keypress=None):
        """Go back without changing a thing."""
        # exit form
        self.editing = False
        # swtich back
        self.parentApp.setNextForm('MAIN')
        self.parentApp.switchFormNow()
