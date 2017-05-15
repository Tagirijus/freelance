"""
A client and project management suite.

You can organize clients, projects, write offers and invoices.

Author: Manuel Senfft (www.tagirijus.de)
"""

from npy_gui import npy_gui


def main():
    """Run the programm with the npyscreen GUI."""
    app = npy_gui.FreelanceApplication()
    app.run()

if __name__ == '__main__':
    main()
