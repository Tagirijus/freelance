"""
A client and project management suite.

You can organize clients, projects, write offers and invoices.
"""

# erst einmal nur das offer Modul
# später wird gefragt, was geladen werden soll:
# z.B. Kunden bearbeiten, Projekte, Rechnungen, Angebote ...
from offer import main

if __name__ == '__main__':
    main.main()
