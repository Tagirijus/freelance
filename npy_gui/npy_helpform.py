"""Help form."""

import npyscreen


class HelpForm(npyscreen.Form):
    """The help form."""

    def create(self):
        """Create the form."""
        # create a textfield which will hold the text
        self.helpfield = self.add(npyscreen.Pager)
        self.helpfield.autowrap = True

    def beforeEditing(self):
        """Fill the helptext."""
        # load the helptext from the main app
        self.helpfield.values = self.parentApp.H.split('\n')

    def afterEditing(self):
        """Return to main page."""
        self.parentApp.switchFormPrevious()
