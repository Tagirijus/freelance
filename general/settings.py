"""
The class holding all the settings (language, paths, etc.).

This class is also for saving and loading objects. In this class
I did not set up setters and getters like in the other classes.
There are too much and I did not know how to make it properly.
"""

import json
import os


class Settings(object):
    """Settings class."""

    def __init__(
        self,
        data_path=None,
        offer_template_en=None,
        offer_template_de=None,
        offer_filename=None,
        date_fmt=None,
        commodity=None,
        client_client_id=None,
        client_company=None,
        client_salutation=None,
        client_name=None,
        client_family_name=None,
        client_street=None,
        client_post_code=None,
        client_city=None,
        client_tax_id=None,
        client_language=None,
        project_client_id=None,
        project_title=None,
        project_hours_per_day=None,
        project_work_days=None,
        project_minimum_days=None,
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
        self.BASE_PATH = os.path.dirname(os.path.realpath(__file__))[
            :os.path.dirname(os.path.realpath(__file__)).rfind('/')
        ]

        # settings and programm
        self.data_path = (os.path.expanduser('~') + '/.tagirijus_freelance'
                          if data_path is None else data_path)
        self.offer_template_en = '' if offer_template_en is None else offer_template_en
        self.offer_template_de = '' if offer_template_de is None else offer_template_de
        self.offer_filename = '' if offer_filename is None else offer_filename
        self.date_fmt = '' if date_fmt is None else date_fmt
        self.commodity = '' if commodity is None else commodity

        # client default values
        self.client_client_id = '' if client_client_id is None else client_client_id
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
        self.project_client_id = '' if project_client_id is None else project_client_id
        self.project_title = '' if project_title is None else project_title
        self.project_hours_per_day = (0 if project_hours_per_day is None else
                                      project_hours_per_day)
        self.project_work_days = ([0, 1, 2, 3, 4] if project_work_days is None else
                                  project_work_days)
        self.project_minimum_days = (2 if project_minimum_days is None else
                                     project_minimum_days)

        # baseentry default values
        self.baseentry_title = '' if baseentry_title is None else baseentry_title
        self.baseentry_comment = '' if baseentry_comment is None else baseentry_comment
        self.baseentry_amount = 0.0 if baseentry_amount is None else baseentry_amount
        self.baseentry_amount_format = ('' if baseentry_amount_format is None
                                        else baseentry_amount_format)
        self.baseentry_time = 0.0 if baseentry_time is None else baseentry_time
        self.baseentry_price = 0.0 if baseentry_price is None else baseentry_price

        # multiplyentry default values
        self.multiplyentry_title = ('' if multiplyentry_title is None else
                                    multiplyentry_title)
        self.multiplyentry_comment = ('' if multiplyentry_comment is None else
                                      multiplyentry_comment)
        self.multiplyentry_amount = (0.0 if multiplyentry_amount is None else
                                     multiplyentry_amount)
        self.multiplyentry_amount_format = ('' if multiplyentry_amount_format is None
                                            else multiplyentry_amount_format)
        self.multiplyentry_hour_rate = (0.0 if multiplyentry_hour_rate is None else
                                        multiplyentry_hour_rate)

        # connectentry default values
        self.connectentry_title = ('' if connectentry_title is None else
                                   connectentry_title)
        self.connectentry_comment = ('' if connectentry_comment is None else
                                     connectentry_comment)
        self.connectentry_amount = (0.0 if connectentry_amount is None else
                                    connectentry_amount)
        self.connectentry_amount_format = ('' if connectentry_amount_format is None else
                                           connectentry_amount_format)
        self.connectentry_is_time = (True if connectentry_is_time is None else
                                     connectentry_is_time)
        self.connectentry_multiplicator = (0.0 if connectentry_multiplicator is None else
                                           connectentry_multiplicator)

        # generate freelance dir under ~/.tagirijus_freelance, if it does not exist
        self.generate_data_path()

        # try to load settings from self.data_path/freelance.settings afterwards
        self.load_settings_from_file()

    def to_json(self, indent=2):
        """Convert settings data to json format."""
        out = {}

        # fetch all setting variables
        out['data_path'] = self.data_path
        out['offer_template_en'] = self.offer_template_en
        out['offer_template_de'] = self.offer_template_de
        out['offer_filename'] = self.offer_filename
        out['date_fmt'] = self.date_fmt
        out['commodity'] = self.commodity

        out['client_client_id'] = self.client_client_id
        out['client_company'] = self.client_company
        out['client_salutation'] = self.client_salutation
        out['client_name'] = self.client_name
        out['client_family_name'] = self.client_family_name
        out['client_street'] = self.client_street
        out['client_post_code'] = self.client_post_code
        out['client_city'] = self.client_city
        out['client_tax_id'] = self.client_tax_id
        out['client_language'] = self.client_language

        out['project_client_id'] = self.project_client_id
        out['project_title'] = self.project_title
        out['project_hours_per_day'] = self.project_hours_per_day
        out['project_work_days'] = self.project_work_days
        out['project_minimum_days'] = self.project_minimum_days

        out['baseentry_title'] = self.baseentry_title
        out['baseentry_comment'] = self.baseentry_comment
        out['baseentry_amount'] = self.baseentry_amount
        out['baseentry_amount_format'] = self.baseentry_amount_format
        out['baseentry_time'] = self.baseentry_time
        out['baseentry_price'] = self.baseentry_price

        out['multiplyentry_title'] = self.multiplyentry_title
        out['multiplyentry_comment'] = self.multiplyentry_comment
        out['multiplyentry_amount'] = self.multiplyentry_amount
        out['multiplyentry_amount_format'] = self.multiplyentry_amount_format
        out['multiplyentry_hour_rate'] = self.multiplyentry_hour_rate

        out['connectentry_title'] = self.connectentry_title
        out['connectentry_comment'] = self.connectentry_comment
        out['connectentry_amount'] = self.connectentry_amount
        out['connectentry_amount_format'] = self.connectentry_amount_format
        out['connectentry_is_time'] = self.connectentry_is_time
        out['connectentry_multiplicator'] = self.connectentry_multiplicator

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
        if 'data_path' in js.keys():
            self.data_path = js['data_path']

        if 'offer_template_en' in js.keys():
            self.offer_template_en = js['offer_template_en']

        if 'offer_template_de' in js.keys():
            self.offer_template_de = js['offer_template_de']

        if 'offer_filename' in js.keys():
            self.offer_filename = js['offer_filename']

        if 'date_fmt' in js.keys():
            self.date_fmt = js['date_fmt']

        if 'commodity' in js.keys():
            self.commodity = js['commodity']

        if 'client_client_id' in js.keys():
            self.client_client_id = js['client_client_id']

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

        if 'project_client_id' in js.keys():
            self.project_client_id = js['project_client_id']

        if 'project_title' in js.keys():
            self.project_title = js['project_title']

        if 'project_hours_per_day' in js.keys():
            self.project_hours_per_day = js['project_hours_per_day']

        if 'project_work_days' in js.keys():
            self.project_project_work_days = js['project_work_days']

        if 'project_minimum_days' in js.keys():
            self.project_minimum_days = js['project_minimum_days']

        if 'baseentry_title' in js.keys():
            self.baseentry_title = js['baseentry_title']

        if 'baseentry_comment' in js.keys():
            self.baseentry_comment = js['baseentry_comment']

        if 'baseentry_amount' in js.keys():
            self.baseentry_amount = js['baseentry_amount']

        if 'baseentry_amount_format' in js.keys():
            self.baseentry_amount_format = js['baseentry_amount_format']

        if 'baseentry_time' in js.keys():
            self.baseentry_time = js['baseentry_time']

        if 'baseentry_price' in js.keys():
            self.baseentry_price = js['baseentry_price']

        if 'multiplyentry_title' in js.keys():
            self.multiplyentry_title = js['multiplyentry_title']

        if 'multiplyentry_comment' in js.keys():
            self.multiplyentry_comment = js['multiplyentry_comment']

        if 'multiplyentry_amount' in js.keys():
            self.multiplyentry_amount = js['multiplyentry_amount']

        if 'multiplyentry_amount_format' in js.keys():
            self.multiplyentry_amount_format = js['multiplyentry_amount_format']

        if 'multiplyentry_hour_rate' in js.keys():
            self.multiplyentry_hour_rate = js['multiplyentry_hour_rate']

        if 'connectentry_title' in js.keys():
            self.connectentry_title = js['connectentry_title']

        if 'connectentry_comment' in js.keys():
            self.connectentry_comment = js['connectentry_comment']

        if 'connectentry_amount' in js.keys():
            self.connectentry_amount = js['connectentry_amount']

        if 'connectentry_amount_format' in js.keys():
            self.connectentry_amount_format = js['connectentry_amount_format']

        if 'connectentry_is_time' in js.keys():
            self.connectentry_is_time = js['connectentry_is_time']

        if 'connectentry_multiplicator' in js.keys():
            self.connectentry_multiplicator = js['connectentry_multiplicator']

    def gen_abs_path_to_settings_file(self):
        """Generate the absolut path to the settings file."""
        return self.data_path + '/freelance.settings'

    def generate_data_path(self):
        """Check if data_path exists or create dir."""
        # does it exist?
        if os.path.isdir(self.data_path):
            # yep! go on
            return
        else:
            # nope? create it!
            os.mkdir(self.data_path)

    def save_settings_to_file(self):
        """Save the settings to file in data_path."""
        f = open(self.gen_abs_path_to_settings_file(), 'w')
        f.write(self.to_json())
        f.close()

    def load_settings_from_file(self):
        """Load the settings from file in data_path."""
        # check if the file exists
        if os.path.isfile(self.gen_abs_path_to_settings_file()):
            # load content from file
            f = open(self.gen_abs_path_to_settings_file(), 'r')
            loaded = f.read().strip()
            f.close()

            # and feed own variables with it
            self.feed_json(loaded)
