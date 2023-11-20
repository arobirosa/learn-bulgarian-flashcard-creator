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

# This script downloads the dictionary data, creates a local database

import configparser
import gzip
import urllib.request
import sqlite3
from os.path import exists

# TODO Add logging replacing the print calls
# TODO Move this module to a package in the main application
# TODO Internationalize user inputs

# The database file located at https://rechnik.chitanka.info/db.sql.gz can only be downloaded with an interactive browser.
# It moved it to my own hosting. It has the GPL 2 license
GRAMMATICAL_DATABASE_URL = 'https://files.areko.consulting/rechnik.chitanka.info.bulgarian.db.sqlite.gz'
GRAMMATICAL_DATABASE_LOCAL_FILENAME = 'data/grammatical_dictionary.db'


def run_count_sql_statement_using_config(sql_statement : str):
    with sqlite3.connect(GRAMMATICAL_DATABASE_LOCAL_FILENAME) as db_connection:
        db_cursor = db_connection.cursor()
        db_cursor.execute(sql_statement)
        firstRow = db_cursor.fetchone()
        firstValue, = firstRow
        return firstValue
    return -1


def was_grammar_database_imported():
    """
    Checks if the database contains the expected number of derivative words.
    :return: True if the database has the grammatical information
    """
    if not exists(GRAMMATICAL_DATABASE_LOCAL_FILENAME):
        return False

    if run_count_sql_statement_using_config("SELECT count(1) FROM sqlite_schema WHERE type = 'table' AND name = "
                                      "'derivative_form';") != 1:
        return False

    derivative_words_count = run_count_sql_statement_using_config('select count(1) from derivative_form')
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

        with open(GRAMMATICAL_DATABASE_LOCAL_FILENAME, 'wb+') as uncompressed_database_file:
            print(f'Saving data to {uncompressed_database_file.name}')
            uncompressed_database_file.write(uncompressed_dbdump_data)

    print('Checking if the database was correctly downloaded')
    return was_grammar_database_imported()


# Main body
if not download_import_grammar_database():
    exit(2)
else:
    print('Now you can start using the flash creator')
