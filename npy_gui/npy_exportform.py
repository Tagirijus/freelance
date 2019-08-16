"""Form for choosing the export template."""

import npyscreen


class TemplateChooseList(npyscreen.MultiLineAction):
    """The list holding the choosable templates."""

    def update_values(self):
        """Update values and refresh view."""
        if self.parent.parentApp.tmpEntry_offer_invoice == 'offer':
            self.values = sorted(
                self.parent.parentApp.S.defaults[
                    self.parent.parentApp.tmpClient.language
                ].get_offer_templates_as_list(),
                key=lambda x: x[0].lower()
            )
        else:
            self.values = sorted(
                self.parent.parentApp.S.defaults[
                    self.parent.parentApp.tmpClient.language
                ].get_invoice_templates_as_list(),
                key=lambda x: x[0].lower()
            )

        self.display()
        self.clear_filter()

    def display_value(self, vl):
        """Display the list values."""
        return vl[0]

    def actionHighlighted(self, act_on_this, keypress):
        """Do something, because a key was pressed."""
        # export offer with selected template
        if self.parent.parentApp.tmpEntry_offer_invoice == 'offer':
            exported = self.parent.parentApp.tmpOffer.export_to_openoffice(
                client=self.parent.parentApp.tmpClient,
                project=self.parent.parentApp.tmpProject,
                global_list=self.parent.parentApp.L,
                settings=self.parent.parentApp.S,
                template=act_on_this[1],
                file=self.parent.parentApp.S.defaults[
                    self.parent.parentApp.tmpClient.language
                ].offer_filename
            )

        # export invoice with selected template
        else:
            exported = self.parent.parentApp.tmpInvoice.export_to_openoffice(
                client=self.parent.parentApp.tmpClient,
                project=self.parent.parentApp.tmpProject,
                global_list=self.parent.parentApp.L,
                settings=self.parent.parentApp.S,
                template=act_on_this[1],
                file=self.parent.parentApp.S.defaults[
                    self.parent.parentApp.tmpClient.language
                ].invoice_filename
            )

        if not exported:
            npyscreen.notify_confirm(
                'Something went wrong exporting the offer, sorry!',
                form_color='DANGER'
            )
        else:
            self.parent.parentApp.switchFormPrevious()


class ExportForm(npyscreen.ActionPopup):
    """Form for choosing the template."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(ExportForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel
        })

        self.color = 'STANDOUT'

    def create(self):
        """Create the form."""
        # create the input widgets
        self.choose_list = self.add(
            TemplateChooseList,
            scroll_exit=True
        )

    def beforeEditing(self):
        """Load template list."""
        self.choose_list.update_values()

    def on_ok(self, keypress=None):
        """Save and go back."""
        # export template

        # and switch back to previous form
        self.parentApp.switchFormPrevious()

    def on_cancel(self, keypress=None):
        """Do the same as in on_ok."""
        # do not export, cancel instead
        self.parentApp.switchFormPrevious()
