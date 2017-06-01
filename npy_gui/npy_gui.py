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
from npy_gui.npy_defaultsform import DefaultsOfferForm
from npy_gui.npy_defaultsform import DefaultsInvoiceForm
from npy_gui.npy_defaultsform import DefaultsClientProjectForm
from npy_gui.npy_defaultsform import DefaultsEntryForm
from npy_gui.npy_entryform import BaseEntryForm
from npy_gui.npy_entryform import MultiplyEntryForm
from npy_gui.npy_entryform import ConnectEntryForm
from npy_gui.npy_exportform import ExportForm
from npy_gui.npy_helpform import HelpForm
from npy_gui.npy_inactiveform import InactiveForm
from npy_gui.npy_mainform import MainForm
from npy_gui.npy_offerform import EntryChooseForm
from npy_gui.npy_offerform import OfferForm
from npy_gui.npy_invoiceform import InvoiceForm
from npy_gui.npy_presetform import PresetForm
from npy_gui.npy_projectform import ProjectForm
from npy_gui.npy_settingsform import SettingsForm
from npy_gui.npy_unpaidinvoiceform import UnpaidInvoiceForm
from npy_gui.npy_allinvoicesform import AllInvoicesForm
from offer.entries import BaseEntry
from offer.offerinvoice import Offer
from offer.offerinvoice import Invoice
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
        self.P_what = 'offer'
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
        self.tmpOffer_index = -1
        self.tmpInvoice = Invoice()
        self.tmpInvoice_new = True
        self.tmpInvoice_index = -1
        self.tmpEntry = BaseEntry()
        self.tmpEntry_new = True
        self.tmpEntry_index = -1
        self.tmpEntry_change_type = False
        self.tmpEntry_offer_invoice = 'offer'

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
            'Defaults_offer',
            DefaultsOfferForm,
            name='Freelance > Settings > Defaults > Offer'
        )
        self.addForm(
            'Defaults_invoice',
            DefaultsInvoiceForm,
            name='Freelance > Settings > Defaults > Invoice'
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
            name='Freelance > Client',
            color='NO_EDIT'
        )
        self.addForm(
            'Project',
            ProjectForm,
            name='Freelance > Project',
            color='NO_EDIT'
        )
        self.addForm(
            'Inactive',
            InactiveForm,
            name='Freelance > Inactive clients and projects',
            color='WARNING'
        )
        self.addForm(
            'Offer',
            OfferForm,
            name='Freelance > Project > Offer',
            color='NO_EDIT'
        )
        self.addForm(
            'Invoice',
            InvoiceForm,
            name='Freelance > Project > Invoice',
            color='NO_EDIT'
        )
        self.addForm(
            'UnpaidInvoice',
            UnpaidInvoiceForm,
            name='Freelance > Unpaid invoices',
            color='DANGER'
        )
        self.addForm(
            'AllInvoices',
            AllInvoicesForm,
            name='Freelance > All invoices',
            color='WARNING'
        )
        self.addForm(
            'EntryChoose',
            EntryChooseForm,
            name='Freelance > Project > Offer > Entry'
        )
        self.addForm(
            'BaseEntry',
            BaseEntryForm,
            name='Freelance > Project > Offer > Base entry',
            color='NO_EDIT'
        )
        self.addForm(
            'MultiplyEntry',
            MultiplyEntryForm,
            name='Freelance > Project > Offer > Multiply entry',
            color='NO_EDIT'
        )
        self.addForm(
            'ConnectEntry',
            ConnectEntryForm,
            name='Freelance > Project > Offer > Connect entry',
            color='NO_EDIT'
        )
        self.addForm(
            'Presets',
            PresetForm,
            name='Choose a preset',
            color='WARNING'
        )
        self.addForm(
            'Export',
            ExportForm,
            name='Choose a template'
        )
