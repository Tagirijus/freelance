"""Form for the defaults."""

import npyscreen


class DefaultChooseList(npyscreen.MultiLineAction):
    """The list holding the choosable default entries."""

    def actionHighlighted(self, act_on_this, keypress):
        """Do something, because a key was pressed."""
        # general was chosen
        if act_on_this == 'General defaults':
            # generate name for form
            tit = 'Freelance > Settings > Defaults ({}) > General'
            self.parent.parentApp.getForm('Defaults_general').name = tit.format(
                self.parent.parentApp.tmpDefault.language
            )

            # go to the Defaults_general form
            self.parent.parentApp.setNextForm('Defaults_general')
            self.parent.parentApp.switchFormNow()

        # client and project was chosen
        elif act_on_this == 'Client and project defaults':
            # generate name for form
            tit = 'Freelance > Settings > Defaults ({}) > Client / Project'
            self.parent.parentApp.getForm('Defaults_clientproject').name = tit.format(
                self.parent.parentApp.tmpDefault.language
            )

            # go to the Defaults_clientproject form
            self.parent.parentApp.setNextForm('Defaults_clientproject')
            self.parent.parentApp.switchFormNow()

        # entry was chosen
        elif act_on_this == 'Entry defaults':
            # generate name for form
            tit = 'Freelance > Settings > Defaults ({}) > Entry'
            self.parent.parentApp.getForm('Defaults_entry').name = tit.format(
                self.parent.parentApp.tmpDefault.language
            )

            # go to the Defaults_clientproject form
            self.parent.parentApp.setNextForm('Defaults_entry')
            self.parent.parentApp.switchFormNow()


class DefaultsForm(npyscreen.ActionPopup):
    """Form for editing the defaults."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(DefaultsForm, self).__init__(*args, **kwargs)

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
            DefaultChooseList,
            values=[
                'General defaults',
                'Client and project defaults',
                'Entry defaults'
            ]
        )

    def on_ok(self, keypress=None):
        """Save and go back."""
        self.parentApp.S.save_settings_to_file()
        self.parentApp.setNextForm('Settings')
        self.parentApp.switchFormNow()

    def on_cancel(self, keypress=None):
        """Do the same as in on_ok."""
        self.on_ok(keypress)


class DefaultsGeneralForm(npyscreen.FormMultiPageActionWithMenus):
    """Form for editing the general defaults."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(DefaultsGeneralForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel
        })

    def switch_to_help(self):
        """Switch to the help screen."""
        self.values_to_tmp()
        self.parentApp.load_helptext('help_defaults_general.txt')
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
        self.language = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Language:',
            begin_entry_at=20
        )
        self.seperation = self.add_widget_intelligent(
            npyscreen.FixedText,
            editable=False
        )
        self.offer_title = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Offer title:',
            begin_entry_at=20
        )
        self.offer_template = self.add_widget_intelligent(
            npyscreen.TitleFilenameCombo,
            name='Offer template:',
            begin_entry_at=20,
            must_exist=True
        )
        self.offer_filename = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Offer filename:',
            begin_entry_at=20
        )
        self.offer_round_price = self.add_widget_intelligent(
            npyscreen.TitleMultiSelect,
            name='Off. round price:',
            begin_entry_at=20,
            max_height=2,
            scroll_exit=True,
            values=['enabled']
        )
        self.date_fmt = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Date format:',
            begin_entry_at=20
        )
        self.project_wage = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Wage:',
            begin_entry_at=20
        )
        self.commodity = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Commodity:',
            begin_entry_at=20
        )

    def beforeEditing(self):
        """Get the values from the active tmpDefault variable."""
        self.language.value = self.parentApp.tmpDefault.language
        self.offer_title.value = self.parentApp.tmpDefault.offer_title
        self.offer_template.value = self.parentApp.tmpDefault.offer_template
        self.offer_filename.value = self.parentApp.tmpDefault.offer_filename
        self.offer_round_price.value = (
            [0] if self.parentApp.tmpDefault.get_offer_round_price() else []
        )
        self.date_fmt.value = self.parentApp.tmpDefault.date_fmt
        self.project_wage.value = str(float(self.parentApp.tmpDefault.get_project_wage()))
        self.commodity.value = self.parentApp.tmpDefault.commodity

    def values_to_tmp(self, save=False):
        """Store values to temp object."""
        # get values in temp variables
        lang_old = self.parentApp.tmpDefault.language

        # prevent user from changing 'en' to another name
        old_is_en = lang_old == 'en'
        language = 'en' if old_is_en else self.language.value

        # check if user really tried to change en and send message
        lang_en_tried_to_change = old_is_en and self.language.value != 'en'
        if lang_en_tried_to_change:
            npyscreen.notify_confirm(
                'Changed language name back to "en". ' +
                'Please do not change it!',
                form_color='WARNING'
            )

        # get stuff into tmpDefault
        self.parentApp.tmpDefault.language = language
        self.parentApp.tmpDefault.offer_title = self.offer_title.value
        self.parentApp.tmpDefault.offer_template = self.offer_template.value
        self.parentApp.tmpDefault.offer_filename = self.offer_filename.value
        if self.offer_round_price.value == [0]:
            self.parentApp.tmpDefault.set_offer_round_price(True)
        else:
            self.parentApp.tmpDefault.set_offer_round_price(False)
        self.parentApp.tmpDefault.date_fmt = self.date_fmt.value
        self.parentApp.tmpDefault.set_project_wage(self.project_wage.value)
        self.parentApp.tmpDefault.commodity = self.commodity.value

        # check things
        lang_exists = language in self.parentApp.S.defaults.keys()
        lang_equal_old = language == lang_old

        # create cases
        case_create_new = self.parentApp.tmpDefault_new and not lang_exists
        case_modify_actual = not self.parentApp.tmpDefault_new and lang_equal_old
        case_rename_actual = not self.parentApp.tmpDefault_new and not lang_equal_old

        # save or not?
        if not save:
            return False

        # check case
        if case_create_new:
            # try to create a new one
            new_created = self.parentApp.S.new_default(language)
            if new_created:
                self.parentApp.S.defaults[language] = self.parentApp.tmpDefault.copy()
                return True
            else:
                # did not work, go on editing
                return False

        elif case_modify_actual:
            # simply modify the selected one - no name change
            self.parentApp.S.defaults[language] = self.parentApp.tmpDefault.copy()
            return True

        elif case_rename_actual and not lang_exists:
            # rename the selected one
            renamed = self.parentApp.S.rename_default(
                old_lang=lang_old,
                new_lang=language,
                client_list=self.parentApp.L.client_list
            )

            if renamed:
                # worked, finish
                return True
            else:
                # did not work, go on editing
                return False
        else:
            # fallback: no case applies (should not happen)
            return False

    def on_ok(self, keypress=None):
        """Check values and set them."""
        allright = self.values_to_tmp(save=True)

        # everything allright? then switch form!
        if allright:
            # get object and save files
            lang = self.parentApp.tmpDefault.language
            self.parentApp.S.defaults[lang] = self.parentApp.tmpDefault
            self.parentApp.S.save_settings_to_file()
            self.parentApp.L.save_client_list_to_file()

            # switch back
            self.parentApp.setNextForm('Defaults')
            self.parentApp.switchFormNow()
        else:
            npyscreen.notify_confirm(
                'Language name not possible. It already exists, ' +
                'is empty or something else. Choose another one!',
                form_color='WARNING'
            )

    def on_cancel(self, keypress=None):
        """Go back without changing a thing."""
        # switch back
        self.parentApp.setNextForm('Defaults')
        self.parentApp.switchFormNow()


class DefaultsClientProjectForm(npyscreen.FormMultiPageActionWithMenus):
    """Form for editing the client and project defaults."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(DefaultsClientProjectForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel
        })

    def switch_to_help(self):
        """Switch to the help screen."""
        self.values_to_tmp()
        self.parentApp.load_helptext('help_defaults_clientproject.txt')
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
        self.client_id = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Client ID:',
            begin_entry_at=20
        )
        self.client_company = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Client company:',
            begin_entry_at=20
        )
        self.client_salutation = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Client salut.:',
            begin_entry_at=20
        )
        self.client_name = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Client name:',
            begin_entry_at=20
        )
        self.client_family_name = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Client fam. name:',
            begin_entry_at=20
        )
        self.client_street = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Client street:',
            begin_entry_at=20
        )
        self.client_post_code = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Client post code:',
            begin_entry_at=20
        )
        self.client_city = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Client city:',
            begin_entry_at=20
        )
        self.client_tax_id = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Client tax ID:',
            begin_entry_at=20
        )
        self.seperation = self.add_widget_intelligent(
            npyscreen.FixedText,
            editable=False
        )
        self.project_title = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Project title:',
            begin_entry_at=20
        )
        self.project_hours_per_day = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Project h / d:',
            begin_entry_at=20
        )
        self.project_work_days = self.add_widget_intelligent(
            npyscreen.TitleMultiSelect,
            name='Project days:',
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
        self.project_minimum_days = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Project min days:',
            begin_entry_at=20
        )

    def beforeEditing(self):
        """Get values from parentApp.tmpDefault object."""
        # simple strings
        self.client_id.value = self.parentApp.tmpDefault.client_id
        self.client_company.value = self.parentApp.tmpDefault.client_company
        self.client_salutation.value = self.parentApp.tmpDefault.client_salutation
        self.client_name.value = self.parentApp.tmpDefault.client_name
        self.client_family_name.value = self.parentApp.tmpDefault.client_family_name
        self.client_street.value = self.parentApp.tmpDefault.client_street
        self.client_post_code.value = self.parentApp.tmpDefault.client_post_code
        self.client_city.value = self.parentApp.tmpDefault.client_city
        self.client_tax_id.value = self.parentApp.tmpDefault.client_tax_id

        # another simple string or integers
        self.project_title.value = self.parentApp.tmpDefault.project_title
        self.project_hours_per_day.value = str(
            self.parentApp.tmpDefault.get_project_hours_per_day()
        )

        # handle the work_days
        self.project_work_days.value = self.parentApp.tmpDefault.get_project_work_days()

        # simple integer
        self.project_minimum_days.value = str(
            self.parentApp.tmpDefault.get_project_minimum_days()
        )

    def values_to_tmp(self):
        """Store values in temp object."""
        # get values into temp object
        self.parentApp.tmpDefault.client_id = self.client_id.value
        self.parentApp.tmpDefault.client_company = self.client_company.value
        self.parentApp.tmpDefault.client_salutation = self.client_salutation.value
        self.parentApp.tmpDefault.client_name = self.client_name.value
        self.parentApp.tmpDefault.client_family_name = self.client_family_name.value
        self.parentApp.tmpDefault.client_street = self.client_street.value
        self.parentApp.tmpDefault.client_post_code = self.client_post_code.value
        self.parentApp.tmpDefault.client_city = self.client_city.value
        self.parentApp.tmpDefault.client_tax_id = self.client_tax_id.value
        self.parentApp.tmpDefault.project_title = self.project_title.value
        self.parentApp.tmpDefault.set_project_hours_per_day(
            self.project_hours_per_day.value
        )
        self.parentApp.tmpDefault.set_project_work_days(self.project_work_days.value)
        self.parentApp.tmpDefault.set_project_minimum_days(
            self.project_minimum_days.value
        )

    def on_ok(self, keypress=None):
        """Check values and set them."""
        self.values_to_tmp()

        # get object and save files
        lang = self.parentApp.tmpDefault.language
        self.parentApp.S.defaults[lang] = self.parentApp.tmpDefault
        self.parentApp.S.save_settings_to_file()

        # switch back
        self.parentApp.setNextForm('Defaults')
        self.parentApp.switchFormNow()

    def on_cancel(self, keypress=None):
        """Go back without changing a thing."""
        # switch back
        self.parentApp.setNextForm('Defaults')
        self.parentApp.switchFormNow()


class DefaultsEntryForm(npyscreen.FormMultiPageActionWithMenus):
    """Form for editing the entry defaults."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(DefaultsEntryForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel
        })

    def switch_to_help(self):
        """Switch to the help screen."""
        self.values_to_tmp()
        self.parentApp.load_helptext('help_defaults_entry.txt')
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
        self.baseentry_title = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Base title:',
            begin_entry_at=20
        )
        self.baseentry_comment = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Base comment:',
            begin_entry_at=20
        )
        self.baseentry_amount = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Base amount:',
            begin_entry_at=20
        )
        self.baseentry_amount_format = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Base amount fmt:',
            begin_entry_at=20
        )
        self.baseentry_time = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Base time:',
            begin_entry_at=20
        )
        self.baseentry_price = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Base price:',
            begin_entry_at=20
        )
        self.add_widget_intelligent(
            npyscreen.FixedText,
            editable=False
        )
        self.multiplyentry_title = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Multi title:',
            begin_entry_at=20
        )
        self.multiplyentry_comment = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Multi comment:',
            begin_entry_at=20
        )
        self.multiplyentry_amount = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Multi amount:',
            begin_entry_at=20
        )
        self.multiplyentry_amount_format = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Multi amount fmt:',
            begin_entry_at=20
        )
        self.multiplyentry_hour_rate = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Multi h-rate:',
            begin_entry_at=20
        )
        self.add_widget_intelligent(
            npyscreen.FixedText,
            editable=False
        )
        self.connectentry_title = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Connect title:',
            begin_entry_at=20
        )
        self.connectentry_comment = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Connect comment:',
            begin_entry_at=20
        )
        self.connectentry_amount = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Connect amount:',
            begin_entry_at=20
        )
        self.connectentry_amount_format = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Con. amount fmt:',
            begin_entry_at=20
        )
        self.connectentry_multiplicator = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Connect multi:',
            begin_entry_at=20
        )
        self.connectentry_is_time = self.add_widget_intelligent(
            npyscreen.TitleMultiSelect,
            name='Connect is_time:',
            begin_entry_at=20,
            max_height=2,
            scroll_exit=True,
            values=['True']
        )

    def beforeEditing(self):
        """Get values form parentApp.tmpDefault."""
        self.baseentry_title.value = (
            self.parentApp.tmpDefault.baseentry_title
        )
        self.baseentry_comment.value = (
            self.parentApp.tmpDefault.baseentry_comment
        )
        self.baseentry_amount.value = str(
            self.parentApp.tmpDefault.get_baseentry_amount()
        )
        self.baseentry_amount_format.value = (
            self.parentApp.tmpDefault.baseentry_amount_format
        )
        self.baseentry_time.value = str(
            self.parentApp.tmpDefault.get_baseentry_time()
        )
        self.baseentry_price.value = str(
            self.parentApp.tmpDefault.get_baseentry_price()
        )
        self.multiplyentry_title.value = (
            self.parentApp.tmpDefault.multiplyentry_title
        )
        self.multiplyentry_comment.value = (
            self.parentApp.tmpDefault.multiplyentry_comment
        )
        self.multiplyentry_amount.value = str(
            self.parentApp.tmpDefault.get_multiplyentry_amount()
        )
        self.multiplyentry_amount_format.value = (
            self.parentApp.tmpDefault.multiplyentry_amount_format
        )
        self.multiplyentry_hour_rate.value = str(
            self.parentApp.tmpDefault.get_multiplyentry_hour_rate()
        )
        self.connectentry_title.value = (
            self.parentApp.tmpDefault.connectentry_title
        )
        self.connectentry_comment.value = (
            self.parentApp.tmpDefault.connectentry_comment
        )
        self.connectentry_amount.value = str(
            self.parentApp.tmpDefault.get_connectentry_amount()
        )
        self.connectentry_amount_format.value = (
            self.parentApp.tmpDefault.connectentry_amount_format
        )
        self.connectentry_multiplicator.value = str(
            self.parentApp.tmpDefault.get_connectentry_multiplicator()
        )
        self.connectentry_is_time.value = (
            [0] if self.parentApp.tmpDefault.get_connectentry_is_time() else []
        )

    def values_to_tmp(self):
        """Store values in temp object."""
        # get values in temp object
        self.parentApp.tmpDefault.baseentry_title = self.baseentry_title.value
        self.parentApp.tmpDefault.baseentry_comment = self.baseentry_comment.value
        self.parentApp.tmpDefault.set_baseentry_amount(
            self.baseentry_amount.value
        )
        self.parentApp.tmpDefault.baseentry_amount_format = (
            self.baseentry_amount_format.value
        )
        self.parentApp.tmpDefault.set_baseentry_time(
            float(self.baseentry_time.value)
        )
        self.parentApp.tmpDefault.set_baseentry_price(
            float(self.baseentry_price.value)
        )
        self.parentApp.tmpDefault.multiplyentry_title = self.multiplyentry_title.value
        self.parentApp.tmpDefault.multiplyentry_comment = (
            self.multiplyentry_comment.value
        )

        self.parentApp.tmpDefault.set_multiplyentry_amount(
            float(self.multiplyentry_amount.value)
        )
        self.parentApp.tmpDefault.multiplyentry_amount_format = (
            self.multiplyentry_amount_format.value
        )

        self.parentApp.tmpDefault.set_multiplyentry_hour_rate(
            float(self.multiplyentry_hour_rate.value)
        )
        self.parentApp.tmpDefault.connectentry_title = self.connectentry_title.value
        self.parentApp.tmpDefault.connectentry_comment = self.connectentry_comment.value

        self.parentApp.tmpDefault.set_connectentry_amount(
            float(self.connectentry_amount.value)
        )
        self.parentApp.tmpDefault.connectentry_amount_format = (
            self.connectentry_amount_format.value
        )

        self.parentApp.tmpDefault.set_connectentry_multiplicator(
            float(self.connectentry_multiplicator.value)
        )
        self.parentApp.tmpDefault.set_connectentry_is_time(
            self.connectentry_is_time.value
        )

    def on_ok(self, keypress=None):
        """Check values and set them."""
        self.values_to_tmp()

        # get object and save files
        lang = self.parentApp.tmpDefault.language
        self.parentApp.S.defaults[lang] = self.parentApp.tmpDefault
        self.parentApp.S.save_settings_to_file()

        # switch back
        self.parentApp.setNextForm('Defaults')
        self.parentApp.switchFormNow()

    def on_cancel(self, keypress=None):
        """Go back without changing a thing."""
        # switch back
        self.parentApp.setNextForm('Defaults')
        self.parentApp.switchFormNow()
