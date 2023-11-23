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


def remove_empty_conversions(rule):
    match rule:
        case '0':
            return ''
        case '\\-':
            return None
        case _:
            return rule


def check_if_fullfils_condition(word_root, first_rule):
    """
    If the first derivation rule contains a condition, checks that the root word fullfils it.
    Throws an exception if not.

    :param word_root: Word to test
    :param first_rule:  String containing the suffix of the word root to replace when creating the derivate forms and possible a conditions
    """
    if ',' not in first_rule:
        return
    _, word_condition = first_rule.split(', ')
    word_condition_pattern = fr'.*{word_condition}$'
    if not re.match(word_condition_pattern, word_root):
        raise ValueError(
            f'The word'f's root {word_root} must end with {word_condition}')


def calculate_derivative_forms_of_noun(word_root, rules_string, speech_part):
    """
    :param word_root: Masculine noun without definite article
    :param rules_string: List of replacements from the grammatical database for this noun
    :return: dictionary containing the derivative forms
    """
    rules = rules_string.split('\n')
    check_if_fullfils_condition(word_root, rules[0])
    if ',' in rules[0]:
        suffix_to_replace, _ = rules[0].split(', ')
    else:
        suffix_to_replace = rules[0]
    if suffix_to_replace == '0':
        suffix_to_replace = ''
    elif not word_root.endswith(suffix_to_replace):
        raise ValueError(
            f'The word'f's root {word_root} must end with {suffix_to_replace}')
    if suffix_to_replace == '':
        word_rest = word_root
    else:
        word_rest = word_root[:-len(suffix_to_replace)]

    rules_meaning_and_position = {
        'singular_indefinite': 1,
        'singular_definite': 2,
        'plural_indefinite': 3,
        'plural_definite': 4,
        'contable': None
    }
    if speech_part == 'noun_male':
        rules_meaning_and_position = {
            'singular_indefinite': 1,
            'singular_definite': 3,
            'plural_indefinite': 4,
            'plural_definite': 5,
            'contable': 6
        }

    derivative_forms = {key: word_rest + remove_empty_conversions(
        rules[rule_position]) for
                        key, rule_position in
                        rules_meaning_and_position.items()
                        if rule_position is not None}
    logger.debug(f'Derivative forms of the noun {derivative_forms}')
    return derivative_forms
