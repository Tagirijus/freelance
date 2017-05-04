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
        def_language=None,
        languages=None,
        defaults=None,
        keep_offer_preset_date=None
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
        is_dir = os.path.isdir(str(self.data_path))
        is_file = os.path.isfile(str(self.data_path))
        if not is_dir or is_file:
            raise IOError
        self.inactive_dir = '/inactive' if inactive_dir is None else inactive_dir
        self.def_language = 'en' if def_language is None else str(def_language)
        self.set_def_language(def_language)
        self.languages = ['en'] if languages is None else languages

        # generate freelance dir under ~/.tagirijus_freelance, if it does not exist
        self.generate_data_path()

        # preset settings
        self.keep_offer_preset_date = (False if keep_offer_preset_date is None
                                       else bool(keep_offer_preset_date))

        # try to load settings from self.data_path/freelance.settings afterwards
        self.load_settings_from_file()

        # get the defaults from the file(s)
        self.defaults = {}
        for lang in self.languages:
            self.defaults[lang] = Default(
                data_path=self.data_path,
                language=str(lang)
            )

    def set_def_language(self, value=None):
        """Set default language if it exists in the self.languages."""
        if value is not None:
            if str(value) in self.languages:
                self._def_language = str(value)
                return True
            else:
                self._def_language = 'en'
                return False
        return False

    def remove_default(self, language=None):
        """Remove the default."""
        if type(language) is str:
            if (language in self.defaults.keys() and
                    language in self.languages):
                # remove it from self.languages
                self.languages.pop(self.languages.index(str(language)))

                # delete the file
                self.defaults[language].delete_default_file()

                # remove the self.defaults dict entry
                del self.defaults[language]

    def get_default(self, language=None):
        """Return Default object, if it exists."""
        if type(language) is str:
            if language in self.defaults.keys():
                # return the default langauge pack, if it exists
                return self.defaults[language]
            else:
                # otherwise return a default language en pack
                return Default(
                    data_path=self.data_path,
                    language='en'
                )

    def new_default(self, language=None):
        """Make a new default."""
        if type(language) is str:
            if (language not in self.defaults.keys() and
                    language not in self.languages):

                # appaned language to self.languages
                self.languages.append(str(language))

                # append language to defaults dict
                self.defaults[language] = Default(
                    data_path=self.data_path,
                    language=language
                )

    def to_json(self, indent=2, ensure_ascii=False):
        """Convert settings data to json format."""
        out = {}

        # fetch all setting variables
        out['data_path'] = self.data_path
        out['inactive_dir'] = self.inactive_dir
        out['def_language'] = self.def_language
        out['languages'] = self.languages
        out['keep_offer_preset_date'] = self.keep_offer_preset_date

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

        if 'def_language' in js.keys():
            self.def_language = js['def_language']

        if 'languages' in js.keys():
            self.languages = js['languages']

        if 'keep_offer_preset_date' in js.keys():
            self.keep_offer_preset_date = js['keep_offer_preset_date']

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
                self.defaults[lang].save_defaults_to_file(new_data_path=self.data_path)
        except Exception:
            pass

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
