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
from tkinter import messagebox

from flashcardcreator.main import set_flashcard_database, \
    load_logging_configuration, WordFinder, parse_line
from flashcardcreator.userinput import ask_user_for_a_word_and_a_type
from flashcardcreator.util import OTHER_WORD_TYPES

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

group_word_source = parser.add_argument_group('Word source',
                                              'Where does the word(s) come from?')
exclusive_group_word_source = group_word_source.add_mutually_exclusive_group(
    required=True)
exclusive_group_word_source.add_argument('-a', '--ask-word-continuously',
                                         action='store_true', required=False,
                                         help='Ask the user to enter one or more words')
exclusive_group_word_source.add_argument('-w', '--word', dest='word_to_import',
                                         metavar='WORD',
                                         help='One word as parameter in the command line')
exclusive_group_word_source.add_argument('-i', '--input-file',
                                         dest='input_file_path',
                                         type=str,
                                         help='A file with words to import. It must exist. Please check the file format in the documentation.')
parser.add_argument('-o', '--output-file',
                    dest='output_file_path',
                    type=str,
                    help='A file where you want to store the results of the import. If it exists, the lines will be appended."')
parser.add_argument('-t', '--other-word-type',
                    choices=OTHER_WORD_TYPES,
                    help='If the word cannot be found in the grammar dictionary, imports it with this word type')

global_arguments = parser.parse_args()
logger.debug(f'Received parameters: {global_arguments}')
if global_arguments.ask_word_continuously and global_arguments.other_word_type is not None:
    parser.error(
        "The parameter --other-word-type can only be used when only word is imported")
if global_arguments.input_file_path and global_arguments.output_file_path is None:
    parser.error("The parameter --output-file is missing")

set_flashcard_database(global_arguments.flashcard_database)
load_logging_configuration(debug=global_arguments.debug,
                           verbose=global_arguments.verbose)


def find_word_and_create_flashcards(word_to_import, other_word_type):
    """
    Finds and creates the flashcards for the given word
    :param other_word_type: Type of the word if it isn't found in the grammar dictionary
    :param word_to_import: Flashcards will be created for this word
    :return: None if the word wasn't found. True if the flash card was created. False if the creation was aborted.
    """
    found_word = WordFinder.find_word_with_english_translation(word_to_import,
                                                               other_word_type)
    if found_word is None or found_word.has_flashcards():
        return None
    if not found_word.create_flashcard():
        return False
    found_word.create_flashcards_for_linked_words()
    return True


def show_word_not_found_dialog(word):
    message = f"The word {word} cannot be found or has already flashcards"
    messagebox.showinfo("Error", message)


if global_arguments.word_to_import:
    find_word_and_create_flashcards(global_arguments.word_to_import,
                                    global_arguments.other_word_type)
elif global_arguments.ask_word_continuously:
    while True:
        result_tuple = ask_user_for_a_word_and_a_type()
        if not result_tuple:
            logger.info("The user wants to exit")
            break
        word_to_import, word_type = result_tuple
        logger.debug(f'The user entered the word {word_to_import}')
        creation_result = find_word_and_create_flashcards(word_to_import,
                                                          word_type)
        if creation_result is None:
            show_word_not_found_dialog(word_to_import)
    logger.info("Exiting")
elif global_arguments.input_file_path:
    with open(global_arguments.input_file_path, 'r') as file, \
            open(global_arguments.output_file_path, 'a') as output_file:
        for line in file:
            parsedLine = parse_line(line)
            if parsedLine.is_comment:
                output_file.write(f"{parsedLine.original_line}")
            elif parsedLine.error:
                output_file.write(f"# ERROR: {parsedLine.error}\n")
                output_file.write(f"{parsedLine.original_line}")
            else:
                # Add the word or phrase to the flashcard database
                found_word = WordFinder.find_word_with_english_translation(
                    parsedLine.word_or_phrase,
                    parsedLine.word_type,
                    parsedLine.translation)
                if found_word is None:
                    output_file.write(
                        "# ERROR: The following word wasn't found\n")
                    output_file.write(f"{parsedLine.original_line}")
                elif found_word.exists_flashcard_for_this_word():
                    output_file.write(
                        f"# INFO: The word {parsedLine.word_or_phrase} already has flashcards\n")
                else:
                    if not found_word.create_flashcard():
                        output_file.write(
                            f"# ERROR: No flashcards were created for the word '{parsedLine.word_or_phrase}'\n")
                    else:
                        found_word.create_flashcards_for_linked_words()
                        logger.debug(
                            f"Flashcard for {parsedLine.word_or_phrase} and linked words were created")
