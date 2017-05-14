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
from offer.offeramounttime import OfferAmountTime
import os


class OfferInvoice(object):
    """A class holding a list of entries."""

    def __init__(
        self,
        title=None,
        id=None,
        comment=None,
        date_fmt=None,
        date=None,
        due_days=None,
        due_date=None,
        paid=None,
        wage=None,
        round_price=None,
        entry_list=None
    ):
        """Initialize the class."""
        self.title = '' if title is None else str(title)
        self.id = '' if id is None else str(id)
        self.comment = '' if comment is None else str(comment)
        self.date_fmt = '%d.%m.%Y' if date_fmt is None else str(date_fmt)
        self._date = ddate.today()          # set default
        self.set_date(date)                 # try to set arguments value
        self._due_days = 14                 # set default
        self.set_due_days(due_days)         # try to set arguments value
        self._due_date = ddate.today()      # set default
        self.set_due_date(due_date)         # try to set arguments value
        self._paid = False                  # set default
        self.set_paid(paid)                 # try to set arguments value
        self._round_price = False           # set default
        self.set_round_price(round_price)   # try to set arguments value
        self._wage = Decimal(0)             # set default
        self.set_wage(wage)                 # try to set arguments value
        self._entry_list = []               # set default
        self.set_entry_list(entry_list)     # try to set arguments value

    def set_date(self, value):
        """Set date."""
        if type(value) is ddate:
            self._date = value
        else:
            try:
                self._date = datetime.strptime(value, '%Y-%m-%d').date()
            except Exception:
                pass

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

    def set_due_date(self, value):
        """Set due_date."""
        if type(value) is ddate:
            self._due_date = value
        else:
            try:
                self._due_date = datetime.strptime(value, '%Y-%m-%d').date()
            except Exception:
                # calculate it with the due_days
                self._due_date = ddate.today() + timedelta(days=self._due_days)

    def get_due_date(self):
        """Get due_date."""
        return self._due_date

    def set_paid(self, value):
        """Set paid."""
        try:
            self._paid = bool(value)
        except Exception:
            pass

    def get_paid(self):
        """Get paid."""
        return self._paid

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
        out['date_fmt'] = self.date_fmt

        try:
            out['date'] = self._date.strftime('%Y-%m-%d')
        except Exception:
            out['date'] = ddate.today().strftime('%Y-%m-%d')

        out['due_days'] = self._due_days

        try:
            out['due_date'] = self._due_date.strftime('%Y-%m-%d')
        except Exception:
            out['due_date'] = ddate.today().strftime('%Y-%m-%d')

        out['paid'] = self._paid
        out['wage'] = float(self._wage)
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
    def from_json(cls, js=None, keep_date=True):
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

        if 'due_days' in js.keys():
            due_days = js['due_days']
        else:
            due_days = None

        if 'due_date' in js.keys():
            try:
                due_date = datetime.strptime(js['due_date'], '%Y-%m-%d').date()
            except Exception:
                due_date = None
        else:
            due_date = None

        if not keep_date:
            date = None
            due_date = None
            due_remind = None

        if 'paid' in js.keys():
            paid = js['paid']
        else:
            paid = None

        if 'wage' in js.keys():
            wage = js['wage']
        else:
            wage = None

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
            date_fmt=date_fmt,
            date=date,
            due_days=due_days,
            due_date=due_date,
            paid=paid,
            wage=wage,
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
                wage=wage
            )

        # return it, check if rounded or not
        if round_price:
            return round(out)
        else:
            return out

    def get_price_tax_total(self, wage=None, project=None, round_price=None):
        """Get summerized total tax prices form entry_list."""
        return self.get_price_total(
            wage=wage, project=project, tax=True, round_price=round_price
        )

    def get_time_total(self):
        """Get times of entries summerized."""
        # init output variable
        out = OfferAmountTime('0:00')

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

    def get_finish_date(self, project=None):
        """Calculate and return the finish date."""
        # if no projetc is given, return 1987-15-10
        # if not is_project(project):
        if not check_objects.is_project(project):
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
            file = replacer(
                text=file,
                settings=settings,
                client=client,
                project=project,
                global_list=global_list
            ).replace(' ', '_')

        # use the offer title as filename
        else:
            file = self.title.replace(' ', '_')

        # check if output file exists and alter the name then
        file_num = 2
        file_new = file + file_ext
        while os.path.isfile(file_new):
            file_new = file + '_' + str(file_num) + file_ext
            file_num += 1
        file = file_new

        # get replacement dict
        replace_me = replacer(
            settings=settings,
            client=client,
            project=project,
            global_list=global_list
        )

        # get own data for this offer as well
        commodity = settings.defaults[client.language].commodity

        replace_me['TITLE'] = self.title

        replace_me['COMMENT'] = self.comment

        replace_me['WAGE'] = '{} {}/h'.format(
            self.get_wage(project=project),
            commodity
        )

        price_total = self.get_price_total(
            wage=self.get_wage(project=project),
            project=project,
            round_price=self.get_round_price()
        )
        replace_me['PRICE_TOTAL'] = '{} {}'.format(
            price_total,
            commodity
        )

        tax_total = self.get_price_total(
            wage=self.get_wage(project=project),
            project=project,
            tax=True,
            round_price=self.get_round_price()
        )
        replace_me['TAX_TOTAL'] = '{} {}'.format(
            tax_total,
            commodity
        )

        replace_me['PRICE_TAX_TOTAL'] = '{} {}'.format(
            price_total + tax_total,
            commodity
        )

        if self.date_fmt != '':
            replace_me['DATE'] = self._date.strftime(self.date_fmt)
        else:
            replace_me['DATE'] = self._date

        replace_me['FINISH_DATE'] = self.get_finish_date(project=project)

        replace_me['TIME_TOTAL'] = self.get_time_total()

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

            entries.append(
                {
                    'POSITION': position,
                    'TITLE': e.title,
                    'COMMENT': e.comment,
                    'TIME': time,
                    'AMOUNT': e.get_amount_str(),
                    'PRICE': '{} {}'.format(price, commodity),
                    'UNIT_PRICE': '{} {}'.format(price_unit, commodity),
                    'TAX': '{} {}'.format(tax, commodity),
                    'UNIT_TAX': '{} {}'.format(tax_unit, commodity)
                }
            )

        # final endering
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

    def copy(self, keep_date=True):
        """Copy the own offer into new offer object."""
        return Offer().from_json(js=self.to_json(), keep_date=keep_date)


class Invoice(OfferInvoice):
    """The invoice object."""

    def copy(self, keep_date=True):
        """Copy the own offer into new offer object."""
        return Invoice().from_json(js=self.to_json(), keep_date=keep_date)
