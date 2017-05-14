"""
A client and project management suite.

You can organize clients, projects, write offers and invoices.
"""

from npy_gui import npy_gui


def main():
    """Run the programm with the npyscreen GUI."""
    app = npy_gui.FreelanceApplication()
    app.run()

if __name__ == '__main__':
    main()
