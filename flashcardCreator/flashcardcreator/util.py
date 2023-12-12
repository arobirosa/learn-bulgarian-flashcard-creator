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

# Contains methods related with the configuration files
import os
import logging

EXPRESSION_WORD_TYPE = 'expression'
OTHER_WORD_TYPES = [EXPRESSION_WORD_TYPE, 'abreviation', 'adjective', 'adverb',
                    'conjuntion',
                    'geographical', 'idiom',
                    'interjection', 'math',
                    'name_bg-place',
                    'name_bg-various',
                    'name_capital', 'name_city',
                    'name_country',
                    'name_popular',
                    'name_various',
                    'noun_plurale-tantum',
                    'numeral', 'particle',
                    'phrase', 'plural', 'prefix',
                    'preposition',
                    'suffix']

logger = logging.getLogger(__name__)


def convert_to_absolute_path(relative_file):
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.abspath(
        os.path.join(current_script_directory, "..", relative_file))
    logger.debug(f"Absolute path: {file_path}")
    return file_path
