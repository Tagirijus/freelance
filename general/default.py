"""The class holding all the default texts."""

from decimal import Decimal
import json
from offer.offeramounttime import OfferAmountTime
import os


class Default(object):
    """Settings class."""

    def __init__(
        self,
        data_path=None,
        language=None,
        offer_title=None,
        offer_comment=None,
        offer_comment_b=None,
        offer_filename=None,
        offer_round_price=None,
        offer_templates=None,
        invoice_title=None,
        invoice_id=None,
        invoice_comment=None,
        invoice_comment_b=None,
        invoice_filename=None,
        invoice_round_price=None,
        invoice_templates=None,
        invoice_due_days=None,
        invoice_delivery=None,
        date_fmt=None,
        commodity=None,
        client_id=None,
        client_company=None,
        client_company_b=None,
        client_attention=None,
        client_salutation=None,
        client_name=None,
        client_family_name=None,
        client_street=None,
        client_post_code=None,
        client_city=None,
        client_country=None,
        client_tax_id=None,
        client_language=None,
        project_title=None,
        project_hours_per_day=None,
        project_work_days=None,
        project_minimum_days=None,
        project_wage=None,
        baseentry_title=None,
        baseentry_comment=None,
        baseentry_amount=None,
        baseentry_amount_format=None,
        baseentry_amount_b=None,
        baseentry_amount_b_format=None,
        baseentry_time=None,
        baseentry_price=None,
        multiplyentry_title=None,
        multiplyentry_comment=None,
        multiplyentry_amount=None,
        multiplyentry_amount_format=None,
        multiplyentry_amount_b=None,
        multiplyentry_amount_b_format=None,
        multiplyentry_hour_rate=None,
        connectentry_title=None,
        connectentry_comment=None,
        connectentry_amount=None,
        connectentry_amount_format=None,
        connectentry_amount_b=None,
        connectentry_amount_b_format=None,
        connectentry_is_time=None,
        connectentry_multiplicator=None
    ):
        """Initialize the class and hard code defaults, if no file is given."""
        self.language = 'NEW' if language is None else language

        self.offer_title = '' if offer_title is None else offer_title
        self.offer_comment = '' if offer_comment is None else offer_comment
        self.offer_comment_b = '' if offer_comment_b is None else offer_comment_b
        self.offer_filename = '' if offer_filename is None else offer_filename
        self.set_offer_round_price(
            False if offer_round_price is None else offer_round_price
        )
        self._offer_templates = {}                      # set default
        self.set_offer_templates(offer_templates)       # try to set arguments value

        self.invoice_title = '' if invoice_title is None else invoice_title
        self.invoice_id = '' if invoice_id is None else invoice_id
        self.invoice_comment = '' if invoice_comment is None else invoice_comment
        self.invoice_comment_b = '' if invoice_comment_b is None else invoice_comment_b
        self.invoice_filename = '' if invoice_filename is None else invoice_filename
        self.set_invoice_round_price(
            False if invoice_round_price is None else invoice_round_price
        )
        self._invoice_templates = {}                        # set default
        self.set_invoice_templates(invoice_templates)       # try to set arguments value
        self._invoice_due_days = 14                         # set default
        self.set_invoice_due_days(invoice_due_days)         # try to set arguments value
        self.invoice_delivery = '' if invoice_delivery is None else invoice_delivery

        self.date_fmt = '' if date_fmt is None else date_fmt
        self.commodity = '' if commodity is None else commodity

        # client default values
        self.client_id = '{CLIENT_COUNT}' if client_id is None else client_id
        self.client_company = '' if client_company is None else client_company
        self.client_company_b = '' if client_company_b is None else client_company_b
        self.client_attention = 'Attn.' if client_attention is None else client_attention
        self.client_salutation = '' if client_salutation is None else client_salutation
        self.client_name = '' if client_name is None else client_name
        self.client_family_name = '' if client_family_name is None else client_family_name
        self.client_street = '' if client_street is None else client_street

        self.client_post_code = '' if client_post_code is None else client_post_code
        self.client_city = '' if client_city is None else client_city
        self.client_country = '' if client_country is None else client_country
        self.client_tax_id = '' if client_tax_id is None else client_tax_id
        self.client_language = 'en' if client_language is None else client_language

        # project default values
        self.project_title = '{PROJECT_COUNT}' if project_title is None else project_title
        self._project_hours_per_day = 0
        self.set_project_hours_per_day(project_hours_per_day)
        self._project_work_days = [0, 1, 2, 3, 4]
        self.set_project_work_days(project_work_days)
        self._project_minimum_days = 2
        self.set_project_minimum_days(project_minimum_days)
        self._project_wage = Decimal(0)
        self.set_project_wage(project_wage)

        # baseentry default values
        self.baseentry_title = '' if baseentry_title is None else baseentry_title
        self.baseentry_comment = '' if baseentry_comment is None else baseentry_comment
        self._baseentry_amount = OfferAmountTime(baseentry_amount)
        self.baseentry_amount_format = ('' if baseentry_amount_format is None
                                        else baseentry_amount_format)
        if baseentry_amount_b is None:
            self._baseentry_amount_b = OfferAmountTime(1)
        else:
            self._baseentry_amount_b = OfferAmountTime(baseentry_amount_b)
        self.baseentry_amount_b_format = ('' if baseentry_amount_b_format is None
                                        else baseentry_amount_b_format)
        self._baseentry_time = OfferAmountTime(baseentry_time)
        self._baseentry_price = Decimal(0)
        self.set_baseentry_price(baseentry_price)

        # multiplyentry default values
        self.multiplyentry_title = ('' if multiplyentry_title is None else
                                    multiplyentry_title)
        self.multiplyentry_comment = ('' if multiplyentry_comment is None else
                                      multiplyentry_comment)
        self._multiplyentry_amount = OfferAmountTime(multiplyentry_amount)
        self.multiplyentry_amount_format = ('' if multiplyentry_amount_format is None
                                            else multiplyentry_amount_format)
        if multiplyentry_amount_b is None:
            self._multiplyentry_amount_b = OfferAmountTime(1)
        else:
            self._multiplyentry_amount_b = OfferAmountTime(multiplyentry_amount_b)
        self.multiplyentry_amount_b_format = ('' if multiplyentry_amount_b_format is None
                                            else multiplyentry_amount_b_format)
        self._multiplyentry_hour_rate = OfferAmountTime(multiplyentry_hour_rate)

        # connectentry default values
        self.connectentry_title = ('' if connectentry_title is None else
                                   connectentry_title)
        self.connectentry_comment = ('' if connectentry_comment is None else
                                     connectentry_comment)
        self._connectentry_amount = OfferAmountTime(connectentry_amount)
        self.connectentry_amount_format = ('' if connectentry_amount_format is None else
                                           connectentry_amount_format)
        if connectentry_amount_b is None:
            self._connectentry_amount_b = OfferAmountTime(1)
        else:
            self._connectentry_amount_b = OfferAmountTime(connectentry_amount_b)
        self.connectentry_amount_b_format = (
            '' if connectentry_amount_b_format is None else connectentry_amount_b_format
        )
        self.set_connectentry_is_time(
            True if connectentry_is_time is None else connectentry_is_time
        )
        self._connectentry_multiplicator = Decimal(0)
        self.set_connectentry_multiplicator(connectentry_multiplicator)

        # try to load default automatically
        if data_path is not None:
            self.load_settings_from_file(data_path)

    def set_offer_round_price(self, value):
        """Set offer_round_price."""
        self._offer_round_price = bool(value)

    def get_offer_round_price(self):
        """Get offer_round_price."""
        return self._offer_round_price

    def set_offer_templates(self, value):
        """Set offer_templates."""
        if type(value) is dict:
            self._offer_templates = value
        elif type(value) is list:
            self._offer_templates = {}
            for x in value:
                self.add_offer_template(x[0], x[1])

    def get_offer_templates_as_list(self):
        """Get offer_templates as list with tuples of key+value."""
        return [(key, self._offer_templates[key]) for key in self._offer_templates]

    def get_offer_templates(self):
        """Get offer_templates as dict."""
        return self._offer_templates

    def add_offer_template(self, key, value):
        """Add to offer_templates."""
        self._offer_templates[key] = value

    def del_offer_template(self, key):
        """Try to delete offer_templates entry."""
        if key in self._offer_templates:
            del self._offer_templates[key]

    def set_invoice_round_price(self, value):
        """Set invoice_round_price."""
        self._invoice_round_price = bool(value)

    def get_invoice_round_price(self):
        """Get invoice_round_price."""
        return self._invoice_round_price

    def set_invoice_templates(self, value):
        """Set invoice_templates."""
        if type(value) is dict:
            self._invoice_templates = value
        elif type(value) is list:
            self._invoice_templates = {}
            for x in value:
                self.add_invoice_template(x[0], x[1])

    def get_invoice_templates_as_list(self):
        """Get invoice_templates as list with tuples of key+value."""
        return [(key, self._invoice_templates[key]) for key in self._invoice_templates]

    def get_invoice_templates(self):
        """Get invoice_templates as dict."""
        return self._invoice_templates

    def add_invoice_template(self, key, value):
        """Add to invoice_templates."""
        self._invoice_templates[key] = value

    def del_invoice_template(self, key):
        """Try to delete invoice_templates entry."""
        if key in self._invoice_templates:
            del self._invoice_templates[key]

    def set_invoice_due_days(self, value):
        """Set invoice_due_days."""
        try:
            self._invoice_due_days = int(value)
        except Exception:
            pass

    def get_invoice_due_days(self):
        """Get invoice_due_days."""
        return self._invoice_due_days

    def set_project_hours_per_day(self, value):
        """Set project_hours_per_day."""
        try:
            self._project_hours_per_day = int(value)
        except Exception:
            pass

    def get_project_hours_per_day(self):
        """Get project_hours_per_day."""
        return self._project_hours_per_day

    def set_project_work_days(self, value):
        """Set project_work_days."""
        if type(value) is list:
            self._project_work_days = value

    def get_project_work_days(self):
        """Get project_work_days."""
        return self._project_work_days

    def set_project_minimum_days(self, value):
        """Set project_minimum_days."""
        try:
            self._project_minimum_days = int(value)
        except Exception:
            pass

    def get_project_minimum_days(self):
        """Get project_minimum_days."""
        return self._project_minimum_days

    def set_project_wage(self, value):
        """Set project_wage."""
        try:
            self._project_wage = Decimal(str(value))
        except Exception:
            pass

    def get_project_wage(self):
        """Get project_wage."""
        return self._project_wage

    def set_baseentry_amount(self, value):
        """Set baseentry_amount."""
        self._baseentry_amount.set(value)

    def get_baseentry_amount(self):
        """Get baseentry_amount."""
        return self._baseentry_amount

    def set_baseentry_amount_b(self, value):
        """Set baseentry_amount_b."""
        self._baseentry_amount_b.set(value)

    def get_baseentry_amount_b(self):
        """Get baseentry_amount_b."""
        return self._baseentry_amount_b

    def set_baseentry_time(self, value):
        """Set baseentry_time."""
        self._baseentry_time.set(value)

    def get_baseentry_time(self):
        """Get baseentry_time."""
        self._baseentry_time.type('time')
        return self._baseentry_time

    def set_baseentry_price(self, value):
        """Set baseentry_price."""
        try:
            self._baseentry_price = Decimal(str(value))
        except Exception:
            pass

    def get_baseentry_price(self):
        """Get baseentry_price."""
        return self._baseentry_price

    def set_multiplyentry_amount(self, value):
        """Set multiplyentry_amount."""
        self._multiplyentry_amount.set(value)

    def get_multiplyentry_amount(self):
        """Get multiplyentry_amount."""
        return self._multiplyentry_amount

    def set_multiplyentry_amount_b(self, value):
        """Set multiplyentry_amount_b."""
        self._multiplyentry_amount_b.set(value)

    def get_multiplyentry_amount_b(self):
        """Get multiplyentry_amount_b."""
        return self._multiplyentry_amount_b

    def set_multiplyentry_hour_rate(self, value):
        """Set multiplyentry_hour_rate."""
        self._multiplyentry_hour_rate.set(value)

    def get_multiplyentry_hour_rate(self):
        """Get multiplyentry_hour_rate."""
        self._multiplyentry_hour_rate.type('time')
        return self._multiplyentry_hour_rate

    def set_connectentry_amount(self, value):
        """Set connectentry_amount."""
        self._connectentry_amount.set(value)

    def get_connectentry_amount(self):
        """Get connectentry_amount."""
        return self._connectentry_amount

    def set_connectentry_amount_b(self, value):
        """Set connectentry_amount_b."""
        self._connectentry_amount_b.set(value)

    def get_connectentry_amount_b(self):
        """Get connectentry_amount_b."""
        return self._connectentry_amount_b

    def set_connectentry_is_time(self, value):
        """Set connectentry_is_time."""
        self._connectentry_is_time = bool(value)

    def get_connectentry_is_time(self):
        """Get connectentry_is_time."""
        return self._connectentry_is_time

    def set_connectentry_multiplicator(self, value):
        """Set connectentry_multiplicator."""
        try:
            self._connectentry_multiplicator = Decimal(str(value))
        except Exception:
            pass

    def get_connectentry_multiplicator(self):
        """Get connectentry_multiplicator."""
        return self._connectentry_multiplicator

    def to_json(self, indent=2):
        """Convert settings data to json format."""
        out = {}

        # fetch all setting variables
        out['language'] = self.language

        out['offer_title'] = self.offer_title
        out['offer_comment'] = self.offer_comment
        out['offer_comment_b'] = self.offer_comment_b
        out['offer_filename'] = self.offer_filename
        out['offer_round_price'] = self._offer_round_price
        out['offer_templates'] = self._offer_templates

        out['invoice_title'] = self.invoice_title
        out['invoice_id'] = self.invoice_id
        out['invoice_comment'] = self.invoice_comment
        out['invoice_comment_b'] = self.invoice_comment_b
        out['invoice_filename'] = self.invoice_filename
        out['invoice_round_price'] = self._invoice_round_price
        out['invoice_templates'] = self._invoice_templates
        out['invoice_due_days'] = self._invoice_due_days
        out['invoice_delivery'] = self.invoice_delivery

        out['date_fmt'] = self.date_fmt
        out['commodity'] = self.commodity

        out['client_id'] = self.client_id
        out['client_company'] = self.client_company
        out['client_company_b'] = self.client_company_b
        out['client_attention'] = self.client_attention
        out['client_salutation'] = self.client_salutation
        out['client_name'] = self.client_name
        out['client_family_name'] = self.client_family_name
        out['client_street'] = self.client_street
        out['client_post_code'] = self.client_post_code
        out['client_city'] = self.client_city
        out['client_country'] = self.client_country
        out['client_tax_id'] = self.client_tax_id
        out['client_language'] = self.client_language

        out['project_title'] = self.project_title
        out['project_hours_per_day'] = self._project_hours_per_day
        out['project_work_days'] = self._project_work_days
        out['project_minimum_days'] = self._project_minimum_days
        out['project_wage'] = float(self._project_wage)

        out['baseentry_title'] = self.baseentry_title
        out['baseentry_comment'] = self.baseentry_comment
        out['baseentry_amount'] = str(self._baseentry_amount)
        out['baseentry_amount_format'] = self.baseentry_amount_format
        out['baseentry_amount_b'] = str(self._baseentry_amount_b)
        out['baseentry_amount_b_format'] = self.baseentry_amount_b_format
        out['baseentry_time'] = str(self._baseentry_time)
        out['baseentry_price'] = float(self._baseentry_price)

        out['multiplyentry_title'] = self.multiplyentry_title
        out['multiplyentry_comment'] = self.multiplyentry_comment
        out['multiplyentry_amount'] = str(self._multiplyentry_amount)
        out['multiplyentry_amount_format'] = self.multiplyentry_amount_format
        out['multiplyentry_amount_b'] = str(self._multiplyentry_amount_b)
        out['multiplyentry_amount_b_format'] = self.multiplyentry_amount_b_format
        out['multiplyentry_hour_rate'] = str(self._multiplyentry_hour_rate)

        out['connectentry_title'] = self.connectentry_title
        out['connectentry_comment'] = self.connectentry_comment
        out['connectentry_amount'] = str(self._connectentry_amount)
        out['connectentry_amount_format'] = self.connectentry_amount_format
        out['connectentry_amount_b'] = str(self._connectentry_amount_b)
        out['connectentry_amount_b_format'] = self.connectentry_amount_b_format
        out['connectentry_is_time'] = self._connectentry_is_time
        out['connectentry_multiplicator'] = float(self._connectentry_multiplicator)

        # return the json
        return json.dumps(out, indent=indent, sort_keys=True)

    def feed_json(self, js=None):
        """Feed settings variables from json string."""
        if js is None:
            return

        # get js as dict
        try:
            js = json.loads(js)
        except Exception:
            # do not load it
            return

        # feed settings variables
        if 'language' in js.keys():
            self.language = js['language']

        if 'offer_title' in js.keys():
            self.offer_title = js['offer_title']

        if 'offer_comment' in js.keys():
            self.offer_comment = js['offer_comment']

        if 'offer_comment_b' in js.keys():
            self.offer_comment_b = js['offer_comment_b']

        if 'offer_filename' in js.keys():
            self.offer_filename = js['offer_filename']

        if 'offer_round_price' in js.keys():
            self.set_offer_round_price(js['offer_round_price'])

        if 'offer_templates' in js.keys():
            self._offer_templates = js['offer_templates']

        if 'invoice_title' in js.keys():
            self.invoice_title = js['invoice_title']

        if 'invoice_id' in js.keys():
            self.invoice_id = js['invoice_id']

        if 'invoice_comment' in js.keys():
            self.invoice_comment = js['invoice_comment']

        if 'invoice_comment_b' in js.keys():
            self.invoice_comment_b = js['invoice_comment_b']

        if 'invoice_filename' in js.keys():
            self.invoice_filename = js['invoice_filename']

        if 'invoice_round_price' in js.keys():
            self.set_invoice_round_price(js['invoice_round_price'])

        if 'invoice_templates' in js.keys():
            self._invoice_templates = js['invoice_templates']

        if 'invoice_due_days' in js.keys():
            self.set_invoice_due_days(js['invoice_due_days'])

        if 'invoice_delivery' in js.keys():
            self.invoice_delivery = js['invoice_delivery']

        if 'date_fmt' in js.keys():
            self.date_fmt = js['date_fmt']

        if 'commodity' in js.keys():
            self.commodity = js['commodity']

        if 'client_id' in js.keys():
            self.client_id = js['client_id']

        if 'client_company' in js.keys():
            self.client_company = js['client_company']

        if 'client_company_b' in js.keys():
            self.client_company_b = js['client_company_b']

        if 'client_attention' in js.keys():
            self.client_attention = js['client_attention']

        if 'client_salutation' in js.keys():
            self.client_salutation = js['client_salutation']

        if 'client_name' in js.keys():
            self.client_name = js['client_name']

        if 'client_family_name' in js.keys():
            self.client_family_name = js['client_family_name']

        if 'client_street' in js.keys():
            self.client_street = js['client_street']

        if 'client_post_code' in js.keys():
            self.client_post_code = js['client_post_code']

        if 'client_city' in js.keys():
            self.client_city = js['client_city']

        if 'client_country' in js.keys():
            self.client_country = js['client_country']

        if 'client_tax_id' in js.keys():
            self.client_tax_id = js['client_tax_id']

        if 'client_language' in js.keys():
            self.client_language = js['client_language']

        if 'project_title' in js.keys():
            self.project_title = js['project_title']

        if 'project_hours_per_day' in js.keys():
            self.set_project_hours_per_day(js['project_hours_per_day'])

        if 'project_work_days' in js.keys():
            self.set_project_work_days(js['project_work_days'])

        if 'project_minimum_days' in js.keys():
            self.set_project_minimum_days(js['project_minimum_days'])

        if 'project_wage' in js.keys():
            self.set_project_wage(js['project_wage'])

        if 'baseentry_title' in js.keys():
            self.baseentry_title = js['baseentry_title']

        if 'baseentry_comment' in js.keys():
            self.baseentry_comment = js['baseentry_comment']

        if 'baseentry_amount' in js.keys():
            self.set_baseentry_amount(js['baseentry_amount'])

        if 'baseentry_amount_format' in js.keys():
            self.baseentry_amount_format = js['baseentry_amount_format']

        if 'baseentry_amount_b' in js.keys():
            self.set_baseentry_amount_b(js['baseentry_amount_b'])

        if 'baseentry_amount_b_format' in js.keys():
            self.baseentry_amount_b_format = js['baseentry_amount_b_format']

        if 'baseentry_time' in js.keys():
            self.set_baseentry_time(js['baseentry_time'])

        if 'baseentry_price' in js.keys():
            self.set_baseentry_price(js['baseentry_price'])

        if 'multiplyentry_title' in js.keys():
            self.multiplyentry_title = js['multiplyentry_title']

        if 'multiplyentry_comment' in js.keys():
            self.multiplyentry_comment = js['multiplyentry_comment']

        if 'multiplyentry_amount' in js.keys():
            self.set_multiplyentry_amount(js['multiplyentry_amount'])

        if 'multiplyentry_amount_format' in js.keys():
            self.multiplyentry_amount_format = js['multiplyentry_amount_format']

        if 'multiplyentry_amount_b' in js.keys():
            self.set_multiplyentry_amount_b(js['multiplyentry_amount_b'])

        if 'multiplyentry_amount_b_format' in js.keys():
            self.multiplyentry_amount_b_format = js['multiplyentry_amount_b_format']

        if 'multiplyentry_hour_rate' in js.keys():
            self.set_multiplyentry_hour_rate(js['multiplyentry_hour_rate'])

        if 'connectentry_title' in js.keys():
            self.connectentry_title = js['connectentry_title']

        if 'connectentry_comment' in js.keys():
            self.connectentry_comment = js['connectentry_comment']

        if 'connectentry_amount' in js.keys():
            self.set_connectentry_amount(js['connectentry_amount'])

        if 'connectentry_amount_format' in js.keys():
            self.connectentry_amount_format = js['connectentry_amount_format']

        if 'connectentry_amount_b' in js.keys():
            self.set_connectentry_amount_b(js['connectentry_amount_b'])

        if 'connectentry_amount_b_format' in js.keys():
            self.connectentry_amount_b_format = js['connectentry_amount_b_format']

        if 'connectentry_is_time' in js.keys():
            self.set_connectentry_is_time(js['connectentry_is_time'])

        if 'connectentry_multiplicator' in js.keys():
            self.set_connectentry_multiplicator(js['connectentry_multiplicator'])

    def gen_abs_path_to_default_file(self, data_path, lang=None):
        """Generate the absolut path to the settings file."""
        lang_set = type(lang) is str
        if not lang_set:
            return data_path + '/defaults_' + self.language + '.settings'
        else:
            return data_path + '/defaults_' + lang + '.settings'

    def delete_default_file(self, data_path, lang=None):
        """Delete the default file in data_path."""
        if os.path.isfile(self.gen_abs_path_to_default_file(data_path, lang)):
            os.remove(self.gen_abs_path_to_default_file(data_path, lang))

    def save_defaults_to_file(self, data_path):
        """Save the default to file in data_path."""
        f = open(self.gen_abs_path_to_default_file(data_path), 'w')
        f.write(self.to_json())
        f.close()

    def load_settings_from_file(self, data_path):
        """Load the settings from file in data_path."""
        # check if the file exists
        if os.path.isfile(self.gen_abs_path_to_default_file(data_path)):
            # load content from file
            f = open(self.gen_abs_path_to_default_file(data_path), 'r')
            loaded = f.read().strip()
            f.close()

            # and feed own variables with it
            self.feed_json(loaded)

    def copy(self):
        """Return copy of own object."""
        return Default(
            language=self.language,
            offer_title=self.offer_title,
            offer_comment=self.offer_comment,
            offer_comment_b=self.offer_comment_b,
            offer_filename=self.offer_filename,
            offer_round_price=self._offer_round_price,
            offer_templates=self._offer_templates,
            invoice_title=self.invoice_title,
            invoice_id=self.invoice_id,
            invoice_comment=self.invoice_comment,
            invoice_comment_b=self.invoice_comment_b,
            invoice_filename=self.invoice_filename,
            invoice_round_price=self._invoice_round_price,
            invoice_templates=self._invoice_templates,
            invoice_due_days=self._invoice_due_days,
            invoice_delivery=self.invoice_delivery,
            date_fmt=self.date_fmt,
            commodity=self.commodity,
            client_id=self.client_id,
            client_company=self.client_company,
            client_company_b=self.client_company_b,
            client_attention=self.client_attention,
            client_salutation=self.client_salutation,
            client_name=self.client_name,
            client_family_name=self.client_family_name,
            client_street=self.client_street,
            client_post_code=self.client_post_code,
            client_city=self.client_city,
            client_country=self.client_country,
            client_tax_id=self.client_tax_id,
            client_language=self.client_language,
            project_title=self.project_title,
            project_hours_per_day=self._project_hours_per_day,
            project_work_days=self._project_work_days,
            project_minimum_days=self._project_minimum_days,
            project_wage=self._project_wage,
            baseentry_title=self.baseentry_title,
            baseentry_comment=self.baseentry_comment,
            baseentry_amount=self._baseentry_amount,
            baseentry_amount_format=self.baseentry_amount_format,
            baseentry_amount_b=self._baseentry_amount_b,
            baseentry_amount_b_format=self.baseentry_amount_b_format,
            baseentry_time=self._baseentry_time,
            baseentry_price=self._baseentry_price,
            multiplyentry_title=self.multiplyentry_title,
            multiplyentry_comment=self.multiplyentry_comment,
            multiplyentry_amount=self._multiplyentry_amount,
            multiplyentry_amount_format=self.multiplyentry_amount_format,
            multiplyentry_amount_b=self._multiplyentry_amount_b,
            multiplyentry_amount_b_format=self.multiplyentry_amount_b_format,
            multiplyentry_hour_rate=self._multiplyentry_hour_rate,
            connectentry_title=self.connectentry_title,
            connectentry_comment=self.connectentry_comment,
            connectentry_amount=self._connectentry_amount,
            connectentry_amount_format=self.connectentry_amount_format,
            connectentry_amount_b=self._connectentry_amount_b,
            connectentry_amount_b_format=self.connectentry_amount_b_format,
            connectentry_is_time=self._connectentry_is_time,
            connectentry_multiplicator=self._connectentry_multiplicator
        )
