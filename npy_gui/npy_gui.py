"""The GUI for the Freelance programm - written with npyscreen."""

from clients.client import Client
from clients.project import Project
from clients.list import List
from general.default import Default
from general.preset import Preset
from general.settings import Settings
import npyscreen
from npy_gui.npy_clientform import ClientForm
from npy_gui.npy_defaultsform import DefaultsForm
from npy_gui.npy_defaultsform import DefaultsGeneralForm
from npy_gui.npy_defaultsform import DefaultsClientProjectForm
from npy_gui.npy_defaultsform import DefaultsEntryForm
from npy_gui.npy_helpform import HelpForm
from npy_gui.npy_mainform import MainForm
from npy_gui.npy_settingsform import SettingsForm
from offer.offer import Offer
import os


class FreelanceApplication(npyscreen.NPSAppManaged):
    """The main application object."""

    def load_helptext(self, helpfile=None):
        """Try to load the helptext into self.H."""
        helpfile = self.S.BASE_PATH + '/npy_gui/' + str(helpfile)

        # try to load the file
        if os.path.isfile(helpfile):
            f = open(helpfile, 'r')
            self.H = f.read()
            f.close()
        # choose fallback text instead
        else:
            self.H = 'Helpfile not found ... sorry! Time to learn by doing!'

    def onStart(self):
        """Create all the forms and variables, which are needed."""
        # get global variables for the app
        self.S = Settings()
        self.L = List(data_path=self.S.data_path)
        self.P = Preset(data_path=self.S.data_path)
        self.H = 'Fallback helptext is: learn by doing! (;'

        # set global temp variables
        self.tmpDefault = Default()
        self.tmpDefault_new = True
        self.tmpClient = Client()
        self.tmpClient_new = True
        self.tmpProject = Project()
        self.tmpProject_new = True
        self.tmpOffer = Offer()
        self.tmpOffer_new = True

        # create the forms
        self.addForm(
            'MAIN',
            MainForm,
            name='Freelance'
        )
        self.addForm(
            'Help',
            HelpForm,
            name='Freelance - Help'
        )
        self.addForm(
            'Settings',
            SettingsForm,
            name='Freelance > Settings'
        )
        self.addForm(
            'Defaults',
            DefaultsForm,
            name='Freelance > Settings > Defaults'
        )
        self.addForm(
            'Defaults_general',
            DefaultsGeneralForm,
            name='Freelance > Settings > Defaults > General'
        )
        self.addForm(
            'Defaults_clientproject',
            DefaultsClientProjectForm,
            name='Freelance > Settings > Defaults > Client / Project'
        )
        self.addForm(
            'Defaults_entry',
            DefaultsEntryForm,
            name='Freelance > Settings > Defaults > Entry'
        )
        self.addForm(
            'Client',
            ClientForm,
            name='Freelance > Client'
        )
