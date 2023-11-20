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

# This script is the starting point. Process the input, ask the user for additional
# information and stores the new word on the database with its translation

import argparse
import sqlite3

# TODO Add logging replacing the print calls
GRAMMATICAL_DATABASE_LOCAL_FILENAME = 'data/grammatical_dictionary.db'

def return_first_row_of_sql_statement(database_file, sql_statement : str, params):
    with sqlite3.connect(database_file) as db_connection:
        db_cursor = db_connection.cursor()
        db_cursor.execute(sql_statement, params)
        return db_cursor.fetchone()

def trim_lower_case(input : str):
    return input.strip().lower()

parser = argparse.ArgumentParser(
     prog='flashcardCreatorBG',
     description='Selects vocabulary and generates flashcards for studying')
parser.add_argument('-d', '--flashcard-database', type=str, default='flashcards.sqlite')
parser.add_argument('-v', '--verbose', action='store_true', help='Shows what the flash generator is doing')
parser.add_argument('word_to_import', type=trim_lower_case, help='Word which you want to study')

global_arguments = parser.parse_args()
print(global_arguments)

# Find what type of word is it together with its writing rules
search_params = (global_arguments.word_to_import, )
found_classified_word = return_first_row_of_sql_statement(GRAMMATICAL_DATABASE_LOCAL_FILENAME, '''
    SELECT w.id, w.type_id, wt.speech_part, wt.comment, wt.rules, wt.rules_test
    FROM derivative_form as df
    join word as w
    on w.id = df.base_word_id
    join word_type as wt
    on w.type_id = wt.id
    where df.name = ?;
''', search_params)



print(found_classified_word)

# Check if the word already exists in the flashcard database

# Find translation in English for the word

# Ask the user to accept the translation

# If the noun is irregular, ask the user what he wants to study

# Add the word to the flashcard database
