"""
The class holding informatin about the client and the client_list.

The classes do not have privat values and setter and getter methods!
"""

import json


class Client(object):
    """This class holds the detailed client information."""

    def __init__(
        self,
        client_id=None,
        company=None,
        salutation=None,
        name=None,
        family_name=None,
        street=None,
        post_code=None,
        city=None,
        tax_id=None,
        language=None
    ):
        """Initialize the class."""
        self.client_id = 'no_id' if client_id is None else str(client_id)
        self.company = '' if company is None else str(company)
        self.salutation = '' if salutation is None else str(salutation)
        self.name = '' if name is None else str(name)
        self.family_name = '' if family_name is None else str(family_name)
        self.street = '' if street is None else str(street)
        self.post_code = '' if post_code is None else str(post_code)
        self.city = '' if city is None else str(city)
        self.tax_id = '' if tax_id is None else str(tax_id)
        self.language = '' if language is None else str(language)

    def fullname(self):
        """Return name + familyname."""
        name = self.name
        family_name = ' ' + self.family_name if self.family_name != '' else ''
        return name + family_name

    def to_json(self, indent=2):
        """Convert variables data to json format."""
        out = {}

        # fetch all variables
        out['type'] = self.__class__.__name__
        out['client_id'] = self.client_id
        out['company'] = self.company
        out['salutation'] = self.salutation
        out['name'] = self.name
        out['family_name'] = self.family_name
        out['street'] = self.street
        out['post_code'] = self.post_code
        out['city'] = self.city
        out['tax_id'] = self.tax_id
        out['language'] = self.language

        # return the json
        return json.dumps(out, indent=indent, sort_keys=True)

    @classmethod
    def from_json(cls, js=None):
        """Convert all data from json format."""
        if js is None:
            return cls()

        # get js as dict
        if type(js) is not dict:
            try:
                js = json.loads(js)
            except Exception:
                # return default object
                return cls()

        # create new entry object from json
        if 'client_id' in js.keys():
            client_id = js['client_id']
        else:
            client_id = None

        if 'company' in js.keys():
            company = js['company']
        else:
            company = None

        if 'salutation' in js.keys():
            salutation = js['salutation']
        else:
            salutation = None

        if 'name' in js.keys():
            name = js['name']
        else:
            name = None

        if 'family_name' in js.keys():
            family_name = js['family_name']
        else:
            family_name = None

        if 'street' in js.keys():
            street = js['street']
        else:
            street = None

        if 'post_code' in js.keys():
            post_code = js['post_code']
        else:
            post_code = None

        if 'city' in js.keys():
            city = js['city']
        else:
            city = None

        if 'tax_id' in js.keys():
            tax_id = js['tax_id']
        else:
            tax_id = None

        if 'language' in js.keys():
            language = js['language']
        else:
            language = None

        # return new object
        return cls(
            client_id=client_id,
            company=company,
            salutation=salutation,
            name=name,
            family_name=family_name,
            street=street,
            post_code=post_code,
            city=city,
            tax_id=tax_id,
            language=language
        )

    def copy(self):
        """Return copy of own object as new object."""
        return Client().from_json(js=self.to_json())
