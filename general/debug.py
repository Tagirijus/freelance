"""Simple debug function."""


def debug(text=None, obj=None):
    """Write debug text into DEBUG.txt."""
    out = ''

    # handle text first
    out += str(text) + '\n'

    # handle an object
    if obj is not None:
        out += '\n'
        out += 'Object str: ' + str(obj) + '\n'
        out += 'Object type: ' + str(type(obj)) + '\n'

    f = open('DEBUG.txt', 'w')
    f.write(out)
    f.close()
