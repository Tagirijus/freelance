"""Testing app for client and project class."""

from clients.client import Client
from clients.project import Project


def test_client_project_id_checks():
    """Test the integrity of client and project class IDs."""
    client_a = Client(client_id='A')
    client_b = Client(client_id='B')

    c_list = []
    c_list.append(client_a)
    c_list.append(client_b)

    project_a_a = Project(client_id='A', title='AA')
    project_a_b = Project(client_id='A', title='AB')
    project_b_a = Project(client_id='B', title='BA')
    project_b_b = Project(client_id='B', title='BB')

    p_list = []
    p_list.append(project_a_a)
    p_list.append(project_a_b)
    p_list.append(project_b_a)
    p_list.append(project_b_b)

    # try to change client_a ID to client_b ID
    check = c_list[0].set_client_id('B', c_list)
    assert check is False
    assert c_list[0].get_client_id() == 'A'

    # try to assign project AA to non existing client ID
    check = p_list[0].set_client_id('C', c_list)
    assert check is False
    assert p_list[0].get_client_id() == 'A'

    # assign project BB to client_a
    assert p_list[3].get_client_id() == 'B'         # before it belongs to B
    check = p_list[3].set_client_id('A', c_list)
    assert check is True
    assert p_list[3].get_client_id() == 'A'         # now it bleongs to A

    # client_a now has 3 projects and client_b only 1
    client_a_len = len(c_list[0].get_project_list(p_list))
    client_b_len = len(c_list[1].get_project_list(p_list))
    assert client_a_len == 3
    assert client_b_len == 1
