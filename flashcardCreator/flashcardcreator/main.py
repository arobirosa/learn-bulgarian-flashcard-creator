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

import configparser
# Contains the main classes
import logging
import re
import sqlite3
import unicodedata
from abc import ABC, abstractmethod
from collections import defaultdict

import yaml

import flashcardcreator.userinput
from flashcardcreator.affix import \
    calculate_derivative_forms_with_english_field_names, \
    calculate_derivative_forms_from_verb, filter_verb_participles
from flashcardcreator.database import insert_noun, insert_adjective, \
    insert_other_word_type, \
    return_rows_of_sql_statement, GRAMMATICAL_DATABASE_LOCAL_FILENAME, \
    insert_participles_with_cursor, \
    insert_verb_meaning_with_cursor, insert_verb_tense_with_cursor, \
    verb_pair_not_exists, verb_pair_insert
from flashcardcreator.translator import translate_text_to_english
from flashcardcreator.util import OTHER_WORD_TYPES, EXPRESSION_WORD_TYPE

CONFIG_FILENAME = 'configuration.ini'

CYRILLIC_LETTERS_LOWER_UPPER_CASE_PAIRS = [
    ('а', 'А'),
    ('б', 'Б'),
    ('в', 'В'),
    ('г', 'Г'),
    ('д', 'Д'),
    ('е', 'Е'),
    ('ж', 'Ж'),
    ('з', 'З'),
    ('и', 'И'),
    ('й', 'Й'),
    ('к', 'К'),
    ('л', 'Л'),
    ('м', 'М'),
    ('н', 'Н'),
    ('о', 'О'),
    ('п', 'П'),
    ('р', 'Р'),
    ('с', 'С'),
    ('т', 'Т'),
    ('у', 'У'),
    ('ф', 'Ф'),
    ('х', 'Х'),
    ('ц', 'Ц'),
    ('ч', 'Ч'),
    ('ш', 'Ш'),
    ('щ', 'Щ'),
    ('ъ', 'Ъ'),
    ('ь', 'Ь'),
    ('ю', 'Ю'),
    ('я', 'Я')
]

logger = logging.getLogger(__name__)
# Location of the flashcard which can be given by the user
flashcard_database = None
main_debug = False
config = configparser.ConfigParser(interpolation=None)
config.read(CONFIG_FILENAME)


def _insert_verb(database_file, derivative_forms_to_study, root_word,
                 final_translation, word_id, is_terminative,
                 linked_verb_present_singular1):
    """
    Insert the verb in all required tables. It runs in a single transaction.

    :param is_terminative: Is is a terminative verb?
    :param word_id: Word ID in the grammatical database
    :param root_word: Singular first person in present tense
    :param derivative_forms_to_study: All derivative forms which are irregular
    :param final_translation: Translation in English accepted by the use
    :param database_file: Required.
    :param linked_verb_present_singular1: Optional. String with the singular in first person in present
    :return:
    """
    logger.info(
        f'Adding a flashcard for the verb {root_word} to all required tables')
    with sqlite3.connect(database_file) as db_connection:
        db_cursor = db_connection.cursor()
        # Причастия (отглаголни прилагателни)
        verb_participles = filter_verb_participles(derivative_forms_to_study)
        insert_participles_with_cursor(db_cursor, verb_participles,
                                       final_translation, word_id)

        # Meaning
        insert_verb_meaning_with_cursor(db_cursor, final_translation,
                                        word_id, root_word)

        derivative_forms_to_study_with_defaults = defaultdict(lambda: None)
        derivative_forms_to_study_with_defaults.update(
            derivative_forms_to_study)
        # Сегашно време
        insert_verb_tense_with_cursor(db_cursor,
                                      present_singular1=root_word,
                                      tense='p',
                                      imperfect=not is_terminative,
                                      singular1=root_word,
                                      singular2=
                                      derivative_forms_to_study_with_defaults[
                                          'сег.вр., 2л., ед.ч.'],
                                      plural3=
                                      derivative_forms_to_study_with_defaults[
                                          'сег.вр., 3л., мн.ч.'])
        # Минало свършено време (аорист)
        if 'мин.св.вр., 1л., ед.ч.' in derivative_forms_to_study_with_defaults or \
                'мин.св.вр., 2л., ед.ч.' in derivative_forms_to_study_with_defaults:
            insert_verb_tense_with_cursor(db_cursor,
                                          present_singular1=root_word,
                                          tense='a',
                                          imperfect=not is_terminative,
                                          singular1=
                                          derivative_forms_to_study_with_defaults[
                                              'мин.св.вр., 1л., ед.ч.'],
                                          singular2=
                                          derivative_forms_to_study_with_defaults[
                                              'мин.св.вр., 2л., ед.ч.'],
                                          plural3=None)

        # Минало несвършено време (имперфект)
        if not is_terminative and (
                'мин.несв.вр., 1л., ед.ч.' in derivative_forms_to_study_with_defaults or \
                'мин.несв.вр., 2л., ед.ч.' in derivative_forms_to_study_with_defaults):
            insert_verb_tense_with_cursor(db_cursor,
                                          present_singular1=root_word,
                                          tense='i',
                                          imperfect=not is_terminative,
                                          singular1=
                                          derivative_forms_to_study_with_defaults[
                                              'мин.несв.вр., 1л., ед.ч.'],
                                          singular2=
                                          derivative_forms_to_study_with_defaults[
                                              'мин.несв.вр., 2л., ед.ч.'],
                                          plural3=None)

        # Imperative
        if 'повелително наклонение, ед.ч.' in derivative_forms_to_study_with_defaults or \
                'повелително наклонение, мн.ч.' in derivative_forms_to_study_with_defaults:
            insert_verb_tense_with_cursor(db_cursor,
                                          present_singular1=root_word,
                                          tense='!',
                                          imperfect=not is_terminative,
                                          singular1=None,
                                          singular2=
                                          derivative_forms_to_study_with_defaults[
                                              'повелително наклонение, ед.ч.'],
                                          plural2=
                                          derivative_forms_to_study_with_defaults[
                                              'повелително наклонение, мн.ч.'],
                                          plural3=None)

        if linked_verb_present_singular1:
            if is_terminative:
                terminative_verb = root_word
                imperfective_verb = linked_verb_present_singular1
            else:
                terminative_verb = linked_verb_present_singular1
                imperfective_verb = root_word
            if verb_pair_not_exists(db_cursor, terminative_verb,
                                    imperfective_verb):
                verb_pair_insert(db_cursor, terminative_verb,
                                 imperfective_verb)

        db_connection.commit()
        logger.info(
            f'The verb {root_word} was added to all required tables')


class AbstractClassifiedWord(ABC):
    def __init__(self, word_id, root_word, word_meaning, word_type_id,
                 speech_part):
        self._word_id = word_id
        self._root_word = root_word
        self._meaning = word_meaning
        self._word_type_id = word_type_id
        self._speech_part = speech_part
        self._final_translation = None
        self.linked_word = None


    def exists_flashcard_for_this_word(self):
        """
        Check if the word already exists in the flashcard database

        :return: True if the word don't exist
        """
        word_search_parameters = {
            'wordToSearch': self._root_word,
            'wordId': self._word_id
        }
        found_flashcards = return_rows_of_sql_statement(
            flashcard_database, '''
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

        if found_flashcards:
            logger.warning(
                f'The word {self._root_word} has already flash cards')
            return True
        else:
            return False


    def ask_user_for_final_translation(self):
        """
        Uses a translation API to suggest the user a translation and ask him for a corrected translation
        :return: True if the final translation was accepted. False if the user wants to exit
        """
        global main_debug
        # Find an automatic translation in English for the word
        translated_word_original = translate_text_to_english(self._root_word,
                                                             debug_client_calls=main_debug)

        logger.info(
            f'The word {self._root_word} translates to "{translated_word_original}" ')

        # Ask the user to accept the translation
        final_translation = flashcardcreator.userinput.ask_user_for_translation(
            self._root_word, translated_word_original)
        if not final_translation:
            logger.info("Exiting because no translation was provided")
            return False

        logger.debug(f'The final translation is {final_translation}')
        self._final_translation = final_translation
        return True


    def create_flashcards_for_linked_words(self):
        """
        If the word is linked to other words, import those words if there aren't any flashcards for them.
        This imports the pairs of perfective and imperfective verbs
        :return: None
        """
        linked_words = self._get_linked_words()
        new_words = [WordFinder.find_word_with_english_translation(word, None)
                     for
                     word in linked_words]
        # Remove all Nones from existing words
        new_words_to_import = [classifiedWord for classifiedWord in new_words
                               if classifiedWord]
        for word_to_import in new_words_to_import:
            word_to_import.linked_word = self._root_word
            word_to_import.create_flashcard()
        for word_to_import in new_words_to_import:
            word_to_import.create_flashcards_for_linked_words()


    def _calculate_derivative_forms(self):
        return calculate_derivative_forms_with_english_field_names(
            self._word_id)


    @abstractmethod
    def _add_row_to_flashcard_database(self, derivative_forms_to_study):
        pass


    def create_flashcard(self):
        """
        If this ClassifiedWord don't have flashcards, creates one or more flashcards.
        If uses the grammatical database and the configuration to decide what are the irregular derivative words which are important to study.

        :return: True if one or more flashcards where created
        :rtype: bool
        """
        if self.exists_flashcard_for_this_word():
            logger.warning(
                f"The word {self._root_word} has already flash cards")
            return False
        elif not self._final_translation:
            logger.warning(
                f"The word {self._root_word} hasn''t got any translations")
            return False

        # If the word is irregular, keep only what is important to study
        all_derivative_forms = self._calculate_derivative_forms()
        derivative_forms_to_study = {}
        if all_derivative_forms:
            derivative_forms_to_keep_config = flashcardcreator.main.config[
                self._speech_part].get(str(self._word_type_id))
            if derivative_forms_to_keep_config:
                derivative_forms_to_keep = derivative_forms_to_keep_config.split(
                    '|')
            else:
                raise ValueError(
                    f'The configuration value for {self._word_type_id} inside {self._speech_part} section is missing. The derivate forms were {all_derivative_forms}')
            derivative_forms_to_study = {key: all_derivative_forms[key] for key
                                         in
                                         derivative_forms_to_keep if
                                         key in all_derivative_forms}
            logger.debug(
                f'The following derivative forms are import to study {derivative_forms_to_study}')

        return self._add_row_to_flashcard_database(derivative_forms_to_study)
        # Add the word to the flashcard database


    def __str__(self):
        return f"Word ID: {self.word_id}\n" \
               f"Root Word: {self.root_word}\n" \
               f"Word Type ID: {self.word_type_id}\n" \
               f"Speech Part: {self.speech_part}"


    def _get_linked_words(self):
        """
        Returns all the words surrounded by double brackets
        :return: List of words or empty list
        """
        if not self._meaning:
            return []
        matches = re.findall(r'\[\[([^\[\]]+)\]\]', self._meaning)
        logger.debug(
            f"Extract the linked words {matches} from the meaning {self._meaning}")
        return matches


class Noun(AbstractClassifiedWord):

    def _calculate_noun_gender(self):
        match self._speech_part:
            case 'noun_female':
                return 'f'
            case 'noun_neutral':
                return 'n'
            case 'noun_male':
                return 'm'
            case _:
                raise ValueError(
                    f'Unable to get the gender for the speech part {self._speech_part}')


    def _add_row_to_flashcard_database(self, derivative_forms_to_study):
        noun_fields = {
            'noun': self._root_word,
            'meaningInEnglish': self._final_translation,
            'genderAbrev': self._calculate_noun_gender(),
            'irregularPluralEnding': None,
            'irregularDefiniteArticle': None,
            'countableEnding': None,
            'irregularPluralWithArticle': None,
            'countableEnding': None,
            'externalWordId': self._word_id
        }
        if 'singular_definite' in derivative_forms_to_study:
            noun_fields['irregularDefiniteArticle'] = \
                derivative_forms_to_study[
                    'singular_definite']
        if 'plural_indefinite' in derivative_forms_to_study:
            noun_fields['irregularPluralEnding'] = derivative_forms_to_study[
                'plural_indefinite']
        if 'plural_definite' in derivative_forms_to_study:
            noun_fields['irregularPluralWithArticle'] = \
                derivative_forms_to_study[
                    'plural_definite']
        if 'contable' in derivative_forms_to_study:
            noun_fields['countableEnding'] = derivative_forms_to_study[
                'contable']
        insert_noun(flashcard_database, noun_fields)
        return True


class Adjective(AbstractClassifiedWord):

    def _add_row_to_flashcard_database(self, derivative_forms_to_study):
        adjective_fields = {
            'masculineForm': self._root_word,
            'meaningInEnglish': self._final_translation,
            'femenineForm': None,
            'neutralForm': None,
            'pluralForm': None,
            'masculine_definite': None,
            'externalWordId': self._word_id
        }
        if 'femenineForm' in derivative_forms_to_study:
            adjective_fields['femenineForm'] = \
                derivative_forms_to_study[
                    'femenineForm']
        if 'neutralForm' in derivative_forms_to_study:
            adjective_fields['neutralForm'] = \
                derivative_forms_to_study[
                    'neutralForm']
        if 'pluralForm' in derivative_forms_to_study:
            adjective_fields['pluralForm'] = \
                derivative_forms_to_study[
                    'pluralForm']
        if 'masculine_definite' in derivative_forms_to_study:
            adjective_fields['masculine_definite'] = \
                derivative_forms_to_study[
                    'masculine_definite']
        insert_adjective(flashcard_database, adjective_fields)
        return True


class Verb(AbstractClassifiedWord):
    """
    Represents verbs
    """


    def _add_row_to_flashcard_database(self, derivative_forms_to_study):
        _insert_verb(flashcard_database, derivative_forms_to_study,
                     self._root_word, self._final_translation,
                     self._word_id, self._is_terminative(), self.linked_word)


    def _calculate_derivative_forms(self):
        return calculate_derivative_forms_from_verb(self._word_id)


    def _is_terminative(self):
        """
        Returns is this verb, глагол, is of typ "свършен вид"
        :return: True if is of typ "свършен вид"
        """
        match self._speech_part:
            case 'verb_intransitive_imperfective' | 'verb_transitive_imperfective' | 'verb':
                return False
            case 'verb_intransitive_terminative' | 'verb_transitive_terminative':
                return True
            case _:
                raise ValueError(
                    f'The verb {self._root_word} has the speech part {self._speech_part} and it is unclear if it is a terminative verb')


class WordWithoutDerivativeForms(AbstractClassifiedWord):
    """
    Represents adverbs, expressions and idioms
    """


    def _add_row_to_flashcard_database(self, derivative_forms_to_study):
        word_fields = {
            'word': self._root_word,
            'meaningInEnglish': self._final_translation,
            'type': self._speech_part,
            'externalWordId': self._word_id
        }
        insert_other_word_type(flashcard_database, word_fields)
        return True


    def _calculate_derivative_forms(self):
        return {}


def first_cyrillic_letter_upper_case(word_without_accents):
    """
    Converts the first Cyrillic letter to upper case.
    When the user enters a name of a person, city, capital or country, the first letter must be in
    upper case and SQLite's lower() function don't support cyrillic characters.

    :param word_without_accents: Word without any accents
    :return: The word with the first character in upper case.
    """
    first_char = word_without_accents[0:1]
    for lowercase, uppercase in CYRILLIC_LETTERS_LOWER_UPPER_CASE_PAIRS:
        if lowercase == first_char:
            return uppercase + word_without_accents[1:]
    return word_without_accents


class WordFinder:

    @staticmethod
    def _remove_accents(input_str):
        """
        Removes all accents or characters which are using two unicode characters. This normalizes the words to search.
        :return: Normalized string without accent characters
        """
        # Decompose all unicode characters in the original one and the accent
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        # We keep the long i as one single unicode character
        nfkd_form = nfkd_form.replace('й', 'й')
        return ''.join(
            [c for c in nfkd_form if
             c != '`' and not unicodedata.combining(c)])


    @staticmethod
    def _trim_lower_case_remove_accents(input_word: str):
        return WordFinder._remove_accents(input_word.strip().lower())


    @staticmethod
    def _find_word(word_to_search: str, other_word_type):
        """
        Normalizes the given word and searches for its word type and derivation rules. Ask
        the user to confirm the translation in English
        If multiple words are found, the user will be prompted to choose one.
        :param other_word_type: Type of the word if it isn't found in the grammar dictionary
        :return:
        :rtype: None or a AbstractClassifiedWord
        """
        # Find what type of word is it together with its writing rules
        word_without_accents = WordFinder._trim_lower_case_remove_accents(
            word_to_search)
        word_like_a_name = first_cyrillic_letter_upper_case(
            word_without_accents)
        search_params = {
            'word_to_search': word_without_accents,
            'word_to_search_like_name': word_like_a_name}
        found_classified_words = flashcardcreator.database.return_rows_of_sql_statement(
            GRAMMATICAL_DATABASE_LOCAL_FILENAME, '''
                SELECT DISTINCT w.id, w.name, w.type_id, wt.speech_part, w.meaning
                FROM derivative_form as df
                    join word as w
                    on w.id = df.base_word_id
                    join word_type as wt
                    on w.type_id = wt.id
                where df.name in (:word_to_search, :word_to_search_like_name)
            UNION 
                SELECT DISTINCT w.id, w.name, w.type_id, wt.speech_part, w.meaning
                FROM word as w
                    join word_type as wt
                    on w.type_id = wt.id
                WHERE w.name in (:word_to_search, :word_to_search_like_name)
                AND NOT EXISTS (SELECT 1 FROM derivative_form as df WHERE df.base_word_id = w.id);
        ''', search_params)

        if not found_classified_words:
            if other_word_type is not None:
                return WordFinder._create_classified_word_subclass(
                    None, word_to_search, None, other_word_type, None)
            else:
                logger.warning(
                    f'The word {word_to_search} is unknown. Exiting')
                return None
        elif len(found_classified_words) > 1:
            found_classified_word = flashcardcreator.userinput.ask_user_to_choose_a_row(
                found_classified_words)
            if found_classified_word is None:
                logger.warning('The user wants to exit')
                return None
        else:
            found_classified_word = found_classified_words[0]

        word_id, root_word, word_type_id, speech_part, word_meaning = found_classified_word
        return WordFinder._create_classified_word_subclass(
            word_id, root_word, word_type_id, speech_part, word_meaning)


    @staticmethod
    def find_word_with_english_translation(word_to_search: str,
                                           other_word_type,
                                           user_translation: str = None) -> AbstractClassifiedWord:
        """
        Normalizes the given word and searches for its word type and derivation rules. Ask
        the user to confirm the translation in English
        If multiple words are found, the user will be prompted to choose one.
        :param word_to_search: Word to search for. It will be converted to the case required by the grammar dictionary
        :param other_word_type: Type of the word if it isn't found in the grammar dictionary
        :param user_translation: Optional. Translation given by the user
        :return:
        :rtype: None or a AbstractClassifiedWord
        """
        word = WordFinder._find_word(word_to_search, other_word_type)
        if word is None and word_to_search.endswith(' се'):
            word = WordFinder._find_word(word_to_search[:-3], other_word_type)
        if word is None or word.exists_flashcard_for_this_word():
            return None

        if user_translation:
            word._final_translation = user_translation
        elif not word.ask_user_for_final_translation():
            return None
        return word


    @staticmethod
    def _create_classified_word_subclass(word_id, root_word, word_type_id,
                                         speech_part, word_meaning):
        """"
        Factory method which creates an instance of the subclasses of ClassifiedWord based on the given fields.
        :rtype A subclass of ClassifiedWord
        """
        logger.debug(
            f'The word {root_word} with {word_id} is classified as {speech_part}')
        match speech_part:
            case 'noun_female' | 'noun_male' | 'noun_neutral':
                return Noun(word_id, root_word, word_meaning, word_type_id,
                            speech_part)
            case 'adjective' | 'pronominal_general' | 'numeral_ordinal':
                return Adjective(word_id, root_word, word_meaning,
                                 word_type_id, speech_part)
            case \
                'adverb' | 'name_capital' | 'name_country' | 'name_city' | 'name_popular' \
                | 'name_various' | 'name_bg-various' | 'name_bg-place' | 'abbreviation' \
                | 'conjunction' | 'interjection' | 'other' | 'particle' | 'prefix' | 'suffix' \
                | 'preposition' | 'phrase' | 'noun_plurale-tantum' \
                | 'expression' | 'geographical' | 'idiom' | 'math' | 'numeral' | 'plural':
                return WordWithoutDerivativeForms(word_id, root_word,
                                                  word_meaning,
                                                  word_type_id, speech_part)
            case 'verb_intransitive_imperfective' | 'verb_intransitive_terminative' | 'verb_transitive_imperfective' | 'verb_transitive_terminative' | 'verb':
                return Verb(word_id, root_word, word_meaning,
                            word_type_id, speech_part)
            case 'pronominal_possessive' | 'pronominal_personal' | 'pronominal_interrogative':
                logger.warning(
                    f'The word {root_word} has already flashcards and won''t be imported')
                return None
            case 'name_people_family' | 'name_people_name' | 'numeral_cardinal' | \
                 'pronominal_demonstrative' | 'pronominal_relative' | \
                 'pronominal_negative' | 'pronominal_indefinite':
                logger.warning(
                    f'The word {root_word} is a {speech_part} and won''t be imported')
                return None
            case _:
                raise ValueError(
                    f"The speech part {speech_part} isn't supported.")


class ParsedLine:
    def __init__(self, original_line, word_or_phrase, translation=None,
                 word_type=None,
                 error=None, is_comment=False):
        self.original_line = original_line
        self.word_or_phrase = word_or_phrase
        self.translation = translation
        self._word_type = word_type
        self.error = error
        self.is_comment = is_comment


    @property
    def word_type(self):
        return self._word_type


    @word_type.setter
    def word_type(self, value):
        if value not in OTHER_WORD_TYPES:
            self.error = f"Invalid word type. Must be one of {OTHER_WORD_TYPES}."
        else:
            self._word_type = value


def parse_line(line: str) -> ParsedLine:
    """
    Parses a line from the input file and returns a ParsedLine instance with
    the word or phrase and optionally an error message, translation and a word type.
    :param line: Mandatory. The line to parse
    :return: ParseLine instance. Never null
    """
    if line.trim().startswith('#') or line.trim() == '':
        return ParsedLine(line, None, None, None, None, True)

    translation = None
    word_type = None
    parts = line.split('=')
    if len(parts) == 3:
        word_or_phrase, translation, word_type = parts
    elif len(parts) == 2:
        word_or_phrase, translation = parts
    elif len(parts) == 1:
        word_or_phrase = parts[0]
    else:
        raise ValueError(f"Invalid line format in line: {line}")

    # Validate the line
    if re.search('[A-Za-z]', word_or_phrase):
        error = f"The word or phrase '{word_or_phrase}' contains Latin characters"
    elif word_type is None:
        # Count the number of words in the phrase without the particle "се"
        words = word_or_phrase.split(' ')
        if len(words) > 1 and words[-1] == 'се':
            words = words[:-1]
        if len(words) > 1 and words[0] == 'се':
            words = words[1:]
        logger.debug(f"Found words in the line {words}")
        if len(words) > 1:
            word_type = EXPRESSION_WORD_TYPE

    return ParsedLine(line, word_or_phrase.trim(), translation.trim(),
                      word_type, error)


def load_logging_configuration(debug=False, verbose=False):
    if debug:
        logging_level = logging.DEBUG
        global main_debug
        main_debug = True
    elif verbose:
        logging_level = logging.INFO
    else:
        logging_level = logging.WARNING
    with open('conf/logging.yaml', 'r') as logging_config:
        config_yaml = yaml.load(logging_config, Loader=yaml.FullLoader)
        logging.config.dictConfig(config_yaml)
    logger.setLevel(logging_level)
    logger.debug(f"The global logging level was set to {logging_level}")


def set_flashcard_database(database_file):
    global flashcard_database
    flashcard_database = database_file
