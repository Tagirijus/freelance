"""A simple command line program to convert between clients and coma separated."""

import argparse
from clients.client import Client
import csv
import os


DEFAULT_COLUMNS = [
    'id',
    'company',
    'attention',
    'salutation',
    'name',
    'family_name',
    'street',
    'post_code',
    'city',
    'country',
    'tax_id',
    'language'
]


def save_client_to_file(directory=None, client=None):
    """Save single client to file."""
    is_client = type(client) is Client
    is_dir = directory is not None

    if not is_client or not is_dir:
        return False

    path = str(directory)

    # create dir if it does not exist
    is_dir = os.path.isdir(str(path))
    is_file = os.path.isfile(str(path))
    if not is_dir and not is_file:
        os.mkdir(path)

    # generate filenames
    filename = path + '/' + client.client_id.replace(' ', '_') + '.flclient'

    # write the file
    f = open(filename, 'w')
    f.write(client.to_json())
    f.close()

    return True


def load_clients(directory=None):
    """Load the clients from files in the directory and return list with clients."""
    if directory is not None:
        if not os.path.isdir(str(directory)):
            return []

    path = str(directory)

    # cycle through the files and append them converted from json to the list
    out = []
    for file in sorted(os.listdir(path)):
        if file.endswith('.flclient'):
            # load the file
            f = open(path + '/' + file, 'r')
            load = f.read()
            f.close()

            # convert file content to Client object and append it
            out.append(Client().from_json(js=load))

    return out


def converter(
    file=None,
    directory=None,
    columns=None,
    store=False,
    delimiter=',',
    quotechar='"'
):
    """Convert from / to coma separated file from / to Freelance client data."""
    is_file = file is not None
    is_dir = directory is not None
    columns_set = type(columns) is list

    # cancel if no file and no directory is given
    if not is_file and not is_dir:
        return False

    # init variables
    clients = []
    clients_csv = []

    # get defaults, if not columns_valid
    if not columns_set:
        columns = DEFAULT_COLUMNS
    else:
        columns = columns[:12]

    # csv > Freelance client data
    if not store:

        # cancel if file does not exists
        if not os.path.isfile(file):
            return False

        # load the file to convert it into client data
        with open(file, 'r', newline='') as csvfile:
            reader = csv.reader(
                csvfile,
                delimiter=delimiter,
                quotechar=quotechar
            )
            for row in reader:
                clients_csv.append(row)

        # convert the clients_csv to client objects
        for client in clients_csv:

            # init new temp client
            new_client = Client()

            # cycle through the columns of the csv
            for i, col in enumerate(client):

                # check if iteration is <= len of columns
                if i < len(columns):

                    # check what this column is supposed to be

                    if columns[i] == 'id':
                        new_client.client_id = col

                    if columns[i] == 'company':
                        new_client.company = col

                    if columns[i] == 'attention':
                        new_client.attention = col

                    if columns[i] == 'salutation':
                        new_client.salutation = col

                    if columns[i] == 'name':
                        new_client.name = col

                    if columns[i] == 'family_name':
                        new_client.family_name = col

                    if columns[i] == 'street':
                        new_client.street = col

                    if columns[i] == 'post_code':
                        new_client.post_code = col

                    if columns[i] == 'city':
                        new_client.city = col

                    if columns[i] == 'country':
                        new_client.country = col

                    if columns[i] == 'tax_id':
                        new_client.tax_id = col

                    if columns[i] == 'language':
                        new_client.language = col

                    # append this client to the clients
                    clients.append(new_client.copy())

        # save the clients to the directory
        for client in clients:
            save_client_to_file(
                directory=directory,
                client=client
            )

    # csv > Freelance client data
    else:

        # cancel if dir does not exists
        if not os.path.isdir(directory):
            return False

        # get the clients from the directory
        clients = load_clients(directory=directory)

        # convert the clients to clients_csv (list)
        for client in clients:

            # init new temp client
            new_client = []

            # get correct column for data
            for x in range(0, len(columns)):

                if columns[x] == 'id':
                    new_client.append(client.client_id)

                if columns[x] == 'company':
                    new_client.append(client.company)

                if columns[x] == 'attention':
                    new_client.append(client.attention)

                if columns[x] == 'salutation':
                    new_client.append(client.salutation)

                if columns[x] == 'name':
                    new_client.append(client.name)

                if columns[x] == 'family_name':
                    new_client.append(client.family_name)

                if columns[x] == 'street':
                    new_client.append(client.street)

                if columns[x] == 'post_code':
                    new_client.append(client.post_code)

                if columns[x] == 'city':
                    new_client.append(client.city)

                if columns[x] == 'country':
                    new_client.append(client.country)

                if columns[x] == 'tax_id':
                    new_client.append(client.tax_id)

                if columns[x] == 'language':
                    new_client.append(client.language)

            # append this client to the clients_csv
            clients_csv.append(new_client)

        # save the clients_csv to the file
        with open(file, 'w', newline='') as csvfile:
            writer = csv.writer(
                csvfile,
                delimiter=delimiter,
                quotechar=quotechar,
                quoting=csv.QUOTE_MINIMAL
            )

            # write header
            writer.writerow(columns)

            # write the client rows
            for row in clients_csv:
                writer.writerow(row)

    return True


def main():
    """Main programm, when started directly."""
    # getting the arguments
    args = argparse.ArgumentParser(
        description=(
            'A simple command line programm for converting between clients '
            'and a coma separated file holding these data.'
        )
    )

    args.add_argument(
        '-f',
        '--file',
        help='coma separated file for loading or saving the conversion data'
    )

    args.add_argument(
        '-d',
        '--directory',
        help='directory for loading or saving the converted Freelance client data'
    )

    args.add_argument(
        '-s',
        '--store',
        action='store_true',
        help=(
            'if set, the programm will convert from Freelance client data to the '
            'coma separated file - otherwise the other direction'
        )
    )

    args.add_argument(
        '-c',
        '--columns',
        metavar='.',
        help='header which column is what data for/in the coma separated file'
    )

    args.add_argument(
        '--delimiter',
        default=',',
        help='the delimiter of the coma separated file'
    )

    args.add_argument(
        '--quotechar',
        default='"',
        help='the quotechar of the coma separated file'
    )

    args.add_argument(
        '-l',
        '--list',
        action='store_true',
        help='list the default columns list and thus the possible column names'
    )

    args = args.parse_args()

    # list default columns
    if args.list:
        print('Column names / default columns are:')
        print(' '.join(DEFAULT_COLUMNS))
        exit()

    # set the filename for the csv
    if args.file is None:
        args.file = 'csv.csv'

        # cancel if this file already exists
        if os.path.exists(args.file):
            print('No -f/--file is set and default filename alreay exists.')
            exit()

    # set dirctory for the client data
    if args.directory is None:
        args.directory = 'client_data/'

        # cancel if it exists
        if os.path.exists(args.directory):
            print('No -d/--directory is set and default directory alreay exists.')
            exit()

    # pass the arguments to the main function
    worked = converter(
        file=args.file,
        directory=args.directory,
        columns=args.columns,
        store=args.store,
        delimiter=args.delimiter,
        quotechar=args.quotechar
    )

    if not worked:
        print('Something went wrong while converting.')
    else:
        print('Successfully converted the data!')


if __name__ == '__main__':
    main()
