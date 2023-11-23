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


import flashcardcreator

from flashcardcreator.affix import calculate_derivative_forms_of_noun

CONFIG_FILENAME = 'configuration.ini'
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    prog='flashcardCreatorBG',
    description='Selects vocabulary and generates flashcards for studying')
parser.add_argument('-d', '--flashcard-database', type=str,
                    default='flashcards.sqlite')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='Shows what the flash generator is doing')
parser.add_argument('-vv', '--debug', action='store_true',
                    help='Shows debug information')
parser.add_argument('word_to_import',
                    help='Word which you want to study')

global_arguments = parser.parse_args()
logger.debug(f'Received parameters: {global_arguments}')

flashcardcreator.main.flashcard_database = global_arguments.flashcard_database
flashcardcreator.main.load_logging_configuration(debug=global_arguments.debug,
                                                 verbose=global_arguments.verbose)

found_word = flashcardcreator.main.WordFinder.find_word_with_english_translation(
    global_arguments.word_to_import)
if found_word is None:
    exit(1)

config = configparser.ConfigParser(interpolation=None)
config.read(CONFIG_FILENAME)

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
