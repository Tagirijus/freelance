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
import uuid


def main():
    """Run the programm."""
    s = Settings()
    client_list = ClientList(data_path=s.data_path)
    project_list = ProjectList(data_path=s.data_path)

    # client = client_list.get_client_list()[0]
    # for x in client.get_project_list(
    #         project_list.get_project_list()):
    #     print(client.get_client_id(), x.get_project_id())

    print(len(project_list.get_project_list()))
    # generate many projects for a
    # for x in range(0,350):
    #     project_list.append(Project(client_id='k', title=str(uuid.uuid1())))
    # print(len(project_list.get_project_list()))
