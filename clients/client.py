"""
The class holding informatin about the client and the client_list.

The classes do not have privat values and setter and getter methods!
"""

from decimal import Decimal
import json


class Client(object):
    """This class holds the detailed client information."""

    def __init__(
        self,
        client_id=None,
        company=None,
        company_b=None,
        attention=None,
        salutation=None,
        name=None,
        family_name=None,
        street=None,
        post_code=None,
        city=None,
        country=None,
        tax_id=None,
        additional_a=None,
        additional_b=None,
        additional_c=None,
        language=None,
        def_wage=None,
        def_commodity=None
    ):
        """Initialize the class."""
        self.client_id = 'no_id' if client_id is None else str(client_id)
        self.company = '' if company is None else str(company)
        self.company_b = '' if company_b is None else str(company_b)
        self.attention = '' if attention is None else str(attention)
        self.salutation = '' if salutation is None else str(salutation)
        self.name = '' if name is None else str(name)
        self.family_name = '' if family_name is None else str(family_name)
        self.street = '' if street is None else str(street)
        self.post_code = '' if post_code is None else str(post_code)
        self.city = '' if city is None else str(city)
        self.country = '' if country is None else str(country)
        self.tax_id = '' if tax_id is None else str(tax_id)
        self.additional_a = '' if additional_a is None else str(additional_a)
        self.additional_b = '' if additional_b is None else str(additional_b)
        self.additional_c = '' if additional_c is None else str(additional_c)
        self.language = 'en' if language is None else str(language)
        self._def_wage = Decimal('0.00')            # set default
        self.set_def_wage(def_wage)                 # try to set arguments value
        self.def_commodity = '$' if def_commodity is None else str(def_commodity)

    def set_def_wage(self, value):
        """Set def_wage."""
        try:
            # only works if value is convertable to Decimal
            self._def_wage = Decimal(str(value))
        except Exception:
            pass

    def get_def_wage(self):
        """Get def_wage."""
        return self._def_wage

    def fullname(self):
        """Return name + familyname."""
        name = self.name
        family_name = ' ' + self.family_name if self.family_name != '' else ''
        return name + family_name

    def to_dict(self):
        """Convert object to dict."""
        out = {}

        # fetch all variables
        out['type'] = self.__class__.__name__
        out['client_id'] = self.client_id
        out['company'] = self.company
        out['company_b'] = self.company_b
        out['attention'] = self.attention
        out['salutation'] = self.salutation
        out['name'] = self.name
        out['family_name'] = self.family_name
        out['street'] = self.street
        out['post_code'] = self.post_code
        out['city'] = self.city
        out['country'] = self.country
        out['tax_id'] = self.tax_id
        out['additional_a'] = self.additional_a
        out['additional_b'] = self.additional_b
        out['additional_c'] = self.additional_c
        out['language'] = self.language
        out['def_wage'] = str(self._def_wage)
        out['def_commodity'] = self.def_commodity

        return out

    def to_json(self, indent=2, ensure_ascii=False):
        """Convert variables data to json format."""
        return json.dumps(
            self.to_dict(),
            indent=indent,
            ensure_ascii=ensure_ascii,
            sort_keys=True
        )

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

        if 'company_b' in js.keys():
            company_b = js['company_b']
        else:
            company_b = None

        if 'attention' in js.keys():
            attention = js['attention']
        else:
            attention = None

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

        if 'country' in js.keys():
            country = js['country']
        else:
            country = None

        if 'tax_id' in js.keys():
            tax_id = js['tax_id']
        else:
            tax_id = None

        if 'additional_a' in js.keys():
            additional_a = js['additional_a']
        else:
            additional_a = None

        if 'additional_b' in js.keys():
            additional_b = js['additional_b']
        else:
            additional_b = None

        if 'additional_c' in js.keys():
            additional_c = js['additional_c']
        else:
            additional_c = None

        if 'language' in js.keys():
            language = js['language']
        else:
            language = None

        if 'def_wage' in js.keys():
            def_wage = js['def_wage']
        else:
            def_wage = None

        if 'def_commodity' in js.keys():
            def_commodity = js['def_commodity']
        else:
            def_commodity = None

        # return new object
        return cls(
            client_id=client_id,
            company=company,
            company_b=company_b,
            salutation=salutation,
            attention=attention,
            name=name,
            family_name=family_name,
            street=street,
            post_code=post_code,
            city=city,
            country=country,
            tax_id=tax_id,
            additional_a=additional_a,
            additional_b=additional_b,
            additional_c=additional_c,
            language=language,
            def_wage=def_wage,
            def_commodity=def_commodity
        )

    def copy(self):
        """Return copy of own object as new object."""
        return Client().from_json(js=self.to_json())
