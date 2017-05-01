"""
A tool for generating an offer.

This tool calculates prices according to hour times wage. It can be handy
for self-employed people, who has to send offers to clients. It is also
handy for just calculating the estimated time for a specific task.
"""

from clients.list import List
from general.settings import Settings
from clients.client import Client
from clients.project import Project
import time


def main():
    """Run the programm."""
    start = time.time()

    s = Settings()
    l = List(data_path=s.data_path)

    print("--- %s seconds ---" % (round(time.time() - start, 4)))
