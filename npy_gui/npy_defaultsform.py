"""Form for the defaults."""

from decimal import Decimal
import npyscreen


class DefaultChooseList(npyscreen.MultiLineAction):
    """The list holding the choosable default entries."""

    def actionHighlighted(self, act_on_this, keypress):
        """Do something, because a key was pressed."""
        # general was chosen
        if act_on_this == 'General defaults':
            # go to the Defaults_general form
            self.parent.parentApp.setNextForm('Defaults_general')
            self.parent.parentApp.switchFormNow()

        # client and project was chosen
        elif act_on_this == 'Client and project defaults':
            # go to the Defaults_clientproject form
            self.parent.parentApp.setNextForm('Defaults_clientproject')
            self.parent.parentApp.switchFormNow()

        # entry was chosen
        elif act_on_this == 'Entry defaults':
            # go to the Defaults_clientproject form
            self.parent.parentApp.setNextForm('Defaults_entry')
            self.parent.parentApp.switchFormNow()


class DefaultsForm(npyscreen.ActionFormWithMenus):
    """Form for editing the defaults."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(DefaultsForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel
        })

    def switch_to_help(self):
        """Switch to the help screen."""
        self.parentApp.load_helptext('help_defaults.txt')
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
        """Go back without changing a thing."""
        # switch back
        self.parentApp.setNextForm('Settings')
        self.parentApp.switchFormNow()


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
        self.date_fmt.value = self.parentApp.tmpDefault.date_fmt
        self.project_wage.value = str(float(self.parentApp.tmpDefault.project_wage))
        self.commodity.value = self.parentApp.tmpDefault.commodity

    def values_to_tmp(self):
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

        offer_title = self.offer_title.value
        offer_template = self.offer_template.value
        offer_filename = self.offer_filename.value
        date_fmt = self.date_fmt.value

        try:
            wage = Decimal(self.project_wage.value)
        except Exception:
            wage = self.parentApp.tmpDefault.project_wage

        commodity = self.commodity.value

        # check things
        lang_exists = language in self.parentApp.S.defaults.keys()
        lang_equal_old = language == lang_old

        # create cases
        case_create_new = self.parentApp.tmpDefault_new and not lang_exists
        case_modify_actual = not self.parentApp.tmpDefault_new and lang_equal_old
        case_rename_actual = not self.parentApp.tmpDefault_new and not lang_equal_old

        # get stuff into tmpDefault
        self.parentApp.tmpDefault.language = language
        self.parentApp.tmpDefault.offer_title = offer_title
        self.parentApp.tmpDefault.offer_template = offer_template
        self.parentApp.tmpDefault.offer_filename = offer_filename
        self.parentApp.tmpDefault.date_fmt = date_fmt
        self.parentApp.tmpDefault.project_wage = wage
        self.parentApp.tmpDefault.commodity = commodity

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
        allright = self.values_to_tmp()

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
        self.client_language = self.add_widget_intelligent(
            npyscreen.TitleSelectOne,
            name='Client language:',
            begin_entry_at=20,
            max_height=4,
            scroll_exit=True,
            value=[0]
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
        self.client_company.value = self.parentApp.tmpDefault.client_company
        self.client_salutation.value = self.parentApp.tmpDefault.client_salutation
        self.client_name.value = self.parentApp.tmpDefault.client_name
        self.client_family_name.value = self.parentApp.tmpDefault.client_family_name
        self.client_street.value = self.parentApp.tmpDefault.client_street
        self.client_post_code.value = self.parentApp.tmpDefault.client_post_code
        self.client_city.value = self.parentApp.tmpDefault.client_city
        self.client_tax_id.value = self.parentApp.tmpDefault.client_tax_id

        # handle languages
        self.client_language.values = self.parentApp.S.languages

        c_lang = self.parentApp.tmpDefault.client_language
        if c_lang in self.client_language.values:
            self.client_language.value[0] = self.client_language.values.index(
                c_lang
            )
        else:
            self.client_language.value[0] = 0

        # another simple string or integers
        self.project_title.value = self.parentApp.tmpDefault.project_title
        self.project_hours_per_day.value = str(
            self.parentApp.tmpDefault.project_hours_per_day
        )

        # handle the work_days
        self.project_work_days.value = self.parentApp.tmpDefault.project_work_days

        # simple integer
        self.project_minimum_days.value = str(
            self.parentApp.tmpDefault.project_minimum_days
        )

    def values_to_tmp(self):
        """Store values in temp object."""
        # get values in temp variables
        client_company = self.client_company.value
        client_salutation = self.client_salutation.value
        client_name = self.client_name.value
        client_family_name = self.client_family_name.value
        client_street = self.client_street.value
        client_post_code = self.client_post_code.value
        client_city = self.client_city.value
        client_tax_id = self.client_tax_id.value
        client_language = self.client_language.values[
            self.client_language.value[0]
        ]
        project_title = self.project_title.value

        # try to convert input to int
        try:
            project_hours_per_day = int(self.project_hours_per_day.value)
        except Exception:
            project_hours_per_day = self.parentApp.tmpDefault.project_hours_per_day

        project_work_days = self.project_work_days.value

        # try to convert input to int
        try:
            project_minimum_days = int(self.project_minimum_days.value)
        except Exception:
            project_minimum_days = self.parentApp.tmpDefault.project_minimum_days

        # assign back to the S variable
        self.parentApp.tmpDefault.client_company = client_company
        self.parentApp.tmpDefault.client_salutation = client_salutation
        self.parentApp.tmpDefault.client_name = client_name
        self.parentApp.tmpDefault.client_family_name = client_family_name
        self.parentApp.tmpDefault.client_street = client_street
        self.parentApp.tmpDefault.client_post_code = client_post_code
        self.parentApp.tmpDefault.client_city = client_city
        self.parentApp.tmpDefault.client_tax_id = client_tax_id
        self.parentApp.tmpDefault.client_language = client_language
        self.parentApp.tmpDefault.project_title = project_title
        self.parentApp.tmpDefault.project_hours_per_day = project_hours_per_day
        self.parentApp.tmpDefault.project_work_days = project_work_days
        self.parentApp.tmpDefault.project_minimum_days = project_minimum_days

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
            self.parentApp.tmpDefault.baseentry_amount
        )
        self.baseentry_amount_format.value = (
            self.parentApp.tmpDefault.baseentry_amount_format
        )
        self.baseentry_time.value = str(
            self.parentApp.tmpDefault.baseentry_time
        )
        self.baseentry_price.value = str(
            self.parentApp.tmpDefault.baseentry_price
        )
        self.multiplyentry_title.value = (
            self.parentApp.tmpDefault.multiplyentry_title
        )
        self.multiplyentry_comment.value = (
            self.parentApp.tmpDefault.multiplyentry_comment
        )
        self.multiplyentry_amount.value = str(
            self.parentApp.tmpDefault.multiplyentry_amount
        )
        self.multiplyentry_amount_format.value = (
            self.parentApp.tmpDefault.multiplyentry_amount_format
        )
        self.multiplyentry_hour_rate.value = str(
            self.parentApp.tmpDefault.multiplyentry_hour_rate
        )
        self.connectentry_title.value = (
            self.parentApp.tmpDefault.connectentry_title
        )
        self.connectentry_comment.value = (
            self.parentApp.tmpDefault.connectentry_comment
        )
        self.connectentry_amount.value = str(
            self.parentApp.tmpDefault.connectentry_amount
        )
        self.connectentry_amount_format.value = (
            self.parentApp.tmpDefault.connectentry_amount_format
        )
        self.connectentry_multiplicator.value = str(
            self.parentApp.tmpDefault.connectentry_multiplicator
        )
        self.connectentry_is_time.value = (
            [0] if self.parentApp.tmpDefault.connectentry_is_time else []
        )

    def values_to_tmp(self):
        """Store values in temp object."""
        # get values in temp variables
        baseentry_title = self.baseentry_title.value
        baseentry_comment = self.baseentry_comment.value

        # try to convert input to float
        try:
            baseentry_amount = float(self.baseentry_amount.value)
        except Exception:
            baseentry_amount = self.parentApp.tmpDefault.baseentry_amount

        baseentry_amount_format = self.baseentry_amount_format.value

        # try to convert input to float
        try:
            baseentry_time = float(self.baseentry_time.value)
        except Exception:
            baseentry_time = self.parentApp.tmpDefault.baseentry_time

        # try to convert input to float
        try:
            baseentry_price = float(self.baseentry_price.value)
        except Exception:
            baseentry_price = self.parentApp.tmpDefault.baseentry_price

        multiplyentry_title = self.multiplyentry_title.value
        multiplyentry_comment = self.multiplyentry_comment.value

        # try to convert input to float
        try:
            multiplyentry_amount = float(self.multiplyentry_amount.value)
        except Exception:
            multiplyentry_amount = self.parentApp.tmpDefault.multiplyentry_amount

        multiplyentry_amount_format = self.multiplyentry_amount_format.value

        # try to convert input to float
        try:
            multiplyentry_hour_rate = float(self.multiplyentry_hour_rate.value)
        except Exception:
            multiplyentry_hour_rate = self.parentApp.tmpDefault.multiplyentry_hour_rate

        connectentry_title = self.connectentry_title.value
        connectentry_comment = self.connectentry_comment.value

        # try to convert input to float
        try:
            connectentry_amount = float(self.connectentry_amount.value)
        except Exception:
            connectentry_amount = self.parentApp.tmpDefault.connectentry_amount

        connectentry_amount_format = self.connectentry_amount_format.value

        # try to convert input to float
        try:
            connectentry_multiplicator = float(self.connectentry_multiplicator.value)
        except Exception:
            connectentry_multiplicator = (
                self.parentApp.tmpDefault.connectentry_multiplicator
            )

        # get boolean out of selection
        connectentry_is_time = (
            True if self.connectentry_is_time.value == [0] else False
        )

        # assign back to the S variable
        self.parentApp.tmpDefault.baseentry_title = (
            baseentry_title
        )
        self.parentApp.tmpDefault.baseentry_comment = (
            baseentry_comment
        )
        self.parentApp.tmpDefault.baseentry_amount = (
            baseentry_amount
        )
        self.parentApp.tmpDefault.baseentry_amount_format = (
            baseentry_amount_format
        )
        self.parentApp.tmpDefault.baseentry_time = (
            baseentry_time
        )
        self.parentApp.tmpDefault.baseentry_price = (
            baseentry_price
        )
        self.parentApp.tmpDefault.multiplyentry_title = (
            multiplyentry_title
        )
        self.parentApp.tmpDefault.multiplyentry_comment = (
            multiplyentry_comment
        )
        self.parentApp.tmpDefault.multiplyentry_amount = (
            multiplyentry_amount
        )
        self.parentApp.tmpDefault.multiplyentry_amount_format = (
            multiplyentry_amount_format
        )
        self.parentApp.tmpDefault.multiplyentry_hour_rate = (
            multiplyentry_hour_rate
        )
        self.parentApp.tmpDefault.connectentry_title = (
            connectentry_title
        )
        self.parentApp.tmpDefault.connectentry_comment = (
            connectentry_comment
        )
        self.parentApp.tmpDefault.connectentry_amount = (
            connectentry_amount
        )
        self.parentApp.tmpDefault.connectentry_amount_format = (
            connectentry_amount_format
        )
        self.parentApp.tmpDefault.connectentry_multiplicator = (
            connectentry_multiplicator
        )
        self.parentApp.tmpDefault.connectentry_is_time = (
            connectentry_is_time
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
