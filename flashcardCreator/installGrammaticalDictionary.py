#  Copyright (c) 2023 Antonio Robirosa <flashcard.creator@areko.consulting>
#
#  This file is part of the Bulgarian Flashcard Creator.
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses/>.
#

# This script downloads the dictionary data, creates a local database and creates
# the configuration file.

import configparser
import gzip
import tempfile
import urllib.request
from getpass import getpass

from mysql.connector import connect, Error

# TODO Add logging replacing the print calls

# The database file located at https://rechnik.chitanka.info/db.sql.gz can only be downloaded with an interactive browser.
# It moved it to my own hosting. It has the GPL 2 license
CONFIG_FILENAME = 'configuration.ini'
GRAMMATICAL_DATABASE_URL = 'https://files.areko.consulting/rechnik.chitanka.info.bulgarian.db.sql.gz'


def run_sql_statement_using_config(sql_statement : str):
    config = configparser.ConfigParser(interpolation=None)
    config.read(CONFIG_FILENAME)
    with connect(host=config['GrammaticalDictionary']['Host'], port=int(config['GrammaticalDictionary']['Port']), user=config['GrammaticalDictionary']['User'], \
            password=config['GrammaticalDictionary']['Password'],database=config['GrammaticalDictionary']['Database']) as db_connection:
        with db_connection.cursor() as db_cursor:
            db_cursor.execute(sql_statement)
            return db_cursor.rowcount
    return -1;



def create_database_configuration():
    """
    Asks for the database parameters and saves the configuration on disk if the connection was successful
    :return:True if there were no errors
    """
    config = configparser.ConfigParser(interpolation=None)
    config.read(CONFIG_FILENAME)
    if 'GrammaticalDictionary' in config and config['GrammaticalDictionary'].get('User'):
        print('The connection to the database containing the grammatical dictionary was already configured')
        return True

    print('Please provide the credentials to connect to your MySQL server')
    database_host=input('Please enter the hostname or IP (Default is localhost): ')
    if not database_host:
        database_host = 'localhost'
    database_port_str=input('Please enter the port (Default is 3336): ')
    if database_port_str:
        database_port = int(database_port_str)
    else:
        database_port = 3306
    database_name=input('Please enter the name of the database: ')
    if not database_name:
        print('No database''s name was entered. Exiting')
        return False
    database_user=input('Please enter the username: ')
    if not database_user:
        print('No user was entered. Exiting')
        return False
    database_password=getpass('Please enter the password of the user: ')
    if not database_password:
        print('No password was entered. Exiting')
        return False

    print('Attempting to connect to the database server')
    try:
        with connect(host=database_host, port=database_port, user=database_user, password=database_password, database=database_name):
            print('Connection SUCCESSFUL.')
    except Error as e:
        print('The connection failed:', e)
        return False

    print("Saving the database connection information in the configuration file")
    config.add_section("GrammaticalDictionary")
    config['GrammaticalDictionary']['Host'] = database_host
    config['GrammaticalDictionary']['Port'] = str(database_port)
    config['GrammaticalDictionary']['Database'] = database_name
    config['GrammaticalDictionary']['User'] = database_user
    config['GrammaticalDictionary']['Password'] = database_password
    with open('configuration.ini', 'w') as configuration_file:
        config.write(configuration_file)

    return True


def was_grammar_database_imported():
    """
    Checks if the database contains the expected number of derivative words.
    :return: True if the database has the grammatical information
    """
    derivative_words_count = run_sql_statement_using_config('select count(1) from derivative_form')
    return derivative_words_count == 4013667


def download_import_grammar_database():
    print("Checking if the grammatical database was already downloaded.")
    if was_grammar_database_imported():
        print('The grammatical database was already imported')
        return True

    print('Downloading the database with the grammatical classification')
    auth_handler = urllib.request.HTTPBasicAuthHandler()
    # TODO Remove credentials from code and change them on server
    auth_handler.add_password(realm='please enter user and password',
                              uri='https://files.areko.consulting',
                              user='reader',
                              passwd='DQaGtM6LK3VNXras')
    opener = urllib.request.build_opener(auth_handler)
    urllib.request.install_opener(opener)

    with urllib.request.urlopen(GRAMMATICAL_DATABASE_URL) as url_downloader_response, gzip.GzipFile(fileobj=url_downloader_response) as compressed_file:
        print(f'Downloading {GRAMMATICAL_DATABASE_URL}. Please wait 3-5 minutes')
        uncompressed_dbdump_data = compressed_file.read()

        with tempfile.NamedTemporaryFile(suffix='dict.sql', delete=False) as uncompressed_file:
            print(f'Saving data to {uncompressed_file.name}')
            uncompressed_file.write(uncompressed_dbdump_data)

    print('Now we are going to create database with the grammatical classification')
    run_sql_statement_using_config(f'source {uncompressed_file.name}')
    return was_grammar_database_imported()


# Main body
if not create_database_configuration():
    exit(1)
elif not download_import_grammar_database():
    exit(2)
else:
    print('Now you can start using the flash creator')
