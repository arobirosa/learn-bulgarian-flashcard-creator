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

# TODO Add translation with PONS
# TODO Add translation with Mymemory https://mymemory.translated.net/doc/spec.php
# TODO Check licenses of the dependencies
# TODO Internationalize all prompts

import argparse
import configparser
import logging.config
import yaml
import unicodedata

import flashcardcreator
import flashcardcreator.userinput
from flashcardcreator.affix import calculate_derivative_forms_of_noun
from flashcardcreator.translator import translate_text_to_english
from flashcardcreator.database import insert_noun, \
    return_first_row_of_sql_statement

GRAMMATICAL_DATABASE_LOCAL_FILENAME = 'data/grammatical_dictionary.db'
CONFIG_FILENAME = 'configuration.ini'
logger = logging.getLogger(__name__)


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])


def trim_lower_case(input_word: str):
    return remove_accents(input_word.strip().lower())


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
found_classified_word = flashcardcreator.database.return_first_row_of_sql_statement(
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

word_id, root_word, word_type_id, speech_part, word_type_rules, word_type_rules_test, word_type_example_word = found_classified_word
logger.debug(
    f'The word {root_word} is classified as {found_classified_word}')

config = configparser.ConfigParser(interpolation=None)
config.read(CONFIG_FILENAME)
if speech_part not in config:
    raise ValueError(
        f'The speech part {speech_part} isn''t supported. If you want to support it, please add a section to the configuration file')

# Check if the word already exists in the flashcard database
word_search_parameters = {
    'wordToSearch': root_word,
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
    logger.info(f'The word {root_word} has already flash cards')
    exit(3)

# Find translation in English for the word
translated_word_original = translate_text_to_english(root_word,
                                                     debug_client_calls=global_arguments.debug)

logger.info(
    f'The word {root_word} translates to "{translated_word_original}" ')

# Ask the user to accept the translation
final_translation = flashcardcreator.userinput.ask_user_for_translation(
    root_word, translated_word_original)
if not final_translation:
    logger.info("Exiting because no translation was provided")
    exit(5)

logger.debug(f'The final translation is {final_translation}')

# If the noun is irregular, keep only what is important to study
all_derivative_forms = calculate_derivative_forms_of_noun(
    root_word, word_type_rules, speech_part)
derivative_forms_to_keep_config = config[speech_part].get(str(word_type_id))
if derivative_forms_to_keep_config:
    derivative_forms_to_keep = derivative_forms_to_keep_config.split(
        ',')
else:
    raise ValueError(
        f'The configuration value for {word_type_id} inside {speech_part} section is missing. The derivate forms were {all_derivative_forms}')

derivative_forms_to_study = {key: all_derivative_forms[key] for key in
                             derivative_forms_to_keep if
                             key in all_derivative_forms}
logger.debug(
    f'The following derivative forms are import to study {derivative_forms_to_study}')


# Add the word to the flashcard database
def calculate_noun_gender(speech_part):
    match speech_part:
        case 'noun_female':
            return 'f'
        case 'noun_neutral':
            return 'n'
        case 'noun_male':
            return 'm'
        case _:
            raise ValueError(
                f'Unable to get the gender for the speech part {speech_part}')


noun_fields = {
    'noun': root_word,
    'meaningInEnglish': final_translation,
    'genderAbrev': calculate_noun_gender(speech_part),
    'irregularPluralEnding': None,
    'irregularDefiniteArticle': None,
    'countableEnding': None,
    'irregularPluralWithArticle': None,
    'countableEnding': None,
    'externalWordId': word_id
}
if 'singular_definite' in derivative_forms_to_study:
    noun_fields['irregularDefiniteArticle'] = derivative_forms_to_study[
        'singular_definite']
if 'plural_indefinite' in derivative_forms_to_study:
    noun_fields['irregularPluralEnding'] = derivative_forms_to_study[
        'plural_indefinite']
if 'plural_definite' in derivative_forms_to_study:
    noun_fields['irregularPluralWithArticle'] = derivative_forms_to_study[
        'plural_definite']
if 'contable' in derivative_forms_to_study:
    noun_fields['countableEnding'] = derivative_forms_to_study['contable']

insert_noun(global_arguments.flashcard_database, noun_fields)
