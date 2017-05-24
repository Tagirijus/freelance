"""Form for the defaults."""

import curses
import npyscreen
import os


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

        # offer was chosen
        elif act_on_this == 'Offer defaults':
            # generate name for form
            tit = 'Freelance > Settings > Defaults ({}) > Offer'
            self.parent.parentApp.getForm('Defaults_offer').name = tit.format(
                self.parent.parentApp.tmpDefault.language
            )

            # go to the Defaults_general form
            self.parent.parentApp.setNextForm('Defaults_offer')
            self.parent.parentApp.switchFormNow()

        # invoice was chosen
        elif act_on_this == 'Invoice defaults':
            # generate name for form
            tit = 'Freelance > Settings > Defaults ({}) > Invoice'
            self.parent.parentApp.getForm('Defaults_invoice').name = tit.format(
                self.parent.parentApp.tmpDefault.language
            )

            # go to the Defaults_general form
            self.parent.parentApp.setNextForm('Defaults_invoice')
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
                'Offer defaults',
                'Invoice defaults',
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


class TemplatesListAction(npyscreen.MultiLineAction):
    """List holding the offer templates."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(TemplatesListAction, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            curses.KEY_IC: self.add_template,
            curses.KEY_DC: self.delete_template
        })

        # additional attributes
        self.offerinvoice = ''

    def update_values(self):
        """Update values and refresh view."""
        if self.offerinvoice == 'offer':
            self.values = self.parent.parentApp.tmpDefault.get_offer_templates_as_list()
        else:
            self.values = self.parent.parentApp.tmpDefault.get_invoice_templates_as_list()

        self.display()
        self.clear_filter()

    def add_template(self, keypress=None):
        """Add template."""
        file = npyscreen.selectFile(
            starting_value=os.path.expanduser('~'),
            confirm_if_exists=False
        )

        name = npyscreen.notify_input(
            'Name of template:'
        )

        # add if name and not exists in dict
        if self.offerinvoice == 'offer':
            if (
                name and
                name not in self.parent.parentApp.tmpDefault.get_offer_templates()
            ):
                self.parent.parentApp.tmpDefault.add_offer_template(
                    key=name, value=file
                )
        else:
            if (
                name and
                name not in self.parent.parentApp.tmpDefault.get_invoice_templates()
            ):
                self.parent.parentApp.tmpDefault.add_invoice_template(
                    key=name, value=file
                )

        self.update_values()

    def delete_template(self, keypress=None):
        """Delete template."""
        # cancel if there are no values
        if len(self.values) < 1:
            return False

        selected = self.values[self.cursor_line][0]

        really = npyscreen.notify_yes_no(
            'Really delete template "{}"?'.format(selected)
        )

        if really:
            if self.offerinvoice == 'offer':
                self.parent.parentApp.tmpDefault.del_offer_template(key=selected)
            else:
                self.parent.parentApp.tmpDefault.del_invoice_template(key=selected)

            self.update_values()

    def display_value(self, vl):
        """Display the value."""
        return '[{}]'.format(vl[0])

    def actionHighlighted(self, act_on_this, keypress):
        """Do something, because a key was pressed."""
        # cancel if there are no values
        if len(self.values) < 1:
            return False

        # get old
        old_key = act_on_this[0]
        old_val = act_on_this[1]

        # ask new stuff
        file = npyscreen.selectFile(
            starting_value=old_val,
            confirm_if_exists=False
        )

        name = npyscreen.notify_input(
            'Name of template:',
            pre_text=old_key
        )

        if name:
            if self.offerinvoice == 'offer':
                self.parent.parentApp.tmpDefault.del_offer_template(key=old_key)
                self.parent.parentApp.tmpDefault.add_offer_template(
                    key=name, value=file
                )
            else:
                self.parent.parentApp.tmpDefault.del_invoice_template(key=old_key)
                self.parent.parentApp.tmpDefault.add_invoice_template(
                    key=name, value=file
                )

            self.update_values()


class TitleTemplatesList(npyscreen.TitleMultiLine):
    """Inherit from TitleMultiLine, but get MultiLineAction."""

    _entry_type = TemplatesListAction


class TitleMultiLineEdit(npyscreen.TitleText):
    """Titled MultiLineEdit."""

    _entry_type = npyscreen.MultiLineEdit
    scroll_exit = True

    def reformat(self):
        """Reformat the content."""
        self.entry_widget.full_reformat()


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
            begin_entry_at=26
        )
        self.date_fmt = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Date format:',
            begin_entry_at=26
        )
        self.project_wage = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Wage:',
            begin_entry_at=26
        )
        self.commodity = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Commodity:',
            begin_entry_at=26
        )

    def beforeEditing(self):
        """Get the values from the active tmpDefault variable."""
        self.language.value = self.parentApp.tmpDefault.language

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
                self.parentApp.tmpDefault_new = False
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


class DefaultsOfferForm(npyscreen.FormMultiPageActionWithMenus):
    """Form for editing the general defaults."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(DefaultsOfferForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel
        })

    def add_temp(self):
        """Add template."""
        self.offer_templates.entry_widget.add_template()

    def del_temp(self):
        """Delete template."""
        self.offer_templates.entry_widget.delete_template()

    def switch_to_help(self):
        """Switch to the help screen."""
        self.values_to_tmp()
        self.parentApp.load_helptext('help_defaults_offer.txt')
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
        self.m.addItem(text='Add offer template', onSelect=self.add_temp, shortcut='a')
        self.m.addItem(text='Del offer template', onSelect=self.del_temp, shortcut='d')
        self.m.addItem(text='Help', onSelect=self.switch_to_help, shortcut='h')
        self.m.addItem(text='Exit', onSelect=self.exit, shortcut='e')

        # create the input widgets
        self.offer_title = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Offer title:',
            begin_entry_at=26
        )
        self.offer_comment = self.add_widget_intelligent(
            TitleMultiLineEdit,
            name='Offer comment:',
            begin_entry_at=26,
            max_height=2,
            value=''
        )
        self.offer_filename = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Offer filename:',
            begin_entry_at=26
        )
        self.offer_round_price = self.add_widget_intelligent(
            npyscreen.TitleMultiSelect,
            name='Offer round price:',
            begin_entry_at=26,
            max_height=2,
            scroll_exit=True,
            values=['enabled']
        )
        self.offer_templates = self.add_widget_intelligent(
            TitleTemplatesList,
            name='Offer templates:',
            begin_entry_at=26,
            max_height=2,
            scroll_exit=True
        )
        self.offer_templates.entry_widget.offerinvoice = 'offer'

    def beforeEditing(self):
        """Get the values from the active tmpDefault variable."""
        self.language = self.parentApp.tmpDefault.language
        self.offer_title.value = self.parentApp.tmpDefault.offer_title
        self.offer_comment.value = self.parentApp.tmpDefault.offer_comment
        self.offer_comment.reformat()
        self.offer_filename.value = self.parentApp.tmpDefault.offer_filename
        self.offer_round_price.value = (
            [0] if self.parentApp.tmpDefault.get_offer_round_price() else []
        )
        self.offer_templates.entry_widget.update_values()

    def values_to_tmp(self, save=False):
        """Store values to temp object."""
        # get stuff into tmpDefault
        self.parentApp.tmpDefault.offer_title = self.offer_title.value
        self.parentApp.tmpDefault.offer_comment = self.offer_comment.value.replace(
            '\n', ' '
        )
        self.parentApp.tmpDefault.offer_filename = self.offer_filename.value
        if self.offer_round_price.value == [0]:
            self.parentApp.tmpDefault.set_offer_round_price(True)
        else:
            self.parentApp.tmpDefault.set_offer_round_price(False)
        self.parentApp.tmpDefault.set_offer_templates(self.offer_templates.values)

        # save or not?
        if not save:
            return False

        language = self.parentApp.tmpDefault.language

        # create new
        if self.parentApp.tmpDefault_new:
            # try to create a new one
            new_created = self.parentApp.S.new_default(language)
            if new_created:
                self.parentApp.S.defaults[language] = self.parentApp.tmpDefault.copy()
                self.parentApp.tmpDefault_new = False
                return True
            else:
                # did not work, go on editing
                return False

        # modify actual
        else:
            # simply modify the selected one - no name change
            self.parentApp.S.defaults[language] = self.parentApp.tmpDefault.copy()
            return True

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


class DefaultsInvoiceForm(npyscreen.FormMultiPageActionWithMenus):
    """Form for editing the general defaults."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(DefaultsInvoiceForm, self).__init__(*args, **kwargs)

        # set up key shortcuts
        self.add_handlers({
            '^O': self.on_ok,
            '^Q': self.on_cancel
        })

    def add_temp(self):
        """Add template."""
        self.invoice_templates.entry_widget.add_template()

    def del_temp(self):
        """Delete template."""
        self.invoice_templates.entry_widget.delete_template()

    def switch_to_help(self):
        """Switch to the help screen."""
        self.values_to_tmp()
        self.parentApp.load_helptext('help_defaults_invoice.txt')
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
        self.m.addItem(text='Add invoice template', onSelect=self.add_temp, shortcut='a')
        self.m.addItem(text='Del invoice template', onSelect=self.del_temp, shortcut='d')
        self.m.addItem(text='Help', onSelect=self.switch_to_help, shortcut='h')
        self.m.addItem(text='Exit', onSelect=self.exit, shortcut='e')

        # create the input widgets
        self.invoice_title = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Invoice title:',
            begin_entry_at=26
        )
        self.invoice_id = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Invoice ID:',
            begin_entry_at=26
        )
        self.invoice_comment = self.add_widget_intelligent(
            TitleMultiLineEdit,
            name='Invoice comment:',
            begin_entry_at=26,
            max_height=2,
            value=''
        )
        self.invoice_filename = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Invoice filename:',
            begin_entry_at=26
        )
        self.invoice_round_price = self.add_widget_intelligent(
            npyscreen.TitleMultiSelect,
            name='Invoice round price:',
            begin_entry_at=26,
            max_height=2,
            scroll_exit=True,
            values=['enabled']
        )
        self.invoice_templates = self.add_widget_intelligent(
            TitleTemplatesList,
            name='Invoice templates:',
            begin_entry_at=26,
            max_height=2,
            scroll_exit=True
        )
        self.invoice_templates.entry_widget.offerinvoice = 'invoice'
        self.invoice_due_days = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Invoice due days:',
            begin_entry_at=26
        )

    def beforeEditing(self):
        """Get the values from the active tmpDefault variable."""
        self.invoice_title.value = self.parentApp.tmpDefault.invoice_title
        self.invoice_id.value = self.parentApp.tmpDefault.invoice_id
        self.invoice_comment.value = self.parentApp.tmpDefault.invoice_comment
        self.invoice_comment.reformat()
        self.invoice_filename.value = self.parentApp.tmpDefault.invoice_filename
        self.invoice_round_price.value = (
            [0] if self.parentApp.tmpDefault.get_invoice_round_price() else []
        )
        self.invoice_templates.entry_widget.update_values()
        self.invoice_due_days.value = str(
            self.parentApp.tmpDefault.get_invoice_due_days()
        )

    def values_to_tmp(self, save=False):
        """Store values to temp object."""
        # get values in temp variables
        self.parentApp.tmpDefault.invoice_title = self.invoice_title.value
        self.parentApp.tmpDefault.invoice_id = self.invoice_id.value
        self.parentApp.tmpDefault.invoice_comment = self.invoice_comment.value.replace(
            '\n', ' '
        )
        self.parentApp.tmpDefault.invoice_filename = self.invoice_filename.value
        if self.invoice_round_price.value == [0]:
            self.parentApp.tmpDefault.set_invoice_round_price(True)
        else:
            self.parentApp.tmpDefault.set_invoice_round_price(False)
        self.parentApp.tmpDefault.set_invoice_templates(self.invoice_templates.values)
        self.parentApp.tmpDefault.set_invoice_due_days(self.invoice_due_days.value)

        language = self.parentApp.tmpDefault.language

        # save or not?
        if not save:
            return False

        # check case
        if self.parentApp.tmpDefault_new:
            # try to create a new one
            new_created = self.parentApp.S.new_default(language)
            if new_created:
                self.parentApp.S.defaults[language] = self.parentApp.tmpDefault.copy()
                self.parentApp.tmpDefault_new = False
                return True
            else:
                # did not work, go on editing
                return False

        else:
            # simply modify the selected one - no name change
            self.parentApp.S.defaults[language] = self.parentApp.tmpDefault.copy()
            return True

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
            begin_entry_at=26
        )
        self.client_company = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Client company:',
            begin_entry_at=26
        )
        self.client_attention = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Client attn.:',
            begin_entry_at=26
        )
        self.client_salutation = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Client salut.:',
            begin_entry_at=26
        )
        self.client_name = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Client name:',
            begin_entry_at=26
        )
        self.client_family_name = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Client fam. name:',
            begin_entry_at=26
        )
        self.client_street = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Client street:',
            begin_entry_at=26
        )
        self.client_post_code = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Client post code:',
            begin_entry_at=26
        )
        self.client_city = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Client city:',
            begin_entry_at=26
        )
        self.client_tax_id = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Client tax ID:',
            begin_entry_at=26
        )
        self.seperation = self.add_widget_intelligent(
            npyscreen.FixedText,
            editable=False
        )
        self.project_title = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Project title:',
            begin_entry_at=26
        )
        self.project_hours_per_day = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Project h / d:',
            begin_entry_at=26
        )
        self.project_work_days = self.add_widget_intelligent(
            npyscreen.TitleMultiSelect,
            name='Project days:',
            begin_entry_at=26,
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
            begin_entry_at=26
        )

    def beforeEditing(self):
        """Get values from parentApp.tmpDefault object."""
        # simple strings
        self.client_id.value = self.parentApp.tmpDefault.client_id
        self.client_company.value = self.parentApp.tmpDefault.client_company
        self.client_attention.value = self.parentApp.tmpDefault.client_attention
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
        self.parentApp.tmpDefault.client_attention = self.client_attention.value
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
            begin_entry_at=26
        )
        self.baseentry_comment = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Base comment:',
            begin_entry_at=26
        )
        self.baseentry_amount = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Base amount:',
            begin_entry_at=26
        )
        self.baseentry_amount_format = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Base amount fmt:',
            begin_entry_at=26
        )
        self.baseentry_time = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Base time:',
            begin_entry_at=26
        )
        self.baseentry_price = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Base price:',
            begin_entry_at=26
        )
        self.add_widget_intelligent(
            npyscreen.FixedText,
            editable=False
        )
        self.multiplyentry_title = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Multi title:',
            begin_entry_at=26
        )
        self.multiplyentry_comment = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Multi comment:',
            begin_entry_at=26
        )
        self.multiplyentry_amount = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Multi amount:',
            begin_entry_at=26
        )
        self.multiplyentry_amount_format = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Multi amount fmt:',
            begin_entry_at=26
        )
        self.multiplyentry_hour_rate = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Multi h-rate:',
            begin_entry_at=26
        )
        self.add_widget_intelligent(
            npyscreen.FixedText,
            editable=False
        )
        self.connectentry_title = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Connect title:',
            begin_entry_at=26
        )
        self.connectentry_comment = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Connect comment:',
            begin_entry_at=26
        )
        self.connectentry_amount = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Connect amount:',
            begin_entry_at=26
        )
        self.connectentry_amount_format = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Con. amount fmt:',
            begin_entry_at=26
        )
        self.connectentry_multiplicator = self.add_widget_intelligent(
            npyscreen.TitleText,
            name='Connect multi:',
            begin_entry_at=26
        )
        self.connectentry_is_time = self.add_widget_intelligent(
            npyscreen.TitleMultiSelect,
            name='Connect is_time:',
            begin_entry_at=26,
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
