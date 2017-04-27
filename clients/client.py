"""The class holding informatin about the client."""

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
        language=None,
        date_fmt=None
    ):
        """Initialize the class."""
        self.client_id = '' if client_id is None else str(client_id)
        self.company = '' if company is None else str(company)
        self.salutation = '' if salutation is None else str(salutation)
        self.name = '' if name is None else str(name)
        self.family_name = '' if family_name is None else str(family_name)
        self.street = '' if street is None else str(street)
        self.post_code = '' if post_code is None else str(post_code)
        self.city = '' if city is None else str(city)
        self.tax_id = '' if tax_id is None else str(tax_id)
        self.language = '' if language is None else str(language)
        self.date_fmt = '' if date_fmt is None else str(date_fmt)

    def get_projects(self, project_list):
        """Get list of projects for only that client."""
        out = []
        for project in project_list:
            try:
                if project.client_id == self.client_id:
                    out.append(project)
            except Exception:
                pass

        return out

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
        out['date_fmt'] = self.date_fmt

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

        if 'date_fmt' in js.keys():
            date_fmt = js['date_fmt']
        else:
            date_fmt = None

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
            language=language,
            date_fmt=date_fmt
        )
