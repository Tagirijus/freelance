"""The class holding all the default texts."""

from decimal import Decimal
import json
from offer import time as time_module
import os


class Default(object):
    """Settings class."""

    def __init__(
        self,
        data_path=None,
        language=None,
        offer_title=None,
        offer_template=None,
        offer_filename=None,
        date_fmt=None,
        commodity=None,
        client_company=None,
        client_salutation=None,
        client_name=None,
        client_family_name=None,
        client_street=None,
        client_post_code=None,
        client_city=None,
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
        baseentry_time=None,
        baseentry_price=None,
        multiplyentry_title=None,
        multiplyentry_comment=None,
        multiplyentry_amount=None,
        multiplyentry_amount_format=None,
        multiplyentry_hour_rate=None,
        connectentry_title=None,
        connectentry_comment=None,
        connectentry_amount=None,
        connectentry_amount_format=None,
        connectentry_is_time=None,
        connectentry_multiplicator=None
    ):
        """Initialize the class and hard code defaults, if no file is given."""
        self.language = 'SET_ME' if language is None else language
        self.offer_title = '' if offer_title is None else offer_title
        self.offer_template = '' if offer_template is None else offer_template
        self.offer_filename = '' if offer_filename is None else offer_filename
        self.date_fmt = '' if date_fmt is None else date_fmt
        self.commodity = '' if commodity is None else commodity

        # client default values
        self.client_company = '' if client_company is None else client_company
        self.client_salutation = '' if client_salutation is None else client_salutation
        self.client_name = '' if client_name is None else client_name
        self.client_family_name = '' if client_family_name is None else client_family_name
        self.client_street = '' if client_street is None else client_street

        self.client_post_code = '' if client_post_code is None else client_post_code
        self.client_city = '' if client_city is None else client_city
        self.client_tax_id = '' if client_tax_id is None else client_tax_id
        self.client_language = 'en' if client_language is None else client_language

        # project default values
        self.project_title = '' if project_title is None else project_title
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
        self._baseentry_amount = Decimal(0)
        self.set_baseentry_amount(baseentry_amount)
        self.baseentry_amount_format = ('' if baseentry_amount_format is None
                                        else baseentry_amount_format)
        self._baseentry_time = Decimal(0)
        self.set_baseentry_time(baseentry_time)
        self._baseentry_price = Decimal(0)
        self.set_baseentry_price(baseentry_price)

        # multiplyentry default values
        self.multiplyentry_title = ('' if multiplyentry_title is None else
                                    multiplyentry_title)
        self.multiplyentry_comment = ('' if multiplyentry_comment is None else
                                      multiplyentry_comment)
        self._multiplyentry_amount = Decimal(0)
        self.set_multiplyentry_amount(multiplyentry_amount)
        self.multiplyentry_amount_format = ('' if multiplyentry_amount_format is None
                                            else multiplyentry_amount_format)
        self._multiplyentry_hour_rate = Decimal(0)
        self.set_multiplyentry_hour_rate(multiplyentry_hour_rate)

        # connectentry default values
        self.connectentry_title = ('' if connectentry_title is None else
                                   connectentry_title)
        self.connectentry_comment = ('' if connectentry_comment is None else
                                     connectentry_comment)
        self._connectentry_amount = Decimal(0)
        self.set_connectentry_amount(connectentry_amount)
        self.connectentry_amount_format = ('' if connectentry_amount_format is None else
                                           connectentry_amount_format)
        self._connectentry_is_time = True
        self.set_connectentry_is_time(connectentry_is_time)
        self._connectentry_multiplicator = Decimal(0)
        self.set_connectentry_multiplicator(connectentry_multiplicator)

        # try to load default automatically
        if data_path is not None:
            self.load_settings_from_file(data_path)

    def set_project_hours_per_day(self, value):
        """Set set_project_hours_per_day."""
        try:
            self._set_project_hours_per_day = int(value)
        except Exception:
            pass

    def get_project_hours_per_day(self):
        """Get set_project_hours_per_day."""
        return self._project_hours_per_day

    def set_project_work_days(self, value):
        """Set set_project_work_days."""
        if type(value) is list:
            self._set_project_work_days = value

    def get_project_work_days(self):
        """Get set_project_work_days."""
        return self._project_work_days

    def set_project_minimum_days(self, value):
        """Set set_project_minimum_days."""
        try:
            self._set_project_minimum_days = int(value)
        except Exception:
            pass

    def get_project_minimum_days(self):
        """Get set_project_minimum_days."""
        return self._project_minimum_days

    def set_project_wage(self, value):
        """Set set_project_wage."""
        try:
            self._set_project_wage = Decimal(str(value))
        except Exception:
            pass

    def get_project_wage(self):
        """Get set_project_wage."""
        return self._project_wage

    def set_baseentry_amount(self, value):
        """Set set_baseentry_amount."""
        try:
            self._set_baseentry_amount = Decimal(str(value))
        except Exception:
            pass

    def get_baseentry_amount(self):
        """Get set_baseentry_amount."""
        return self._baseentry_amount

    def set_baseentry_time(self, value):
        """Set set_baseentry_time."""
        self._time = time_module.to_timedelta(value)

    def get_baseentry_time(self):
        """Get set_baseentry_time."""
        return self._baseentry_time

    def set_baseentry_price(self, value):
        """Set set_baseentry_price."""
        try:
            self._set_baseentry_price = Decimal(str(value))
        except Exception:
            pass

    def get_baseentry_price(self):
        """Get set_baseentry_price."""
        return self._baseentry_price

    def set_multiplyentry_amount(self, value):
        """Set set_multiplyentry_amount."""
        try:
            self._set_multiplyentry_amount = Decimal(str(value))
        except Exception:
            pass

    def get_multiplyentry_amount(self):
        """Get set_multiplyentry_amount."""
        return self._multiplyentry_amount

    def set_multiplyentry_hour_rate(self, value):
        """Set set_multiplyentry_hour_rate."""
        try:
            self._set_multiplyentry_hour_rate = Decimal(str(value))
        except Exception:
            pass

    def get_multiplyentry_hour_rate(self):
        """Get set_multiplyentry_hour_rate."""
        return self._multiplyentry_hour_rate

    def set_connectentry_amount(self, value):
        """Set set_connectentry_amount."""
        try:
            self._set_connectentry_amount = Decimal(str(value))
        except Exception:
            pass

    def get_connectentry_amount(self):
        """Get set_connectentry_amount."""
        return self._connectentry_amount

    def set_connectentry_is_time(self, value):
        """Set set_connectentry_is_time."""
        self._set_connectentry_is_time = bool(value)

    def get_connectentry_is_time(self):
        """Get set_connectentry_is_time."""
        return self._connectentry_is_time

    def set_connectentry_multiplicator(self, value):
        """Set set_connectentry_multiplicator."""
        try:
            self._set_connectentry_multiplicator = Decimal(str(value))
        except Exception:
            pass

    def get_connectentry_multiplicator(self):
        """Get set_connectentry_multiplicator."""
        return self._connectentry_multiplicator

    def to_json(self, indent=2):
        """Convert settings data to json format."""
        out = {}

        # fetch all setting variables
        out['language'] = self.language
        out['offer_title'] = self.offer_title
        out['offer_template'] = self.offer_template
        out['offer_filename'] = self.offer_filename
        out['date_fmt'] = self.date_fmt
        out['commodity'] = self.commodity

        out['client_company'] = self.client_company
        out['client_salutation'] = self.client_salutation
        out['client_name'] = self.client_name
        out['client_family_name'] = self.client_family_name
        out['client_street'] = self.client_street
        out['client_post_code'] = self.client_post_code
        out['client_city'] = self.client_city
        out['client_tax_id'] = self.client_tax_id
        out['client_language'] = self.client_language

        out['project_title'] = self.project_title
        out['project_hours_per_day'] = self._project_hours_per_day
        out['project_work_days'] = self._project_work_days
        out['project_minimum_days'] = self._project_minimum_days
        out['project_wage'] = float(self._project_wage)

        out['baseentry_title'] = self.baseentry_title
        out['baseentry_comment'] = self.baseentry_comment
        out['baseentry_amount'] = float(self._baseentry_amount)
        out['baseentry_amount_format'] = self.baseentry_amount_format
        out['baseentry_time'] = str(self._baseentry_time)
        out['baseentry_price'] = float(self._baseentry_price)

        out['multiplyentry_title'] = self.multiplyentry_title
        out['multiplyentry_comment'] = self.multiplyentry_comment
        out['multiplyentry_amount'] = float(self._multiplyentry_amount)
        out['multiplyentry_amount_format'] = self.multiplyentry_amount_format
        out['multiplyentry_hour_rate'] = float(self._multiplyentry_hour_rate)

        out['connectentry_title'] = self.connectentry_title
        out['connectentry_comment'] = self.connectentry_comment
        out['connectentry_amount'] = float(self._connectentry_amount)
        out['connectentry_amount_format'] = self.connectentry_amount_format
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

        if 'offer_template' in js.keys():
            self.offer_template = js['offer_template']

        if 'offer_filename' in js.keys():
            self.offer_filename = js['offer_filename']

        if 'date_fmt' in js.keys():
            self.date_fmt = js['date_fmt']

        if 'commodity' in js.keys():
            self.commodity = js['commodity']

        if 'client_company' in js.keys():
            self.client_company = js['client_company']

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
            offer_template=self.offer_template,
            offer_filename=self.offer_filename,
            date_fmt=self.date_fmt,
            commodity=self.commodity,
            client_company=self.client_company,
            client_salutation=self.client_salutation,
            client_name=self.client_name,
            client_family_name=self.client_family_name,
            client_street=self.client_street,
            client_post_code=self.client_post_code,
            client_city=self.client_city,
            client_tax_id=self.client_tax_id,
            client_language=self.client_language,
            project_title=self.project_title,
            project_hours_per_day=self.get_project_hours_per_day(),
            project_work_days=self.get_project_work_days(),
            project_minimum_days=self.get_project_minimum_days(),
            project_wage=self.get_project_wage(),
            baseentry_title=self.baseentry_title,
            baseentry_comment=self.baseentry_comment,
            baseentry_amount=self.get_baseentry_amount(),
            baseentry_amount_format=self.baseentry_amount_format,
            baseentry_time=self.baseentry_time,
            baseentry_price=self.get_baseentry_price(),
            multiplyentry_title=self.multiplyentry_title,
            multiplyentry_comment=self.multiplyentry_comment,
            multiplyentry_amount=self.get_multiplyentry_amount(),
            multiplyentry_amount_format=self.multiplyentry_amount_format,
            multiplyentry_hour_rate=self.get_multiplyentry_hour_rate(),
            connectentry_title=self.connectentry_title,
            connectentry_comment=self.connectentry_comment,
            connectentry_amount=self.get_connectentry_amount(),
            connectentry_amount_format=self.connectentry_amount_format,
            connectentry_is_time=self.get_connectentry_is_time(),
            connectentry_multiplicator=self.get_connectentry_multiplicator()
        )
