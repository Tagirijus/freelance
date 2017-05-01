"""
A tool for generating an offer.

This tool calculates prices according to hour times wage. It can be handy
for self-employed people, who has to send offers to clients. It is also
handy for just calculating the estimated time for a specific task.
"""

from clients.list import List
from clients.list import get_inactive_list
from clients.list import activate_project
from general.settings import Settings
import time


def main():
    """Run the programm."""
    start = time.time()

    s = Settings()
    l = List(data_path=s.data_path)

    ld = get_inactive_list(settings=s)

    print('Act   len:', len(l.project_list))
    print('Deact len:', len(ld.project_list))
    print()

    # deactivate the project
    #l.deactivate_project(project=l.project_list[0], inactive_dir=s.inactive_dir)

    # active the project again
    activate_project(l, ld, ld.project_list[1])

    print('Act   len:', len(l.project_list))
    print('Deact len:', len(ld.project_list))
    print()

    print("--- %s seconds ---" % (round(time.time() - start, 4)))
