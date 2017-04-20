"""The main programm is executed here."""

import npyscreen
from datetime import date
# from offer.entries import SimpleEntry


def debug(text):
    """Write stuff into file - temporarily debug function."""
    f = open('TEMP.txt', 'w')
    f.write(str(text))
    f.close()


class OfferApp(npyscreen.NPSAppManaged):
    """Main app for the programm."""

    def onStart(self):
        """Start the app."""
        # init variables
        self.Text = 'Init'
        self.Datum = date.today()

        # register forms
        self.addForm('MAIN', MainForm, name='Peng!')
        self.addForm('Show', ShowForm, name='Results')
        self.addForm('Test', TestForm, name='Testing ...')


class TestForm(npyscreen.Form):
    """This form is test."""

    def create(self):
        """Create shit."""
        # create the controls
        self.t = self.add(npyscreen.TitleText, name='TestForm')

    def beforeEditing(self):
        """Init variables.Fixed"""
        if hasattr(self, 'parentApp'):
            self.t.value = self.parentApp.Text

    def afterEditing(self):
        """Switch back."""
        # give back the actual value for the controls
        self.parentApp.Text = self.t.value

        # switch back to other form
        self.parentApp.switchForm('Show')


class MainForm(npyscreen.Form):
    """This form class defines the display that will be presented to the user."""

    def create(self):
        """Create the form."""
        # create controls
        self.d = self.add(npyscreen.TitleDateCombo, name = "Date:", dateFmt='%Y-%m-%d')

    def beforeEditing(self):
        """Init variables."""
        # get values for the controls form OfferApp
        if hasattr(self, 'parentApp'):
            self.d.value = self.parentApp.Datum

    def afterEditing(self):
        """Switch back."""
        # give back the actual value for the controls
        self.parentApp.Datum = self.d.value

        # switch back to other form
        self.parentApp.switchForm('Test')


class ShowForm(npyscreen.Form):
    """The result screen."""

    def create(self):
        """Create the form."""
        # create controls
        self.show_pager = self.add(npyscreen.Pager, name='Text:')

    def beforeEditing(self):
        """Init variables."""
        # get values for the controls form OfferApp
        if hasattr(self, 'parentApp'):
            show_pager_content = (
                self.parentApp.Text,
                self.parentApp.Datum.strftime('%Y-%m uuund %d')
            )
            self.show_pager.values = show_pager_content

    def afterEditing(self):
        """Switch back."""
        # switch back to other form
        self.parentApp.switchForm('MAIN')
