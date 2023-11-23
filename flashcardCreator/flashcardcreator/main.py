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
from flashcardcreator.database import insert_noun, \
    return_rows_of_sql_statement
from flashcardcreator.translator import translate_text_to_english
import flashcardcreator.userinput
import unicodedata
import yaml

GRAMMATICAL_DATABASE_LOCAL_FILENAME = 'data/grammatical_dictionary.db'
logger = logging.getLogger(__name__)
# Location of the flashcard which can be given by the user
flashcard_database = None
main_debug = False


class AbstractClassifiedWord(ABC):
    def __init__(self, word_id, root_word, word_type_id, speech_part,
                 word_type_rules, word_type_rules_test,
                 word_type_example_word):
        self._word_id = word_id
        self._root_word = root_word
        self._word_type_id = word_type_id
        self._speech_part = speech_part
        self._word_type_rules = word_type_rules
        self._word_type_rules_test = word_type_rules_test
        self._word_type_example_word = word_type_example_word
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
        # Find an automatic translation in English for the word
        translated_word_original = translate_text_to_english(root_word,
                                                             debug_client_calls=__name__.main_debug)

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


    @abstractmethod
    def insert_into_flashcard_database(self):
        pass


    def __str__(self):
        return f"Word ID: {self.word_id}\n" \
               f"Root Word: {self.root_word}\n" \
               f"Word Type ID: {self.word_type_id}\n" \
               f"Speech Part: {self.speech_part}\n" \
               f"Word Type Rules: {self.word_type_rules}\n" \
               f"Word Type Rules Test: {self.word_type_rules_test}\n" \
               f"Word Type Example Word: {self.word_type_example_word}"


class Noun(AbstractClassifiedWord):
    def __init__(self, word_id, root_word, word_type_id, speech_part,
                 word_type_rules, word_type_rules_test,
                 word_type_example_word):
        super().__init__(word_id, root_word, word_type_id, speech_part,
                         word_type_rules, word_type_rules_test,
                         word_type_example_word)

    # def __str__(self):
    #     # Use the __str__ method of the parent class and add information about the additional field
    #     parent_str = super().__str__()
    #     return f"{parent_str}\nAdditional Field: {self.additional_field}"


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
        search_params = {'word_to_search': word_to_search}
        found_classified_words = flashcardcreator.database.return_rows_of_sql_statement(
            GRAMMATICAL_DATABASE_LOCAL_FILENAME, '''
            SELECT w.id, w.name, w.type_id, wt.speech_part, wt.rules, wt.rules_test, wt.example_word
            FROM derivative_form as df
            join word as w
            on w.id = df.base_word_id
            join word_type as wt
            on w.type_id = wt.id
            where df.name = :word_to_search;
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
        if word.exists_flashcard_for_this_word():
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
        word_id, root_word, word_type_id, speech_part, word_type_rules, word_type_rules_test, word_type_example_word = found_classified_word
        match speech_part:
            case 'noun_female', 'noun_male', 'noun_neutral':
                return Noun(word_id, root_word, word_type_id, speech_part,
                            word_type_rules, word_type_rules_test,
                            word_type_example_word)
            case _:
                raise ValueError(
                    f'The speech part {speech_part} isn''t supported.')


def load_logging_configuration(debug=False, verbose=False):
    if debug:
        logging_level = logging.DEBUG
        __name__.main_debug = True
    elif verbose:
        logging_level = logging.INFO
    else:
        logging_level = logging.WARNING
    with open('conf/logging.yaml', 'r') as logging_config:
        config = yaml.load(logging_config, Loader=yaml.FullLoader)
        logging.config.dictConfig(config)
    logger.setLevel(logging_level)
    logger.debug(f"The global logging level was set to {logging_level}")
