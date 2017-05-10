"""Simple debug function."""


def debug(text):
    """Write debug text into DEBUG.txt."""
    f = open('DEBUG.txt', 'w')
    f.write(str(text))
    f.close()
