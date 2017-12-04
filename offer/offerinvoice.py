"""The class holds a list of entries."""

from datetime import date as ddate
from datetime import datetime
from datetime import timedelta
from decimal import Decimal
from general import check_objects
from general.replacer import replacer
import json
from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry
from offer.quantitytime import QuantityTime
import os


class OfferInvoice(object):
    """A class holding a list of entries."""

    def __init__(
        self,
        title=None,
        id=None,
        comment=None,
        comment_b=None,
        date_fmt=None,
        date=None,
        delivery=None,
        due_days=None,
        paid_date=None,
        wage=None,
        commodity=None,
        round_price=None,
        entry_list=None
    ):
        """Initialize the class."""
        self.title = '' if title is None else str(title)
        self.id = '' if id is None else str(id)
        self.comment = '' if comment is None else str(comment)
        self.comment_b = '' if comment_b is None else str(comment_b)
        self.date_fmt = '%d.%m.%Y' if date_fmt is None else str(date_fmt)
        self.set_date(date)
        self.delivery = '' if delivery is None else str(delivery)
        self._due_days = 14             # set default
        self.set_due_days(due_days)     # try to set value
        self.set_paid_date(paid_date)
        self.set_round_price(
            False if round_price is None else round_price
        )
        self._wage = Decimal(0)             # set default
        self.set_wage(wage)                 # try to set arguments value
        self.commodity = '$' if commodity is None else str(commodity)
        self._entry_list = []               # set default
        self.set_entry_list(entry_list)     # try to set arguments value

    def set_date(self, value):
        """Set date."""
        # value is date, set it
        if type(value) is ddate:
            self._date = value

        # value is empty string, set None
        elif value == '' or value is None:
            self._date = None

        # value is other string, try to fetch it to date object
        elif type(value) is str:
            try:
                self._date = datetime.strptime(value, '%Y-%m-%d').date()
            except Exception:
                self._date = None

        else:
            self._date = None

    def get_date(self):
        """Get date."""
        return self._date

    def set_due_days(self, value):
        """Set due_days."""
        try:
            self._due_days = int(value)
        except Exception:
            pass

    def get_due_days(self):
        """Get due_days."""
        return self._due_days

    def get_due_date(self):
        """Get due_date."""
        if self._date is not None:
            return self._date + timedelta(days=self._due_days)
        else:
            return ddate(1987, 10, 15)

    def set_paid_date(self, value):
        """Set paid_date."""
        # value is date, set it
        if type(value) is ddate:
            self._paid_date = value

        # value is empty string, set None
        elif value == '' or value is None:
            self._paid_date = None

        # value is other string, try to fetch it to date object
        elif type(value) is str:
            try:
                self._paid_date = datetime.strptime(value, '%Y-%m-%d').date()
            except Exception:
                self._paid_date = None

        else:
            self._paid_date = None

    def get_paid_date(self):
        """Get paid_date."""
        return self._paid_date

    def set_wage(self, value):
        """Set wage."""
        try:
            # only works if value is convertable to Decimal
            self._wage = Decimal(str(value))
        except Exception:
            pass

    def get_round_price(self):
        """Get round_price."""
        return self._round_price

    def set_round_price(self, value):
        """Set round_price."""
        self._round_price = bool(value)

    def get_wage(self, project=None):
        """Get wage."""
        # tr to get projects wage
        if check_objects.is_project(project):
            p_wage = project.get_wage()
        else:
            p_wage = Decimal(0)

        # return project wage, if own wage is 0, other wise return own wage
        if self._wage == 0:
            return p_wage
        else:
            return self._wage

    def set_entry_list(self, value):
        """Set entry_list."""
        if type(value) is list:
            self._entry_list = value

    def get_entry_list(self):
        """Get entry_list."""
        return self._entry_list

    def append(self, entry=None):
        """Add entry to the entry_list."""
        is_entry = (type(entry) is BaseEntry or type(entry) is MultiplyEntry or
                    type(entry) is ConnectEntry)

        if not is_entry:
            return

        self._entry_list.append(entry)

    def pop(self, index):
        """Pop entry with the given index from list."""
        try:
            self._entry_list.pop(index)
        except Exception:
            pass

    def to_dict(self):
        """Convert object to dict."""
        out = {}

        # fetch the variables
        out['type'] = self.__class__.__name__
        out['title'] = self.title
        out['id'] = self.id
        out['comment'] = self.comment
        out['comment_b'] = self.comment_b
        out['date_fmt'] = self.date_fmt

        try:
            out['date'] = self._date.strftime('%Y-%m-%d')
        except Exception:
            out['date'] = None

        out['delivery'] = self.delivery

        out['due_days'] = self._due_days

        try:
            out['paid_date'] = self._paid_date.strftime('%Y-%m-%d')
        except Exception:
            out['paid_date'] = None

        out['wage'] = float(self._wage)
        out['commodity'] = self.commodity
        out['round_price'] = self._round_price

        # fetch the jsons from the entries
        out['entry_list'] = []
        for entry in self._entry_list:
            try:
                out['entry_list'].append(entry.to_dict())
            except Exception:
                out['entry_list'].append(entry)

        return out

    def to_json(self, indent=2, ensure_ascii=False):
        """Convert variables data to json format."""
        return json.dumps(
            self.to_dict(),
            indent=indent,
            ensure_ascii=ensure_ascii,
            sort_keys=True
        )

    def load_entry_list_from_js(self, lis=None):
        """Convert list to entry object list."""
        entry_list = []
        # cycle through the list of dicts
        for entry in lis:
            # it should have a type key
            if 'type' in entry.keys():
                # entry is BaseEntry
                if entry['type'] == 'BaseEntry':
                    # convert this dict to an offer objetc then!
                    entry_list.append(BaseEntry().from_json(
                        js=entry
                    ))

                # entry is MultiplyEntry
                if entry['type'] == 'MultiplyEntry':
                    # convert this dict to an offer objetc then!
                    entry_list.append(MultiplyEntry().from_json(
                        js=entry
                    ))

                # entry is ConnectEntry
                if entry['type'] == 'ConnectEntry':
                    # convert this dict to an offer objetc then!
                    entry_list.append(ConnectEntry().from_json(
                        js=entry
                    ))

        return entry_list

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

        # create object from json
        if 'title' in js.keys():
            title = js['title']
        else:
            title = None

        if 'id' in js.keys():
            id = js['id']
        else:
            id = None

        if 'comment' in js.keys():
            comment = js['comment']
        else:
            comment = None

        if 'comment_b' in js.keys():
            comment_b = js['comment_b']
        else:
            comment_b = None

        if 'date_fmt' in js.keys():
            date_fmt = js['date_fmt']
        else:
            date_fmt = None

        if 'date' in js.keys():
            try:
                date = datetime.strptime(js['date'], '%Y-%m-%d').date()
            except Exception:
                date = None
        else:
            date = None

        if 'delivery' in js.keys():
            delivery = js['delivery']
        else:
            delivery = None

        if 'due_days' in js.keys():
            due_days = js['due_days']
        else:
            due_days = None

        if 'paid_date' in js.keys():
            try:
                paid_date = datetime.strptime(js['paid_date'], '%Y-%m-%d').date()
            except Exception:
                paid_date = None
        else:
            paid_date = None

        if 'wage' in js.keys():
            wage = js['wage']
        else:
            wage = None

        if 'commodity' in js.keys():
            commodity = js['commodity']
        else:
            commodity = None

        if 'round_price' in js.keys():
            round_price = js['round_price']
        else:
            round_price = None

        if 'entry_list' in js.keys():
            entry_list = js['entry_list']
            entry_list = cls().load_entry_list_from_js(lis=entry_list)
        else:
            entry_list = None

        # return new object
        return cls(
            title=title,
            id=id,
            comment=comment,
            comment_b=comment_b,
            date_fmt=date_fmt,
            date=date,
            delivery=delivery,
            due_days=due_days,
            paid_date=paid_date,
            wage=wage,
            commodity=commodity,
            round_price=round_price,
            entry_list=entry_list
        )

    def get_price_total(self, wage=None, project=None, tax=False, round_price=None):
        """Get prices of entries summerized."""
        if wage is None:
            wage = self.get_wage(project=project)

        if round_price is None:
            round_price = self._round_price

        # init output variable
        out = Decimal(0)

        # iterate through the entries and get its price
        for e in self._entry_list:
            out += e.get_price(
                entry_list=self._entry_list,
                wage=wage
            ) if not tax else e.get_price_tax(
                entry_list=self._entry_list,
                wage=wage,
                round_price=round_price
            )

        # return it, check if rounded or not
        if round_price and not tax:
            return round(out)
        else:
            return out

    def get_price_tax_total(self, wage=None, project=None, round_price=None):
        """Get summerized total tax prices form entry_list."""
        return self.get_price_total(
            wage=wage,
            project=project,
            tax=True,
            round_price=round_price
        )

    def get_time_total(self):
        """Get times of entries summerized."""
        # init output variable
        out = QuantityTime('0:00')

        # iterate through the entries and get its time
        for e in self._entry_list:
            out += e.get_time(
                entry_list=self._entry_list
            )

        # return it
        return out

    def get_hourly_wage(self, wage=None, project=None, tax=False, round_price=None):
        """Calculate hourly wage according to price and time."""
        if wage is None:
            wage = self.get_wage(project=project)

        if round_price is None:
            round_price = self._round_price

        # get price
        price = self.get_price_total(
            wage=wage,
            tax=tax,
            round_price=round_price
        )

        # get hours from total time
        hours = self.get_time_total().get()

        # check round price for own output
        if round_price:
            rounder = 0
        else:
            rounder = 2

        # simply return a Decimal with the calculation
        if hours > 0.0:
            return round(Decimal(float(price) / float(hours)), rounder)
        else:
            return round(Decimal(0), rounder)

    def get_finish_days(self, project=None):
        """Calculate and return the finish days."""
        # if no project is given, return -1
        if not check_objects.is_project(project):
            return -1

        # get time needed for this offer
        time = self.get_time_total()

        # get hours per day
        hours_per_day = project.get_hours_per_day()

        # get days and add one safety day and the minimum days
        finish_days = round(time.full() / hours_per_day) + 1 + project.get_minimum_days()

        # return calculation
        return finish_days

    def get_finish_date(self, project=None):
        """Calculate and return the finish date."""
        # if no project is given, return 1987-15-10
        if not check_objects.is_project(project) or self._date is None:
            return ddate(1987, 10, 15)

        # get time needed for this offer
        time = self.get_time_total()

        # get initial date
        date = self._date

        # get first workday
        while date.weekday() not in project.get_work_days():
            date += timedelta(days=1)

        # add minimum_days
        min_days = project.get_minimum_days()
        while min_days > 0:
            # add the day only, if it is a working day
            if date.weekday() in project.get_work_days():
                min_days -= 1

            # add a day
            date += timedelta(days=1)

        # subtract hours_per_day from time on work_days, till time <= 0
        while time > 0:
            # t's a work day so subtract hours_per_day from time
            if date.weekday() in project.get_work_days():
                time -= project.get_hours_per_day()

            # add a day
            date += timedelta(days=1)

        return date

    def get_project(self, global_list=None):
        """Get project of this offer/invoice."""
        if not check_objects.is_list(global_list):
            return False

        # iter through the projects
        for project in global_list.project_list:
            # offer found, return its project
            if self in project.get_offer_list():
                return project

            # invoice found, return its project
            if self in project.get_invoice_list():
                return project

    def get_client(self, global_list=None, project=None):
        """Get client of this offer/invoice."""
        if not check_objects.is_list(global_list):
            return False

        if project is None:
            project = self.get_project(global_list=global_list)

        return global_list.get_client_by_id(client_id=project.client_id)

    def export_to_openoffice(
        self,
        client=None,
        project=None,
        global_list=None,
        settings=None,
        template=None,
        file=None
    ):
        """Export the offer to an open office file with the secretary module."""
        try:
            import secretary
        except Exception:
            return False

        is_client = check_objects.is_client(client)
        is_project = check_objects.is_project(project)
        is_list = check_objects.is_list(global_list)
        is_settings = check_objects.is_settings(settings)
        is_template = os.path.isfile(template)
        one_not_correct = (
            not is_client or
            not is_project or
            not is_list or
            not is_settings or
            not is_template
        )

        # cancel if one argument is not valid
        if one_not_correct:
            return False

        # cancel if template does not exist
        if not os.path.isfile(template):
            return False

        # get replacement dict
        replace_me = replacer(
            settings=settings,
            global_list=global_list,
            client=client,
            project=project,
            offerinvoice=self
        )

        # get extension from template
        template_name, template_ext = os.path.splitext(template)

        # get accordingly extension for filename
        if template_ext == '.ott' or template_ext == '.odt':
            file_ext = '.odt'
        elif template_ext == '.ots' or template_ext == '.ods':
            file_ext = '.ods'
        else:
            # cancel if template is no openoffice template
            return False

        # get filename with replaced values, if file not empty
        if file != '':
            file = file.format(**replace_me).replace(' ', '_')

        # use the offer title as filename
        else:
            file = self.title.format(**replace_me).replace(' ', '_')

        # check if output file exists and alter the name then
        file_num = 2
        file_new = file + file_ext
        while os.path.isfile(file_new):
            file_new = file + '_' + str(file_num) + file_ext
            file_num += 1
        file = file_new

        # replace the replacer
        for x in replace_me.keys():
            replace_me[x] = replacer(
                text=str(replace_me[x]),
                settings=settings,
                global_list=global_list,
                client=client,
                project=project,
                offerinvoice=self
            )

        # get entries
        entries = []
        position = 0
        for e in self._entry_list:
            position += 1

            time = e.get_time(
                entry_list=self._entry_list
            )

            price = e.get_price(
                entry_list=self._entry_list,
                wage=self.get_wage(project=project),
                round_price=self._round_price
            )

            price_unit = e.get_unit_price(
                entry_list=self._entry_list,
                wage=self.get_wage(project=project),
                round_price=self._round_price
            )

            tax = e.get_price_tax(
                entry_list=self._entry_list,
                wage=self.get_wage(project=project),
                round_price=self._round_price
            )

            tax_unit = e.get_unit_price_tax(
                entry_list=self._entry_list,
                wage=self.get_wage(project=project),
                round_price=self._round_price
            )

            total = price + tax
            total_unit = price_unit + tax_unit

            tmp_replacer = {
                'E_POSITION': position,
                'E_TITLE': e.title,
                'E_COMMENT': e.comment,
                'E_TIME': e.get_time(
                    entry_list=self._entry_list
                ),
                'E_QUANTITY': e.get_quantity_str(),
                'E_QUANTITY_B': e.get_quantity_b_str(),
                'E_PRICE': '{} {}'.format(price, replace_me['COMMODITY']),
                'E_UNIT_PRICE': '{} {}'.format(price_unit, replace_me['COMMODITY']),
                'E_PRICE_TAX': '{} {}'.format(tax, replace_me['COMMODITY']),
                'E_UNIT_PRICE_TAX': '{} {}'.format(tax_unit, replace_me['COMMODITY']),
                'E_TOTAL': '{} {}'.format(total, replace_me['COMMODITY']),
                'E_UNIT_TOTAL': '{} {}'.format(total_unit, replace_me['COMMODITY']),
                'E_TAX_PERCENT': '{}'.format(round(e.get_tax_percent())),
                'E_HAS_TAX': (tax > 0)
            }

            title = replacer(
                text=e.title,
                settings=settings,
                global_list=global_list,
                client=client,
                project=project,
                offerinvoice=self
            )
            title = title.format(**tmp_replacer)

            comment = replacer(
                text=e.comment,
                settings=settings,
                global_list=global_list,
                client=client,
                project=project,
                offerinvoice=self
            )
            comment = comment.format(**tmp_replacer)

            entries.append(
                {
                    'POSITION': position,
                    'TITLE': title,
                    'COMMENT': comment,
                    'TIME': time,
                    'QUANTITY': e.get_quantity_str(),
                    'QUANTITY_B': e.get_quantity_b_str(),
                    'PRICE': '{} {}'.format(price, replace_me['COMMODITY']),
                    'UNIT_PRICE': '{} {}'.format(price_unit, replace_me['COMMODITY']),
                    'PRICE_TAX': '{} {}'.format(tax, replace_me['COMMODITY']),
                    'UNIT_PRICE_TAX': '{} {}'.format(tax_unit, replace_me['COMMODITY']),
                    'TOTAL': '{} {}'.format(total, replace_me['COMMODITY']),
                    'UNIT_TOTAL': '{} {}'.format(total_unit, replace_me['COMMODITY']),
                    'TAX_PERCENT': '{}'.format(round(e.get_tax_percent())),
                    'HAS_TAX': (tax > 0)
                }
            )

        # final rendering
        engine = secretary.Renderer()

        # try to replace stuff in the template
        try:
            result = engine.render(
                template,
                entries=entries,
                data=replace_me
            )

            output = open(file, 'wb')
            output.write(result)
            output.close()

            return True

        except Exception:
            print('TEMPLATE PROBABLY HAS INVALID VARIABLES')
            return False


class Offer(OfferInvoice):
    """The offer object."""

    def copy(self):
        """Copy the own offer into new offer object."""
        return Offer().from_json(js=self.to_json())


class Invoice(OfferInvoice):
    """The invoice object."""

    def copy(self):
        """Copy the own offer into new offer object."""
        return Invoice().from_json(js=self.to_json())
