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

# Contains the main classes
import logging
from abc import ABC, abstractmethod
from flashcardcreator.database import insert_noun, insert_adjective, \
    insert_other_word_type, \
    return_rows_of_sql_statement, GRAMMATICAL_DATABASE_LOCAL_FILENAME
from flashcardcreator.translator import translate_text_to_english
import flashcardcreator.userinput
import configparser
from flashcardcreator.affix import \
    calculate_derivative_forms_with_english_field_names
import unicodedata
import yaml

CONFIG_FILENAME = 'configuration.ini'

logger = logging.getLogger(__name__)
# Location of the flashcard which can be given by the user
flashcard_database = None
main_debug = False
config = configparser.ConfigParser(interpolation=None)
config.read(CONFIG_FILENAME)


class AbstractClassifiedWord(ABC):
    def __init__(self, word_id, root_word, word_type_id, speech_part):
        self._word_id = word_id
        self._root_word = root_word
        self._word_type_id = word_type_id
        self._speech_part = speech_part
        self._final_translation = None


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
                    ',')
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
        insert_adjective(flashcard_database, adjective_fields)
        return True


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
            [c for c in nfkd_form if not unicodedata.combining(c)])


    @staticmethod
    def _trim_lower_case_remove_accents(input_word: str):
        return WordFinder._remove_accents(input_word.strip().lower())


    @staticmethod
    def _find_word(word_to_search: str):
        """
        Normalizes the given word and searches for its word type and derivation rules. Ask
        the user to confirm the translation in English
        If multiple words are found, the user will be prompted to choose one.
        :return:
        :rtype: None or a AbstractClassifiedWord
        """
        # Find what type of word is it together with its writing rules
        search_params = {
            'word_to_search': WordFinder._trim_lower_case_remove_accents(
                word_to_search)}
        found_classified_words = flashcardcreator.database.return_rows_of_sql_statement(
            GRAMMATICAL_DATABASE_LOCAL_FILENAME, '''
                SELECT DISTINCT w.id, w.name, w.type_id, wt.speech_part
                FROM derivative_form as df
                    join word as w
                    on w.id = df.base_word_id
                    join word_type as wt
                    on w.type_id = wt.id
                where df.name = :word_to_search
            UNION 
                SELECT DISTINCT w.id, w.name, w.type_id, wt.speech_part
                FROM word as w
                    join word_type as wt
                    on w.type_id = wt.id
                WHERE w.name = :word_to_search
                AND NOT EXISTS (SELECT 1 FROM derivative_form as df WHERE df.base_word_id = w.id);
        ''', search_params)

        if not found_classified_words:
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

        return WordFinder._create_classified_word_subclass(
            found_classified_word)


    @staticmethod
    def find_word_with_english_translation(word_to_search: str):
        """
        Normalizes the given word and searches for its word type and derivation rules. Ask
        the user to confirm the translation in English
        If multiple words are found, the user will be prompted to choose one.
        :return:
        :rtype: None or a AbstractClassifiedWord
        """
        word = WordFinder._find_word(word_to_search)
        if word is None or word.exists_flashcard_for_this_word():
            return None
        if not word.ask_user_for_final_translation():
            return None
        return word


    @staticmethod
    def _create_classified_word_subclass(found_classified_word):
        """"
        Factory method which creates an instance of the subclasses of ClassifiedWord based on the given fields.
        :rtype A subclass of ClassifiedWord
        """
        logger.debug(
            f'The word {found_classified_word[1]} is classified as {found_classified_word}')
        word_id, root_word, word_type_id, speech_part = found_classified_word
        match speech_part:
            case 'noun_female' | 'noun_male' | 'noun_neutral':
                return Noun(word_id, root_word, word_type_id, speech_part)
            case 'adjective':
                return Adjective(word_id, root_word, word_type_id, speech_part)
            case 'adverb':
                return WordWithoutDerivativeForms(word_id, root_word,
                                                  word_type_id, speech_part)
            case _:
                raise ValueError(
                    f"The speech part {speech_part} isn't supported.")


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
