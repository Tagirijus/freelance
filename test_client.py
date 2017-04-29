"""Testing app for client class."""

from clients.client import Client


def test_client_integrity():
    """Test the client class integrity."""
    client_1 = Client(
        client_id='WEHW01',
        company='Wurst Entertainment',
        salutation='Herr',
        name='Hans',
        family_name='Wurst',
        street='Würstchenstraße 85',
        post_code='11183',
        city='Bockwurstingen',
        language='de'
    )

    client_2 = Client(
        client_id='WEHW02',
        company='Wurst Entertainment',
        salutation='Frau',
        name='Hansina',
        family_name='Wurst',
        street='Würstchenstraße 85',
        post_code='11183',
        city='Bockwurstingen',
        language='de'
    )

    client_3 = Client(
        client_id='BCIP01',
        company='Big Company',
        salutation='Mr.',
        name='Important',
        family_name='Person',
        street='Famous-Street 35',
        post_code='356cb',
        city='Famous-Town',
        language='en'
    )

    # add them all to the global client_list
    client_list = []
    client_list.append(client_1)
    client_list.append(client_2)
    client_list.append(client_3)


def test_client_json_conversion():
    """Test conversion of client object to / from json."""
    client_4 = Client(
        client_id='ABAB01',
        company='Abi Bubi',
        salutation='Herr',
        name='Abridula',
        family_name='Badeldecku',
        street='Am Stackelstick 113',
        post_code='33947',
        city='Fummelbummel',
        language='de'
    )

    # get new client from existing one via json
    new_client = Client().from_json(js=client_4.to_json())

    # both live in the same street
    assert client_4.street == new_client.street

    # both have the same ID
    assert client_4.client_id == new_client.client_id
