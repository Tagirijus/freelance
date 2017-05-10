"""The class for the amount of the entries."""

from decimal import Decimal


class OfferAmountTime(object):
    """
    The OfferAmountTime class.

    A flexible object, which can be represented as a Decimal or a time-string
    like "1:45", if the internal value is 1.75, for example.
    """

    def __init__(self, input=None):
        """Initialize the class."""
        self._type = 'decimal'      # decimal | time
        self._full = Decimal(0)     # set default
        self.set(i=input)           # try to set arguments value

    def __str__(self):
        """Str representation."""
        if self._type == 'time':
            return self.time()

        else:
            return str(self.get())

    def __repr__(self):
        """Same as str."""
        return self.__str__()

    def __add__(self, other):
        """Add."""
        out = self._full

        # check if same type and calculate
        if type(other) is OfferAmountTime:
            out += Decimal(other._full)
        else:
            out += Decimal(other)

        return OfferAmountTime(out)

    def __radd__(self, other):
        """Add."""
        return self.__add__(other)

    def __sub__(self, other):
        """Sub."""
        out = self._full

        # check if same type and calculate
        if type(other) is OfferAmountTime:
            out -= Decimal(other._full)
        else:
            out -= Decimal(other)

        return OfferAmountTime(out)

    def __rsub__(self, other):
        """Sub."""
        # check if same type
        if type(other) is OfferAmountTime:
            out = Decimal(other._full)
        else:
            out = Decimal(other)

        # calculate
        out -= Decimal(self._full)

        return OfferAmountTime(out)

    def __mul__(self, other):
        """Multiply."""
        out = self._full

        # check if same type and calculate
        if type(other) is OfferAmountTime:
            out *= Decimal(other._full)
        else:
            out *= Decimal(other)

        return OfferAmountTime(out)

    def __rmul__(self, other):
        """Multiply."""
        return self.__mul__(other)

    def __truediv__(self, other):
        """Divide."""
        out = self._full

        # check if same type and calculate
        if type(other) is OfferAmountTime:
            out /= Decimal(other._full)
        else:
            out /= Decimal(other)

        return OfferAmountTime(out)

    def __rtruediv__(self, other):
        """Divide."""
        # check if same type
        if type(other) is OfferAmountTime:
            out = Decimal(other._full)
        else:
            out = Decimal(other)

        # calculate
        out /= Decimal(self._full)

        return OfferAmountTime(out)

    def __lt__(self, other):
        """Lower than."""
        if type(other) is OfferAmountTime:
            return self._full < other._full
        else:
            return self._full < other

    def __le__(self, other):
        """Lower equal than."""
        if type(other) is OfferAmountTime:
            return self._full <= other._full
        else:
            return self._full <= other

    def __eq__(self, other):
        """Equal to."""
        if type(other) is OfferAmountTime:
            return self._full == other._full
        else:
            return self._full == other

    def __ne__(self, other):
        """Not equal."""
        if type(other) is OfferAmountTime:
            return self._full != other._full
        else:
            return self._full != other

    def __ge__(self, other):
        """Greater equal."""
        if type(other) is OfferAmountTime:
            return self._full >= other._full
        else:
            return self._full >= other

    def __gt__(self, other):
        """Greater than."""
        if type(other) is OfferAmountTime:
            return self._full > other._full
        else:
            return self._full > other

    def __round__(self, *args):
        """Round."""
        self._full = round(self._full, *args)
        return self

    def set(self, i=None):
        """Convert object from time string or decimal."""
        try:
            # it's directly convertable to Decimal
            self._full = Decimal(str(i))
            self._type = 'decimal'
            return True
        except Exception:
            # it has to be parsed
            # split by ':'
            full = Decimal(0)
            for c, num in enumerate(str(i).split(':')):
                try:
                    # convert to full hours / minutes / whatever
                    if c == 0:
                        full += Decimal(num)

                    # convert to minutes and set new values
                    elif c == 1:
                        # convert to minutes
                        full += Decimal(num) / Decimal(60)

                        # set new values
                        self._full = full
                        self._type = 'time'
                        return True

                except Exception:
                    # error, cancel
                    return False

    def get(self):
        """Get decimal full as Decimal."""
        return self._full

    def full_remain(self):
        """Get (full, remain) tuple."""
        h, m = divmod(self._full, 1)
        m = m * 60
        return (round(h), round(m))

    def full(self):
        """Get full only."""
        return self.full_remain()[0]

    def remain(self):
        """Get full only."""
        return self.full_remain()[1]

    def time(self):
        """Get formatted time as string."""
        return '{}:{:02}'.format(
            self.full(),
            abs(self.remain())
        )

    def type(self, value=None):
        """Set type."""
        if value == 'decimal' or value == 'dec' or value == 'd':
            self._type = 'decimal'
        elif value == 'time' or value == 'tim' or value == 't':
            self._type = 'time'
