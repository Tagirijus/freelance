"""The class holds a list of entries."""


class Offer(object):
    """A class holding a list of entries."""

    def __init__(
        self,
        title='',
        number=1
    ):
        """Initialize the class."""
        self.title = str(title)
        self._number = 1        # set default
        self.set_number(number) # try to set argument

    def set_number(self, value):
        """Set number."""
        try:
            self._number = int(value)
        except Exception:
            pass

    def get_number(self):
        """Get number."""
        return self._number
