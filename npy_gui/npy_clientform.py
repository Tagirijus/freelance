"""Form for the clients."""

import npyscreen


class ClientForm(npyscreen.ActionFormWithMenus):
    """Form for editing the client."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(ClientForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel
        })

    def switch_to_help(self):
        """Switch to the help screen."""
        self.values_to_tmp()
        self.parentApp.load_helptext('help_client.txt')
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
        self.client_id = self.add(
            npyscreen.TitleText,
            name='Client ID:',
            begin_entry_at=20
        )
        self.client_company = self.add(
            npyscreen.TitleText,
            name='Company:',
            begin_entry_at=20
        )
        self.client_attention = self.add(
            npyscreen.TitleText,
            name='Attention:',
            begin_entry_at=20
        )
        self.client_salutation = self.add(
            npyscreen.TitleText,
            name='Salutation:',
            begin_entry_at=20
        )
        self.client_name = self.add(
            npyscreen.TitleText,
            name='Name:',
            begin_entry_at=20
        )
        self.client_family_name = self.add(
            npyscreen.TitleText,
            name='Family name:',
            begin_entry_at=20
        )
        self.client_street = self.add(
            npyscreen.TitleText,
            name='Street:',
            begin_entry_at=20
        )
        self.client_post_code = self.add(
            npyscreen.TitleText,
            name='Post_code:',
            begin_entry_at=20
        )
        self.client_city = self.add(
            npyscreen.TitleText,
            name='City:',
            begin_entry_at=20
        )
        self.client_tax_id = self.add(
            npyscreen.TitleText,
            name='Tax ID:',
            begin_entry_at=20
        )
        self.client_language = self.add(
            npyscreen.TitleSelectOne,
            name='Language:',
            begin_entry_at=20,
            max_height=4,
            scroll_exit=True,
            value=[0]
        )

    def beforeEditing(self):
        """Get values."""
        self.client_id.value = self.parentApp.tmpClient.client_id
        self.client_company.value = self.parentApp.tmpClient.company
        self.client_attention.value = self.parentApp.tmpClient.attention
        self.client_salutation.value = self.parentApp.tmpClient.salutation
        self.client_name.value = self.parentApp.tmpClient.name
        self.client_family_name.value = self.parentApp.tmpClient.family_name
        self.client_street.value = self.parentApp.tmpClient.street
        self.client_post_code.value = self.parentApp.tmpClient.post_code
        self.client_city.value = self.parentApp.tmpClient.city
        self.client_tax_id.value = self.parentApp.tmpClient.tax_id

        # handle languages
        self.client_language.values = self.parentApp.S.get_languages()

        c_lang = self.parentApp.tmpClient.language
        if c_lang in self.client_language.values:
            self.client_language.value[0] = self.client_language.values.index(
                c_lang
            )
        else:
            self.client_language.value[0] = 0

        # get actual caption for form
        if self.parentApp.tmpClient_new:
            self.name = 'Freelance > Client (NEW)'
        else:
            title_name = '{}, {}'.format(
                self.parentApp.tmpClient.client_id,
                self.parentApp.tmpClient.fullname()
            )
            self.name = 'Freelance > Client ({})'.format(title_name)

    def values_to_tmp(self, save=False):
        """Store values to temp variable."""
        # get values into tmp object
        old_client = self.parentApp.tmpClient.copy()
        self.parentApp.tmpClient.client_id = self.client_id.value
        self.parentApp.tmpClient.company = self.client_company.value
        self.parentApp.tmpClient.attention = self.client_attention.value
        self.parentApp.tmpClient.salutation = self.client_salutation.value
        self.parentApp.tmpClient.name = self.client_name.value
        self.parentApp.tmpClient.family_name = self.client_family_name.value
        self.parentApp.tmpClient.street = self.client_street.value
        self.parentApp.tmpClient.post_code = self.client_post_code.value
        self.parentApp.tmpClient.city = self.client_city.value
        self.parentApp.tmpClient.tax_id = self.client_tax_id.value
        self.parentApp.tmpClient.language = self.client_language.values[
            self.client_language.value[0]
        ]

        # save or not?
        if not save:
            return False

        # it is a new client
        if self.parentApp.tmpClient_new:
            # returns false, if client_id exists in client_list (otherwise true)
            worked = self.parentApp.L.add_client(
                client=self.parentApp.tmpClient.copy()
            )

            if worked:
                self.parentApp.tmpClient_new = False

            return worked

        # client gets modified
        else:
            return self.parentApp.L.update_client(
                old_client=old_client,
                new_client=self.parentApp.tmpClient.copy()
            )

    def on_ok(self, keypress=None):
        """Check values and save them."""
        allright = self.values_to_tmp(save=True)

        # check if it's allright and switch form then
        if allright:
            # save the file
            i = self.parentApp.L.get_client_index(
                client=self.parentApp.tmpClient
            )
            self.parentApp.L.save_client_to_file(
                client=self.parentApp.L.client_list[i]
            )

            # switch back
            self.parentApp.setNextForm('MAIN')
            self.parentApp.switchFormNow()
        else:
            npyscreen.notify_confirm(
                'Client ID not possible. Already exists ' +
                'or empty. Choose another one, please!',
                form_color='WARNING'
            )

    def on_cancel(self, keypress=None):
        """Go back without changing a thing."""
        # switch back
        self.parentApp.setNextForm('MAIN')
        self.parentApp.switchFormNow()
