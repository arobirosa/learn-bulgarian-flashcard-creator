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

import logging.config


from flashcardcreator.main import set_flashcard_database, \
    load_logging_configuration, WordFinder

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

set_flashcard_database(global_arguments.flashcard_database)
load_logging_configuration(debug=global_arguments.debug,
                           verbose=global_arguments.verbose)

found_word = WordFinder.find_word_with_english_translation(
    global_arguments.word_to_import)
if found_word is None:
    exit(1)

found_word.create_flashcard()
