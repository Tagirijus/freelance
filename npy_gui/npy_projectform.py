"""Form for the projects."""

import curses
from general.functions import NewOffer
from general.functions import move_list_entry
import npyscreen


class OfferList(npyscreen.MultiLineAction):
    """List holding offers for the chosen project."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(OfferList, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            curses.KEY_IC: self.add_offer,
            curses.KEY_DC: self.delete_offer,
            'c': self.copy_offer,
            '+': self.move_up,
            '-': self.move_down
        })

        # set up additional multiline options
        self.slow_scroll = True
        self.scroll_exit = True

    def move_up(self, keypress=None):
        """Move selected offer up in the list."""
        lis = self.parent.parentApp.tmpProject.get_offer_list()

        # cancel if list is < 2
        if len(lis) < 2:
            return False

        # move selected item up
        new_index = move_list_entry(
            lis=lis,
            index=self.cursor_line,
            direction=1
        )

        # update view
        self.update_values()
        self.cursor_line = new_index

    def move_down(self, keypress=None):
        """Move selected offer down in the list."""
        lis = self.parent.parentApp.tmpProject.get_offer_list()

        # cancel if list is < 2
        if len(lis) < 2:
            return False

        # move selected item up
        new_index = move_list_entry(
            lis=lis,
            index=self.cursor_line,
            direction=-1
        )

        # update view
        self.update_values()
        self.cursor_line = new_index

    def update_values(self):
        """Update list and refresh."""
        # get values
        self.values = self.parent.parentApp.tmpProject.get_offer_list()
        self.display()

        # clear filter for not showing doubled entries (npyscreen bug?)
        self.clear_filter()

    def display_value(self, vl):
        """Display the offers."""
        title = '[no title!]' if vl.title == '' else vl.title
        return '{}'.format(title)

    def copy_offer(self, keypress=None):
        """Copy the selected offer."""
        # cancel if there is nothign to copy
        if len(self.values) < 1:
            return False

        # get copy of the selected offer object
        new_offer = self.values[self.cursor_line].copy()

        # add the offer to the offer_list
        self.parent.parentApp.tmpProject.append_offer(
            offer=new_offer
        )

        # refresh
        self.update_values()

    def add_offer(self, keypress=None):
        """Add a new offer to the project."""
        # get the selected project
        project = self.parent.parentApp.tmpProject

        # get its client
        client = self.parent.parentApp.L.get_client_by_id(
            client_id=project.client_id
        )

        # prepare tmpOffer
        self.parent.parentApp.tmpOffer_new = True
        self.parent.parentApp.tmpOffer_index = self.cursor_line
        self.parent.parentApp.tmpOffer = NewOffer(
            settings=self.parent.parentApp.S,
            global_list=self.parent.parentApp.L,
            client=client,
            project=project
        )

        # switch to offer form
        title_name = 'Freelance > Project > Offer ({}: {})'.format(
            client.client_id,
            project.title
        )
        self.parent.parentApp.getForm('Offer').name = title_name
        self.parent.parentApp.setNextForm('Offer')
        self.parent.parentApp.switchFormNow()

    def delete_offer(self, keypress=None):
        """Delete the selected offer from the project."""
        # get the selected project
        project = self.parent.parentApp.tmpProject

        offer = project.get_offer_list()[self.cursor_line]

        really = npyscreen.notify_yes_no(
            'Really delete offer "{}" from the project?'.format(offer.title),
            form_color='CRITICAL'
        )

        if really:
            # delete offer
            self.parent.parentApp.tmpProject.pop_offer(self.cursor_line)

            # refresh widget list
            self.update_values()

    def actionHighlighted(self, act_on_this, keypress=None):
        """Do something, because a key was pressed."""
        try:
            # get the selected project
            self.parent.values_to_tmp()
            project = self.parent.parentApp.tmpProject

            # get its client
            client = self.parent.parentApp.L.get_client_by_id(
                client_id=project.client_id
            )

            # get the actual offer into temp offer
            self.parent.parentApp.tmpOffer = act_on_this.copy()
            self.parent.parentApp.tmpOffer_new = False
            self.parent.parentApp.tmpOffer_index = self.cursor_line

            # rename form and switch
            title_name = '{}: {}'.format(client.client_id, act_on_this.title)
            self.parent.parentApp.getForm(
                'Offer'
            ).name = 'Freelance > Project > Offer ({})'.format(title_name)

            # switch to the client form
            self.editing = False
            self.parent.parentApp.setNextForm('Offer')
            self.parent.parentApp.switchFormNow()
        except Exception:
            npyscreen.notify_confirm(
                'Something went wrong, sorry!',
                form_color='WARNING'
            )


class OfferListBox(npyscreen.BoxTitle):
    """Box holding the OffeList."""

    _contained_widget = OfferList


class ProjectForm(npyscreen.FormMultiPageActionWithMenus):
    """Form for editing the project."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(ProjectForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel
        })

    def add_offer(self):
        """Add an offer."""
        self.offers_box.entry_widget.add_offer()

    def copy_offer(self):
        """Copy the selected offer."""
        self.offers_box.entry_widget.copy_offer()

    def del_offer(self):
        """Delete an offer."""
        self.offers_box.entry_widget.delete_offer()

    def save(self):
        """Save the offer / project."""
        allright = self.values_to_tmp(save=True)

        # check if it's allright
        if allright:
            # save the file
            i = self.parentApp.L.get_project_index(
                project=self.parentApp.tmpProject
            )
            self.parentApp.L.save_project_to_file(
                project=self.parentApp.L.project_list[i]
            )
        else:
            npyscreen.notify_confirm(
                'Project ID not possible. Already exists ' +
                'or empty. Choose another one, please!',
                form_color='WARNING'
            )

    def switch_to_help(self):
        """Switch to the help screen."""
        self.values_to_tmp()
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
        self.m.addItem(text='Add offer', onSelect=self.add_offer, shortcut='o')
        self.m.addItem(text='Copy offer', onSelect=self.copy_offer, shortcut='c')
        self.m.addItem(text='Delete offer', onSelect=self.del_offer, shortcut='O')
        self.m.addItem(text='Save', onSelect=self.save, shortcut='s')
        self.m.addItem(text='Help', onSelect=self.switch_to_help, shortcut='h')
        self.m.addItem(text='Exit', onSelect=self.exit, shortcut='e')

        # create the input widgets
        self.title = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Title:',
            begin_entry_at=20
        )
        self.offers_box = self.add_widget_intelligent(
            OfferListBox,
            name='Offers',
            max_height=8
        )
        self.wage = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Wage:',
            begin_entry_at=20
        )
        self.hours_per_day = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Hours / day:',
            begin_entry_at=20
        )
        self.work_days = self.add_widget_intelligent(
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
        self.minimum_days = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Minimum days:',
            begin_entry_at=20
        )
        self.client_id = self.add_widget_intelligent(
            npyscreen.TitleSelectOne,
            name='Client:',
            begin_entry_at=20,
            max_height=4,
            scroll_exit=True,
            value=[0]
        )
        self.client_id_list = []

    def beforeEditing(self):
        """Get values from temp object."""
        self.title.value = self.parentApp.tmpProject.title
        self.offers_box.entry_widget.update_values()
        self.wage.value = str(float(self.parentApp.tmpProject.get_wage()))
        self.hours_per_day.value = str(
            self.parentApp.tmpProject.get_hours_per_day()
        )
        self.work_days.value = self.parentApp.tmpProject.get_work_days()
        self.minimum_days.value = str(self.parentApp.tmpProject.get_minimum_days())

        # handle client id
        self.client_id.values = [
            c.client_id + ': ' + c.fullname() for c in self.parentApp.L.client_list
        ]
        self.client_id_list = [
            c.client_id for c in self.parentApp.L.client_list
        ]
        try:
            self.client_id.value = [self.client_id_list.index(
                self.parentApp.tmpProject_client.client_id
            )]
        except Exception:
            pass

    def values_to_tmp(self, save=False):
        """Store values to temp variable."""
        # get values into tmp object
        old_project = self.parentApp.tmpProject.copy()
        self.parentApp.tmpProject.title = self.title.value
        self.parentApp.tmpProject.set_offer_list(
            self.offers_box.entry_widget.values
        )
        self.parentApp.tmpProject.set_wage(self.wage.value)
        self.parentApp.tmpProject.set_hours_per_day(self.hours_per_day.value)
        self.parentApp.tmpProject.set_work_days(self.work_days.value)
        self.parentApp.tmpProject.set_minimum_days(self.minimum_days.value)
        self.parentApp.tmpProject.client_id = self.client_id_list[
            self.client_id.value[0]
        ]

        # save or not?
        if not save:
            return False

        # it is a new project
        if self.parentApp.tmpProject_new:
            # returns false, if project_id() exists in ..._list (otherwise true)
            worked = self.parentApp.L.add_project(
                project=self.parentApp.tmpProject.copy()
            )

            if worked:
                self.parentApp.tmpProject_new = False

            return worked

        # project gets modified
        else:
            return self.parentApp.L.update_project(
                old_project=old_project,
                new_project=self.parentApp.tmpProject.copy()
            )

    def on_ok(self, keypress=None):
        """Check values and store them."""
        allright = self.values_to_tmp(save=True)

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
                'Project ID not possible. Already exists ' +
                'or empty. Choose another one, please!',
                form_color='WARNING'
            )

    def on_cancel(self, keypress=None):
        """Cancel and switch form."""
        self.parentApp.setNextForm('MAIN')
        self.parentApp.switchFormNow()
