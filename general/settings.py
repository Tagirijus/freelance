"""The class holding all the settings (language, paths, etc.)."""

from general.default import Default
import json
import os


class Settings(object):
    """Settings class."""

    def __init__(
        self,
        data_path=None,
        inactive_dir=None,
        languages=None,
        def_language=None,
        defaults=None,
        offer_count_offset=None,
        invoice_count_offset=None,
        ledgeradd_command=None,
        ledgeradd_receiving_account=None,
        ledgeradd_tax_account=None,
        ledgeradd_def_payee=None,
        ledger_alias_file=None,
        ledger_alias_default_account=None,
        ledger_time_command=None
    ):
        """Initialize the class and hard code defaults, if no file is given."""
        self.BASE_PATH = os.path.dirname(os.path.realpath(__file__))[
            :os.path.dirname(os.path.realpath(__file__)).rfind('/')
        ]

        # check if data_path.flsettings exist in the base path of the script
        if os.path.isfile(self.BASE_PATH + '/data_path.flsettings'):
            f = open(self.BASE_PATH + '/data_path.flsettings', 'r')
            data_path = f.read().strip()
            f.close()

        # settings and programm
        self.data_path = (os.path.expanduser('~') + '/.tagirijus_freelance'
                          if data_path is None else data_path)

        # generate freelance dir under ~/.tagirijus_freelance, if it does not exist
        self.generate_data_path()

        self.inactive_dir = '/inactive' if inactive_dir is None else inactive_dir
        self._languages = ['en']                # set default
        self.set_languages(languages)           # try to set arguments value
        self._def_language = 'en'               # set default
        self.set_def_language(def_language)     # try to set arguments value
        self._offer_count_offset = 0            # set default
        self.set_offer_count_offset(offer_count_offset)  # try to set arguments value
        self._invoice_count_offset = 0            # set default
        self.set_invoice_count_offset(invoice_count_offset)  # try to set arguments value

        # ledgeradd integration
        self.ledgeradd_command = (
            '' if ledgeradd_command is None else str(ledgeradd_command)
        )
        self.ledgeradd_receiving_account = (
            'account' if ledgeradd_receiving_account is None else str(
                ledgeradd_receiving_account
            )
        )
        self.ledgeradd_tax_account = (
            'tax' if ledgeradd_tax_account is None else str(
                ledgeradd_tax_account
            )
        )
        self.ledgeradd_def_payee = (
            '' if ledgeradd_def_payee is None else str(
                ledgeradd_def_payee
            )
        )

        # ledger stuff
        self.ledger_alias_file = (
            self.data_path + '/LEDGER_ALIAS_FILE.journal'
            if ledger_alias_file is None
            else str(ledger_alias_file)
        )
        self.ledger_alias_default_account = (
            'Income:{CLIENT_FULLNAME}'
            if ledger_alias_default_account is None
            else str(ledger_alias_default_account)
        )

        # ledger time
        self.ledger_time_command = (
            'ledger -f [YOUR_TIME_JOURNAL] --depth=4' if ledger_time_command is None
            else str(ledger_time_command)
        )

        # try to load settings from self.data_path/freelance.settings afterwards
        self.load_settings_from_file()

        # get the defaults from the file(s)
        self.defaults = {}
        for lang in self._languages:
            self.defaults[lang] = Default(
                data_path=self.data_path,
                language=str(lang)
            )

    def set_languages(self, value):
        """Set languages."""
        if type(value) is list:
            self._languages = value

    def get_languages(self):
        """Get languages."""
        return self._languages

    def set_def_language(self, value=None):
        """Set default language if it exists in the self._languages."""
        if value is not None:
            if str(value) in self._languages:
                self._def_language = str(value)
                return True
            else:
                self._def_language = 'en'
                return False
        return False

    def get_def_language(self):
        """Get default language."""
        return self._def_language

    def set_offer_count_offset(self, value):
        """Set offer_count_offset."""
        try:
            self._offer_count_offset = int(value)
        except Exception:
            pass

    def get_offer_count_offset(self):
        """Get offer_count_offset."""
        return self._offer_count_offset

    def set_invoice_count_offset(self, value):
        """Set invoice_count_offset."""
        try:
            self._invoice_count_offset = int(value)
        except Exception:
            pass

    def get_invoice_count_offset(self):
        """Get invoice_count_offset."""
        return self._invoice_count_offset

    def remove_default(self, language=None, client_list=None):
        """Remove the default."""
        one_not_set = language is None or client_list is None
        lang_exists = language in self.defaults.keys() and language in self._languages

        # cancel if one argument is not set or language does not exist
        if one_not_set or not lang_exists:
            return False

        # remove the language from clients, which have it
        for client in client_list:
            # if the client has this language ...
            if client.language == language:
                # ... set it to the default language
                client.language = 'en'

        # remove it from self._languages
        self._languages.pop(self._languages.index(str(language)))

        # delete the file
        self.defaults[language].delete_default_file(self.data_path)

        # remove the self.defaults dict entry
        del self.defaults[language]
        return True

    def rename_default(self, old_lang=None, new_lang=None, client_list=None):
        """Try to rename the selected old_lang."""
        one_not_set = old_lang is None or new_lang is None or client_list is None
        old_exists = old_lang in self.defaults.keys() and old_lang in self._languages
        new_exists = new_lang in self.defaults.keys()
        new_is_empty = new_lang == ''

        # cancel if one argument is not set, the old_lang does not exist
        # or the new name already exists, or new name is empty
        if one_not_set or not old_exists or new_exists or new_is_empty:
            return False

        # cycle through the clients and change their language as well
        for client in client_list:
            if client.language == old_lang:
                client.language = new_lang

        # create new default with new name
        self.defaults[new_lang] = self.defaults[old_lang].copy()
        self.defaults[new_lang].language = new_lang
        self._languages.append(new_lang)

        # delete old default: its file, its dict entry and from self._languages
        self.defaults[old_lang].delete_default_file(self.data_path, old_lang)
        del self.defaults[old_lang]
        self._languages.pop(self._languages.index(old_lang))

        return True

    def new_default(self, language=None):
        """Make a new default."""
        lang_exists = language in self.defaults.keys() and language in self._languages

        if not lang_exists:
            # appaned language to self._languages
            self._languages.append(str(language))

            # append language to defaults dict
            self.defaults[language] = Default(
                data_path=self.data_path,
                language=language
            )
            return True
        else:
            return False

    def to_json(self, indent=2, ensure_ascii=False):
        """Convert settings data to json format."""
        out = {}

        # fetch all setting variables
        out['data_path'] = self.data_path
        out['inactive_dir'] = self.inactive_dir
        out['languages'] = self._languages
        out['def_language'] = self._def_language
        out['offer_count_offset'] = self._offer_count_offset
        out['invoice_count_offset'] = self._invoice_count_offset
        out['ledgeradd_command'] = self.ledgeradd_command
        out['ledgeradd_receiving_account'] = self.ledgeradd_receiving_account
        out['ledgeradd_tax_account'] = self.ledgeradd_tax_account
        out['ledgeradd_def_payee'] = self.ledgeradd_def_payee
        out['ledger_alias_file'] = self.ledger_alias_file
        out['ledger_alias_default_account'] = self.ledger_alias_default_account
        out['ledger_time_command'] = self.ledger_time_command

        # return the json
        return json.dumps(
            out,
            indent=indent,
            ensure_ascii=ensure_ascii,
            sort_keys=True
        )

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

        if 'inactive_dir' in js.keys():
            self.inactive_dir = js['inactive_dir']

        if 'languages' in js.keys():
            self.set_languages(js['languages'])

        if 'def_language' in js.keys():
            self.set_def_language(js['def_language'])

        if 'offer_count_offset' in js.keys():
            self.set_offer_count_offset(js['offer_count_offset'])

        if 'invoice_count_offset' in js.keys():
            self.set_invoice_count_offset(js['invoice_count_offset'])

        if 'ledgeradd_command' in js.keys():
            self.ledgeradd_command = js['ledgeradd_command']

        if 'ledgeradd_receiving_account' in js.keys():
            self.ledgeradd_receiving_account = js['ledgeradd_receiving_account']

        if 'ledgeradd_tax_account' in js.keys():
            self.ledgeradd_tax_account = js['ledgeradd_tax_account']

        if 'ledgeradd_def_payee' in js.keys():
            self.ledgeradd_def_payee = js['ledgeradd_def_payee']

        if 'ledger_alias_file' in js.keys():
            self.ledger_alias_file = js['ledger_alias_file']

        if 'ledger_alias_default_account' in js.keys():
            self.ledger_alias_default_account = js['ledger_alias_default_account']

        if 'ledger_time_command' in js.keys():
            self.ledger_time_command = js['ledger_time_command']

    def gen_abs_path_to_settings_file(self):
        """Generate the absolut path to the settings file."""
        return self.data_path + '/freelance.settings'

    def generate_data_path(self):
        """Check if data_path exists or create dir."""
        is_dir = os.path.isdir(str(self.data_path))
        is_file = os.path.isfile(str(self.data_path))

        # raise error, if it is a file
        if is_file:
            raise IOError

        # create if it does not exist
        if not is_dir:
            os.mkdir(self.data_path)

    def save_settings_to_file(self):
        """Save the settings to file in data_path."""
        # generate data_path if it does not exist
        self.generate_data_path()

        # save the path to BASE_PATH/data_path.flsettings
        f = open(self.BASE_PATH + '/data_path.flsettings', 'w')
        f.write(self.data_path)
        f.close()

        # save settings to the data_path
        f = open(self.gen_abs_path_to_settings_file(), 'w')
        f.write(self.to_json())
        f.close()

        # save defaults
        try:
            for lang in self.defaults.keys():
                self.defaults[lang].save_defaults_to_file(self.data_path)
        except Exception as e:
            raise e

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
