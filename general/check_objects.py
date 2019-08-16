"""Due to circular dependencies I created these functions to check objeckts."""


def is_client(obj=None):
    """Check object."""
    try:
        return obj.__class__.__name__ == 'Client'
    except Exception:
        return False


def is_project(obj=None):
    """Check object."""
    try:
        return obj.__class__.__name__ == 'Project'
    except Exception:
        return False


def is_offer(obj=None):
    """Check object."""
    try:
        return obj.__class__.__name__ == 'Offer'
    except Exception:
        return False


def is_invoice(obj=None):
    """Check object."""
    try:
        return obj.__class__.__name__ == 'Invoice'
    except Exception:
        return False


def is_settings(obj=None):
    """Check object."""
    try:
        return obj.__class__.__name__ == 'Settings'
    except Exception:
        return False


def is_list(obj=None):
    """Check object."""
    try:
        return obj.__class__.__name__ == 'List'
    except Exception:
        return False


def is_entry(obj=None):
    """Check object."""
    try:
        return (
            obj.__class__.__name__ == 'BaseEntry' or
            obj.__class__.__name__ == 'MultiplyEntry' or
            obj.__class__.__name__ == 'ConnectEntry'
        )
    except Exception:
        return False


def is_preset(obj=None):
    """Check object."""
    try:
        return obj.__class__.__name__ == 'Preset'
    except Exception:
        return False
