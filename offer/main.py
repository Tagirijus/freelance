"""
A tool for generating an offer.

This tool calculates prices according to hour times wage. It can be handy
for self-employed people, who has to send offers to clients. It is also
handy for just calculating the estimated time for a specific task.
"""

from clients.client import Client
from clients.project import Project
from decimal import Decimal
from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry
import os
from general.settings import Settings
from general.default import Default


def main():
    """Run the programm."""
    s = Settings()
    s.set_def_language('de')
    s.save_settings_to_file()
