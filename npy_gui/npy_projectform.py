"""Form for the projects."""

import curses
import npyscreen


class OfferList(npyscreen.MultiLineAction):
    """List holding offers for the chosen project."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(OfferList, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            curses.KEY_IC: self.add_offer,
            curses.KEY_DC: self.delete_offer
        })

        # set up additional multiline options
        self.slow_scroll = True
        self.scroll_exit = True

    def add_offer(self):
        """Add a new offer to the project."""
        pass

    def delete_offer(self):
        """Delete the selected offer from the project."""
        pass


class OfferListBox(npyscreen.BoxTitle):
    """Box holding the OffeList."""

    _contained_widget = OfferList


class ProjectForm(npyscreen.ActionFormWithMenus):
    """Form for editing the project."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(ProjectForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel
        })

    def switch_to_help(self):
        """Switch to the help screen."""
        self.parentApp.load_helptext('help_project.txt')
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
        self.hours_per_day = self.add(
            npyscreen.TitleText,
            name='Hours / day:',
            begin_entry_at=20
        )
        self.work_days = self.add(
            npyscreen.TitleMultiSelect,
            name='Work days:',
            begin_entry_at=20,
            max_height=7,
            scroll_exit=True,
            values=[
                'Monday',
                'Tuesday',
                'Wednesday',
                'Thursday',
                'Friday',
                'Saturday',
                'Sunday'
            ]
        )
        self.minimum_days = self.add(
            npyscreen.TitleText,
            name='Minimum days:',
            begin_entry_at=20
        )
        self.client_id = self.add(
            npyscreen.TitleSelectOne,
            name='Client:',
            begin_entry_at=20,
            max_height=4,
            scroll_exit=True,
            value=[0]
        )
        self.offer_list = self.add(
            OfferListBox,
            name='Offers'
        )

    def beforeEditing(self):
        """Get values from temp object."""
        self.title.value = self.parentApp.tmpProject.title
        self.hours_per_day.value = str(self.parentApp.tmpProject.hours_per_day)
        self.work_days.value = self.parentApp.tmpProject.work_days
        self.minimum_days.value = str(self.parentApp.tmpProject.minimum_days)

        # handle client id
        self.client_id.values = [
            c.client_id for c in self.parentApp.L.client_list
        ]
        try:
            self.client_id.value = [self.client_id.values.index(
                self.parentApp.tmpProject_client.client_id
            )]
        except Exception:
            pass

        self.offer_list.values = self.parentApp.tmpProject.offer_list

    def values_to_tmp(self):
        """Store values to temp variable."""
        # get variables in temp
        title = self.title.value

        try:
            hours_per_day = int(self.hours_per_day.value)
        except Exception:
            hours_per_day = self.parentApp.tmpProject.hours_per_day

        work_days = self.work_days.value

        try:
            minimum_days = int(self.minimum_days.value)
        except Exception:
            minimum_days = self.parentApp.tmpProject.minimum_days

        client_id = self.client_id.values[
            self.client_id.value[0]
        ]

        offer_list = self.offer_list.values

        # get values into tmp object
        old_project = self.parentApp.tmpProject.copy()
        self.parentApp.tmpProject.title = title
        self.parentApp.tmpProject.hours_per_day = hours_per_day
        self.parentApp.tmpProject.work_days = work_days
        self.parentApp.tmpProject.minimum_days = minimum_days
        self.parentApp.tmpProject.client_id = client_id
        self.parentApp.tmpProject.offer_list = offer_list

        # it is a new project
        if self.parentApp.tmpProject_new:
            # returns false, if project_id() exists in ..._list (otherwise true)
            return self.parentApp.L.add_project(
                project=self.parentApp.tmpProject.copy()
            )

        # project gets modified
        else:
            return self.parentApp.L.update_project(
                old_project=old_project,
                new_project=self.parentApp.tmpProject.copy()
            )

    def on_ok(self, keypress=None):
        """Check values and store them."""
        allright = self.values_to_tmp()

        # check if it's allright and switch form then
        if allright:
            # save the file
            i = self.parentApp.L.get_project_index(
                project=self.parentApp.tmpProject
            )
            self.parentApp.L.save_project_to_file(
                project=self.parentApp.L.project_list[i]
            )

            # switch back
            self.parentApp.setNextForm('MAIN')
            self.parentApp.switchFormNow()
        else:
            npyscreen.notify_confirm(
                'Project ID not possible. Already exists\n' +
                'or empty. Choose another one, please!',
                form_color='WARNING'
            )

    def on_cancel(self, keypress=None):
        """Cancel and switch form."""
        self.parentApp.setNextForm('MAIN')
        self.parentApp.switchFormNow()
