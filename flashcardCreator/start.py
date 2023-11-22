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
import configparser
import logging.config
import sqlite3

import yaml

from flashcardcreator.translator import translate_text_to_english

GRAMMATICAL_DATABASE_LOCAL_FILENAME = 'data/grammatical_dictionary.db'
CONFIG_FILENAME = 'configuration.ini'
logger = logging.getLogger(__name__)


def return_first_row_of_sql_statement(database_file, sql_statement: str,
                                      params):
    with sqlite3.connect(database_file) as db_connection:
        db_cursor = db_connection.cursor()
        db_cursor.execute(sql_statement, params)
        return db_cursor.fetchone()


def trim_lower_case(input_word: str):
    return input_word.strip().lower()


parser = argparse.ArgumentParser(
    prog='flashcardCreatorBG',
    description='Selects vocabulary and generates flashcards for studying')
parser.add_argument('-d', '--flashcard-database', type=str,
                    default='flashcards.sqlite')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='Shows what the flash generator is doing')
parser.add_argument('-vv', '--debug', action='store_true',
                    help='Shows debug information')
parser.add_argument('word_to_import', type=trim_lower_case,
                    help='Word which you want to study')

global_arguments = parser.parse_args()

# Logging configuration
if global_arguments.debug:
    logging_level = logging.DEBUG
elif global_arguments.verbose:
    logging_level = logging.INFO
else:
    logging_level = logging.WARNING

with open('conf/logging.yaml', 'r') as logging_config:
    config = yaml.load(logging_config, Loader=yaml.FullLoader)
    logging.config.dictConfig(config)

logger.setLevel(logging_level)
logger.debug(f'Received parameters: {global_arguments}')

# Find what type of word is it together with its writing rules
search_params = {'word_to_import': global_arguments.word_to_import}
found_classified_word = return_first_row_of_sql_statement(
    GRAMMATICAL_DATABASE_LOCAL_FILENAME, '''
    SELECT w.id, w.name, w.type_id, wt.speech_part, wt.rules, wt.rules_test, wt.example_word
    FROM derivative_form as df
    join word as w
    on w.id = df.base_word_id
    join word_type as wt
    on w.type_id = wt.id
    where df.name = :word_to_import;
''', search_params)

if found_classified_word is None:
    logger.info(
        f'The word {global_arguments.word_to_import} is unknown. Exiting')
    exit(1)

word_id, word_original, word_type_id, speech_part, word_type_rules, word_type_rules_test, word_type_example_word = found_classified_word
logger.debug(
    f'The word {word_original} is classified as {found_classified_word}')

config = configparser.ConfigParser(interpolation=None)
config.read(CONFIG_FILENAME)
if ('WordTypes' not in config) or not config['WordTypes'].get(
        'supported_speech_parts'):
    logger.info(
        'The list of supported speech parts is missing inside the configuration')
    exit(2)

if speech_part not in config['WordTypes'].get('supported_speech_parts').split(
        ','):
    logger.info(f'The speech part {speech_part} is still not supported')
    exit(3)

# Check if the word already exists in the flashcard database
word_search_parameters = {
    'wordToSearch': word_original,
    'wordId': word_id
}
first_found_row = return_first_row_of_sql_statement(
    global_arguments.flashcard_database, '''
    select a.masculineForm, a.externalWordId
    from adjetives as a
    where a.masculineForm = :wordToSearch or a.externalWordId = :wordId
    union
    select n.noun, n.externalWordId
    from nouns as n
    where n.noun = :wordToSearch or n.externalWordId = :wordId
    union
    select o.word, o.externalWordId
    from otherWordTypes as o
    where o.word = :wordToSearch or o.externalWordId = :wordId
    union
    select vm.presentSingular1, vm.externalWordId
    from verbMeanings as vm
    where vm.presentSingular1 = :wordToSearch or vm.externalWordId = :wordId
''', word_search_parameters)

if first_found_row is not None:
    logger.info(f'The word {word_original} has already flash cards')
    exit(3)

# Find translation in English for the word
translated_word_original = translate_text_to_english(word_original,
                                                     debug_client_calls=global_arguments.debug)

logger.info(
    f'The word {word_original} translates to "{translated_word_original}" ')
# Ask the user to accept the translation

# If the noun is irregular, ask the user what he wants to study

# Add the word to the flashcard database
