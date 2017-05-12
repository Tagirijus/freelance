"""Form for preset choosing."""

import curses
from general.functions import PresetOffer
from general.functions import PresetBaseEntry
from general.functions import PresetMultiplyEntry
from general.functions import PresetConnectEntry
import npyscreen
from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry
from offer.offerinvoice import Offer


class PresetList(npyscreen.MultiLineAction):
    """The list holding the choosable presets."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(PresetList, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            curses.KEY_DC: self.delete,
            'r': self.rename
        })

        # set up additional multiline options
        self.slow_scroll = True

    def actionHighlighted(self, act_on_this, keypress=None):
        """Do something, because a key was pressed."""
        # cancel if there are no values
        if len(self.values) < 1:
            return False

        entry = act_on_this

        # it's an Offer
        if type(entry) is Offer:
            self.parent.parentApp.tmpOffer = PresetOffer(
                offer_preset=entry,
                settings=self.parent.parentApp.S,
                global_list=self.parent.parentApp.L,
                client=self.parent.parentApp.tmpClient,
                project=self.parent.parentApp.tmpProject
            ).copy(keep_date=False)
            self.parent.parentApp.setNextForm('Offer')
            self.parent.parentApp.switchFormNow()

        # it's a BaseEntry
        elif type(entry) is BaseEntry:
            self.parent.parentApp.tmpEntry = PresetBaseEntry(
                entry_preset=entry,
                settings=self.parent.parentApp.S,
                global_list=self.parent.parentApp.L,
                client=self.parent.parentApp.tmpClient,
                project=self.parent.parentApp.tmpProject
            ).copy(keep_id=False)
            self.parent.parentApp.setNextForm('BaseEntry')
            self.parent.parentApp.switchFormNow()

        # it's a MultiplyEntry
        elif type(entry) is MultiplyEntry:
            self.parent.parentApp.tmpEntry = PresetMultiplyEntry(
                entry_preset=entry,
                settings=self.parent.parentApp.S,
                global_list=self.parent.parentApp.L,
                client=self.parent.parentApp.tmpClient,
                project=self.parent.parentApp.tmpProject
            ).copy(keep_id=False)
            self.parent.parentApp.setNextForm('MultiplyEntry')
            self.parent.parentApp.switchFormNow()

        # it's a ConnectEntry
        elif type(entry) is ConnectEntry:
            self.parent.parentApp.tmpEntry = PresetConnectEntry(
                entry_preset=entry,
                settings=self.parent.parentApp.S,
                global_list=self.parent.parentApp.L,
                client=self.parent.parentApp.tmpClient,
                project=self.parent.parentApp.tmpProject
            ).copy(keep_id=False)
            self.parent.parentApp.setNextForm('ConnectEntry')
            self.parent.parentApp.switchFormNow()

    def rename(self, keypress=None):
        """Try to rename the selected preset."""
        # cancel if there are no values
        if len(self.values) < 1:
            return False

        entry = self.values[self.cursor_line]

        new_name = npyscreen.notify_input(
            'Enter name for preset:',
            pre_text=entry.title
        )

        if new_name:
            if self.is_offer(entry):
                renamed = self.parent.parentApp.P.rename_offer(
                    old_offer_title=entry.title,
                    new_offer_title=new_name
                )
            elif self.is_entry(entry):
                renamed = self.parent.parentApp.P.rename_entry(
                    old_entry_title=entry.title,
                    new_entry_title=new_name
                )
            else:
                renamed = False

            if not renamed:
                npyscreen.notify_confirm(
                    'Rename did not work ...',
                    form_color='DANGER'
                )
            else:
                self.parent.beforeEditing()

    def delete(self, keypress=None):
        """Ask and delete entry."""
        # cancel if there are no values
        if len(self.values) < 1:
            return False

        entry = self.values[self.cursor_line]

        really = npyscreen.notify_yes_no(
            'Really delete the entry "{}"?'.format(entry.title),
            form_color='CRITICAL'
        )

        if really:
            if self.is_offer(entry):
                deleted = self.parent.parentApp.P.remove_offer(offer=entry)
            elif self.is_entry(entry):
                deleted = self.parent.parentApp.P.remove_entry(entry=entry)
            else:
                deleted = False

            if not deleted:
                npyscreen.notify_confirm(
                    'Could not delete the entry!',
                    form_color='WARNING'
                )
            else:
                self.parent.parentApp.P.save_all()
                self.update_values()

    def update_values(self):
        """Update the values."""
        if self.parent.parentApp.P_what == 'offer':
            self.values = sorted(
                self.parent.parentApp.P.offer_list,
                key=lambda x: x.title
            )
        else:
            self.values = sorted(
                self.parent.parentApp.P.entry_list,
                key=lambda x: x.title
            )

        self.display()

        # clear filter for not showing doubled entries (npyscreen bug?)
        self.clear_filter()

    def display_value(self, vl):
        """Display values."""
        return '{}: {}'.format(vl.__class__.__name__, vl.title)

    def is_offer(self, entry=None):
        """Check if entry is Offer."""
        return type(entry) is Offer

    def is_entry(self, entry=None):
        """Check if entry is Entry."""
        return (type(entry) is BaseEntry or type(entry) is MultiplyEntry or
                type(entry) is ConnectEntry)


class PresetForm(npyscreen.ActionFormWithMenus):
    """Form for choosing a preset."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(PresetForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel
        })

    def rename(self):
        """Rename selected preset."""
        self.preset_list.rename()

    def switch_to_help(self):
        """Switch to the help form."""
        self.parentApp.load_helptext('help_presets.txt')
        self.parentApp.setNextForm('Help')
        self.parentApp.switchFormNow()

    def exit(self):
        """Exit the programm."""
        self.parentApp.setNextForm(None)
        self.parentApp.switchFormNow()

    def create(self):
        """Create the widgets."""
        # the menu
        self.m = self.new_menu(name='Menu')
        self.m.addItem(text='Rename', onSelect=self.rename, shortcut='r')
        self.m.addItem(text='Help', onSelect=self.switch_to_help, shortcut='h')
        self.m.addItem(text='Exit', onSelect=self.exit, shortcut='e')

        # the list
        self.preset_list = self.add(
            PresetList,
            name='Presets'
        )

    def beforeEditing(self):
        """Load stuff into the list."""
        self.preset_list.update_values()

    def on_ok(self, keypress=None):
        """Do on ok.."""
        self.parentApp.switchFormPrevious()

    def on_cancel(self, keypress=None):
        """Do the same as on ok.."""
        self.on_ok()
