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


def _remove_empty_conversions(rule):
    match rule:
        case '0':
            return ''
        case '\\-':
            return None
        case _:
            return rule


def _check_if_fullfils_condition(word_root, first_rule):
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


def _check_if_ends_with_suffix_to_replace(word_root, suffix_to_replace):
    """
    Confirms that the suffix of the word root is present.
    :param suffix_to_replace: Suffix which is going to be replaced to create the derivative forms
    :raises: ValueError if the suffix is absent
    :return: None
    """
    if not suffix_to_replace:
        return

    word_condition_pattern = fr'.*{suffix_to_replace}$'
    if not re.match(word_condition_pattern, word_root):
        raise ValueError(
            f'The word'f's root {word_root} must end with {suffix_to_replace}')


def _calculate_all_derivative_forms_using_string_concatenation(word_root,
                                                               suffix_to_replace,
                                                               rules):
    """
    Generates the derivative forms by replacing a suffix to the root.
    :param word_root: Word root
    :param suffix_to_replace: Suffix to replace in the word root
    :param rules: Suffixes for the derivate forms
    :return: List with the derivative forms
    """
    if suffix_to_replace == '':
        word_rest = word_root
    else:
        word_rest = word_root[:-len(suffix_to_replace)]

    return [word_rest + _remove_empty_conversions(
        rule) for
            rule in rules]


def _calculate_derivative_form_using_pattern_replacement(word_root,
                                                         pattern_to_replace,
                                                         rule):
    """
    Generates one derivative form by replacing multiple parts of the word root.

    :param word_root: Word root
    :param pattern_to_replace: Pattern to replace in the word root
    :param rule: Pattern for the derivate forms
    :return: String with derivative forms
    """
    pattern_to_replace_regexp_compiled = _generate_root_replacement_without_brackets(
        pattern_to_replace)
    logger.debug(
        f"Pattern to replace regexp: {pattern_to_replace_regexp_compiled} from {pattern_to_replace}")
    rule_suffix = _generate_rule_suffix_regex_without_question_marks(rule)
    logger.debug(f"Rule suffix: {rule_suffix} from {rule}")
    derivate_form = re.sub(pattern_to_replace_regexp_compiled, rule_suffix,
                           word_root)
    logger.debug(f"Derivate form: {derivate_form}")
    return derivate_form


def _generate_rule_suffix_regex_without_question_marks(rule):
    question_mark_index = 0


    def replace_question_mark(match):
        nonlocal question_mark_index
        question_mark_index += 1
        return f'\\{question_mark_index}'


    pattern_question_mark = re.compile(r'\?')
    return re.sub(pattern_question_mark, replace_question_mark, rule)


def _generate_root_replacement_without_brackets(pattern_to_replace):
    brackets_pattern = re.compile(r'(\[.\])', re.UNICODE)
    brackets_replacement_one_character = '(.)'
    pattern_to_replace_regexp = re.sub(brackets_pattern,
                                       brackets_replacement_one_character,
                                       pattern_to_replace)
    return re.compile(pattern_to_replace_regexp,
                      re.UNICODE)


def _calculate_all_derivative_forms_using_pattern_replacement(word_root,
                                                              pattern_to_replace,
                                                              rules):
    """
    Generates the derivative forms by replacing multiple parts of the word root.
    :param word_root: Word root
    :param pattern_to_replace: Pattern to replace in the word root
    :param rules: Patterns for the derivate forms
    :return: List with the derivative forms
    """
    return [_calculate_derivative_form_using_pattern_replacement(word_root,
                                                                 pattern_to_replace,
                                                                 rule) for rule
            in rules]


def _calculate_all_derivative_forms(word_root, rules_string):
    """
    It applies the given rules to generate all possible derivative forms
    The syntax of the rules comes from the library bgoffice and it is based on the affix definition of ispell.

    :param word_root: Word in its original form
    :param rules_string: Contains the derivation rules
    :return: A list containing all derivative forms. The first element is the word root
    """
    rules = rules_string.split('\n')
    _check_if_fullfils_condition(word_root, rules[0])
    if ',' in rules[0]:
        suffix_to_replace, _ = rules[0].split(', ')
    else:
        suffix_to_replace = rules[0]
    # Discard the first rule which contains the conditions
    rules = rules[1:]
    rules = [rule for rule in rules if rule != '-' and len(rule) > 0]
    if suffix_to_replace == '0':
        suffix_to_replace = ''
    _check_if_ends_with_suffix_to_replace(word_root, suffix_to_replace)
    if '[' in suffix_to_replace:
        derivative_forms = _calculate_all_derivative_forms_using_pattern_replacement(
            word_root, suffix_to_replace, rules)
    else:
        derivative_forms = _calculate_all_derivative_forms_using_string_concatenation(
            word_root, suffix_to_replace, rules)
    logger.debug(f'Derivative forms {derivative_forms}')
    return derivative_forms


def calculate_derivative_forms_of_noun(word_root, rules_string, speech_part):
    """
    Generates all derivative forms using the given rules.

    :param speech_part: Type of the word
    :param word_root: Masculine noun without definite article
    :param rules_string: List of replacements from the grammatical database for this noun
    :return: dictionary containing the derivative forms
    """

    all_derivative_forms = _calculate_all_derivative_forms(word_root,
                                                           rules_string)
    rules_meaning_and_position = {
        'singular_indefinite': 0,
        'singular_definite': 1,
        'plural_indefinite': 2,
        'plural_definite': 3,
        'contable': None
    }
    if speech_part == 'noun_male':
        rules_meaning_and_position = {
            'singular_indefinite': 0,
            'singular_definite': 2,
            'plural_indefinite': 3,
            'plural_definite': 4,
            'contable': 5
        }

    derivative_forms = {key: all_derivative_forms[rule_position]
                        for key, rule_position in
                        rules_meaning_and_position.items()
                        if rule_position is not None}
    logger.debug(f'Derivative forms of the noun {derivative_forms}')
    return derivative_forms
