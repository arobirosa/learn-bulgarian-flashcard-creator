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
from getpass import getpass
from mysql.connector import connect, Error

config = configparser.ConfigParser()
config.read("configuration.ini")
if 'GrammaticalDictionary.User' in config:
    print('The connection to the database containing the grammatical dictionary was already configured')
    exit(1)

print('Downloading the database with the grammatical classification')

print('Please provide the credentials to connect to your MySQL server')
database_host=input('Please enter the hostname or IP (Default is localhost): ')
if not database_host:
    database_host = 'localhost'
database_port_str=input('Please enter the port (Default is 3336): ')
if database_port_str:
    database_port = int(database_port_str)
else:
    database_port = 3306
database_user=input('Please enter the username with rights to create databases and users: ')
if not database_user:
    print('No user was entered. Exiting')
    exit(2)
database_password=getpass('Please enter the password of the user with rights to create databases and users: ')
if not database_password:
    print('No password was entered. Exiting')
    exit(2)

print('Attempting to connect to the database server')
try:
    with connect(host=database_host, port=database_port, user=database_user, password=database_password) as database_connection:
        print('Connection SUCCESSFUL.')
except Error as e:
    print('The connection failed:', e)
    exit(3)

print('Now we are going to create database with the grammatical classification')



# create user bgDictionaryUser@localhost identified by 'changeme'
# grant all on bgDictionary.* to bgDictionaryUser@localhost;
# create database bulgarianDictionary;
# https://rechnik.chitanka.info/db.sql.gz
