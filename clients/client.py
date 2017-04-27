"""The class holding informatin about the client."""

import json


class Client(object):
    """This class holds the detailed client information."""

    def __init__(
        self,
        client_id='',
        company='',
        salutation='',
        name='',
        family_name='',
        street='',
        post_code='',
        city='',
        tax_id='',
        language=''
    ):
        """Initialize the class."""
        self.client_id = str(client_id)
        self.company = str(company)
        self.salutation = str(salutation)
        self.name = str(name)
        self.family_name = str(family_name)
        self.street = str(street)
        self.post_code = str(post_code)
        self.city = str(city)
        self.tax_id = str(tax_id)
        self.language = str(language)

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

        if 'company' in js.keys():
            company = js['company']

        if 'salutation' in js.keys():
            salutation = js['salutation']

        if 'name' in js.keys():
            name = js['name']

        if 'family_name' in js.keys():
            family_name = js['family_name']

        if 'street' in js.keys():
            street = js['street']

        if 'post_code' in js.keys():
            post_code = js['post_code']

        if 'city' in js.keys():
            city = js['city']

        if 'tax_id' in js.keys():
            tax_id = js['tax_id']

        if 'language' in js.keys():
            language = js['language']

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
