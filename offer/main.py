"""
A tool for generating an offer.

This tool calculates prices according to hour times wage. It can be handy
for self-employed people, who has to send offers to clients. It is also
handy for just calculating the estimated time for a specific task.
"""

from clients.client import ClientList
from clients.client import Client
from clients.project import ProjectList
from clients.project import Project
from general.settings import Settings
import time


def main():
    """Run the programm."""
    start = time.time()
    s = Settings()
    client_list = ClientList(data_path=s.data_path)
    project_list = ProjectList(data_path=s.data_path)

    print(len(project_list.get_project_list()))

    print("--- %s seconds ---" % (round(time.time() - start, 4)))
