"""
A tool for generating an offer.

This tool calculates prices according to hour times wage. It can be handy
for self-employed people, who has to send offers to clients. It is also
handy for just calculating the estimated time for a specific task.
"""

from clients.list import List
# from clients.list import get_inactive_list
# from clients.list import activate_project
from datetime import datetime
from general.preset import Preset
from general.settings import Settings
from offer.offer import Offer
from offer.entries import BaseEntry
from offer.entries import MultiplyEntry
from offer.entries import ConnectEntry
import time


def main():
    """Run the programm."""
    start = time.time()

    s = Settings()
    l = List(data_path=s.data_path)
    p = Preset(data_path=s.data_path)

    # ld = get_inactive_list(settings=s)

    print("--- %s seconds ---" % (round(time.time() - start, 4)))
