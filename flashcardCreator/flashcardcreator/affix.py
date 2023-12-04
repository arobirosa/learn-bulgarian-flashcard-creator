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
from flashcardcreator.database import return_rows_of_sql_statement, \
    GRAMMATICAL_DATABASE_LOCAL_FILENAME

DERIVATIVE_FORMS_DESCRIPTIONS_TO_ENGLISH_NAMES = {
    'ед.ч.': 'singular_indefinite',
    'ед.ч. пълен член': 'singular_definite',
    'ед.ч. членувано': 'singular_definite',
    'мн.ч.': 'plural_indefinite',
    'мн.ч. членувано': 'plural_definite',
    'бройна форма': 'contable',
    'м.р.': 'masculineForm',
    'ж.р.': 'femenineForm',
    'ср.р.': 'neutralForm',
    'мн.ч.': 'pluralForm'
}

VERB_PARTICIPLES_WHICH_MIGHT_BE_IRREGULAR = (
    #  Причастия (отглаголни прилагателни)
    'мин.деят.св.прич. м.р.',
    'мин.деят.св.прич. ж.р.',
    'мин.деят.св.прич. ср.р.',
    'мин.деят.св.прич. мн.ч.',
    'мин.деят.св.прич. м.р. пълен член',
    'мин.деят.несв.прич. м.р.',
    'мин.деят.несв.прич. мн.ч.',
    'мин.страд.прич. ср.р.',
    'сег.деят.прич. м.р.',
    'деепричастие'
)

VERB_DERIVATIVE_FORMS_WHICH_MIGHT_BE_IRREGULAR = (
    # Сегашно време
    'сег.вр., 1л., ед.ч.',
    'сег.вр., 2л., ед.ч.',
    'сег.вр., 3л., мн.ч.',  # Some "я" mutate to "е" or "а" like ям
    # Минало свършено време (аорист)
    'мин.св.вр., 1л., ед.ч.',
    'мин.св.вр., 2л., ед.ч.',
    # Минало несвършено време (имперфект)
    'мин.несв.вр., 1л., ед.ч.',
    'мин.несв.вр., 2л., ед.ч.',
    # Imperative
    'повелително наклонение, ед.ч.',
    'повелително наклонение, мн.ч.'
)

logger = logging.getLogger(__name__)


def _find_all_derivative_forms(base_word_id):
    """
    Find all the derivative forms stored in the grammatical database. This is easier than using the rules with affixes of the word types to generate the words.

    :param base_word_id: ID of the root word
    :return: A list containing all derivative forms. The first element is the word root
    """
    search_params = {'base_word_id': base_word_id}
    found_derivative_forms = return_rows_of_sql_statement(
        GRAMMATICAL_DATABASE_LOCAL_FILENAME, '''
            select name, description
            from derivative_form
            where base_word_id = :base_word_id
            order by id;
        ''', search_params)
    logger.debug(f'Derivative forms {found_derivative_forms}')
    return found_derivative_forms


def calculate_derivative_forms_with_english_field_names(base_word_id):
    """
    Generates all derivative forms

    :param base_word_id: ID of the root word
    :return: dictionary containing the derivative forms
    """

    all_derivative_forms = _find_all_derivative_forms(base_word_id)

    derivative_forms = {
        DERIVATIVE_FORMS_DESCRIPTIONS_TO_ENGLISH_NAMES[
            description_bg]: derivative_form
        for derivative_form, description_bg in
        all_derivative_forms
        if description_bg in DERIVATIVE_FORMS_DESCRIPTIONS_TO_ENGLISH_NAMES}
    logger.debug(f'Derivative forms of the word {derivative_forms}')
    return derivative_forms


def calculate_derivative_forms_from_verb(base_word_id):
    """
    Returns derivative forms of verbs which could be irregular

    :param base_word_id: ID of the root word
    :return: dictionary containing the derivative forms
    """

    all_derivative_forms = _find_all_derivative_forms(base_word_id)

    derivative_forms = {
        description_bg: derivative_form for derivative_form, description_bg in
        all_derivative_forms
        if
        description_bg in VERB_DERIVATIVE_FORMS_WHICH_MIGHT_BE_IRREGULAR or description_bg in VERB_PARTICIPLES_WHICH_MIGHT_BE_IRREGULAR}
    logger.debug(f'Derivative forms of the verb {derivative_forms}')
    return derivative_forms


def filter_verb_participles(derivative_forms_to_study):
    """
    It returns the keys containing the verb participles if the are present in the derivative forms to study
    :param derivative_forms_to_study: Required. Dictionary with the derivative forms
    :return: Verb participles
    """
    return {participle: derivative_form for participle, derivative_form in
            derivative_forms_to_study
            if participle in VERB_PARTICIPLES_WHICH_MIGHT_BE_IRREGULAR}
