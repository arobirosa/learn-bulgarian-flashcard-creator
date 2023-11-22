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

import logging

# These methods calculate the derivate forms of the word's root
import re

logger = logging.getLogger(__name__)


def calculate_derivative_forms_of_noun(word_root, rules_string):
    """
    :param word_root: Masculine noun without definite article
    :param rules_string: List of replacements from the grammatical database for this noun
    :return: dictionary containing the derivative forms
    """
    rules = rules_string.split('\n')
    suffix_to_replace, word_condition = rules[0].split(', ')
    if not word_root.endswith(suffix_to_replace):
        raise ValueError(f'The word'f's root {word_root} must end with {suffix_to_replace}')
    word_condition_pattern = fr'.*{word_condition}$'
    if not re.match(word_condition_pattern, word_root):
        raise ValueError(f'The word'f's root {word_root} must end with {word_condition}')
    word_rest = word_root[:-len(suffix_to_replace)]
    derivative_forms = {
        'singular_indefinite': word_rest + rules[1],
        'singular_definite': word_rest + rules[2],
        'plural_indefinite': word_rest + rules[3],
        'plural_definite': word_rest + rules[4],
    }
    logger.debug(f'Derivative forms of the noun {derivative_forms}')
    return derivative_forms
