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

# It implements calls to the PONs dictionary API
import logging
import urllib.request
import urllib.parse
from urllib.parse import urlencode
import json

_DEFAULT_SERVER_URL = 'https://api.pons.com/v1/dictionary'
_DEFAULT_LANGUAGE_PAIR = 'bgen'
_DEFAULT_INPUT_LANGUAGE = 'bg'

logger = logging.getLogger(__name__)


def _extract_translations_nodes(node):
    if isinstance(node, list):
        # If it's a list, recursively call the function on each element
        return [item for sublist in map(_extract_translations_nodes, node) for
                item in sublist]
    elif isinstance(node, dict):
        # If it's a dictionary, check if it has the key "translations"
        if "translations" in node:
            return node["translations"]
        # If it doesn't have "translations", recursively call the function on each value
        return _extract_translations_nodes(list(node.values()))
    else:
        # If it's neither a list nor a dictionary, return an empty list
        return []


class OnlineDictionaryException(Exception):
    def __init__(self,
                 message="There was an error while querying the online dictionary",
                 http_status=None):
        self.message = message
        self.http_status = http_status
        super().__init__(self.message)


class OnlineDictionary:

    def __init__(self, api_key, server_url=_DEFAULT_SERVER_URL,
                 language_pair=_DEFAULT_LANGUAGE_PAIR,
                 input_language=_DEFAULT_INPUT_LANGUAGE,
                 include_examples=False) -> None:
        super().__init__()
        self._api_key = api_key
        self._server_url = server_url
        self._language_pair = language_pair
        self._input_language = input_language
        self._include_examples = include_examples


    def get_full_response_from(self, word_or_phrase: str):
        """
        Returns one or multiple hits with all the translations for the given word or phrase.

        :param word_or_phrase: String to translate
        :return: Translations and examples
        """
        headers = {
            "X-Secret": self._api_key
        }
        if self._include_examples:
            fm_parameter = 1
        else:
            fm_parameter = 0

        final_params = {
            'l': self._language_pair,
            'in': self._input_language,
            'fm': fm_parameter,
            'q': word_or_phrase
        }
        final_encoded_params = urlencode(final_params, encoding="utf-8")
        final_url = f'{self._server_url}?{final_encoded_params}'
        request = urllib.request.Request(final_url, headers=headers)
        try:
            with urllib.request.urlopen(request) as response:
                if response.getcode() == 200:
                    json_data = json.loads(response.read().decode('utf-8'))
                    logger.debug(f"Response: {json_data}")
                    return json_data
                elif response.getcode() == 204:
                    logger.debug(
                        f"There is no translation for {word_or_phrase}")
                    return None
                else:
                    raise OnlineDictionaryException(
                        http_status=response.getcode(),
                        message=response.read().decode('utf-8'))
        except urllib.error.URLError as e:
            raise OnlineDictionaryException() from e
        except urllib.error.HTTPError as e:
            raise OnlineDictionaryException() from e


    def get_translations_from(self, word_or_phrase: str):
        """
        Returns all the translations including the target and source words.

        :param word_or_phrase: To be translated
        :return: None or a list of nodes containing the translations
        """
        full_response = self.get_full_response_from(word_or_phrase)
        if not isinstance(full_response, list):
            return None
        return _extract_translations_nodes(full_response)


    def get_target_single_word_translations_from(self, word_or_phrase: str):
        """
        Returns all the translations in the target language which are single words. PONSs also returns translations of meanings which include many words.

        :param word_or_phrase: To be translated
        :return: None or a set of strings
        """
        translations = self.get_translations_from(word_or_phrase)
        if translations is None:
            return None
        simple_translations = sorted(set([translation['target'] for
                                          translation in translations if
                                          ' ' not in translation['target']]))
        logger.debug(
            f"Simple translations found for '{word_or_phrase}': {simple_translations}")
        if simple_translations:
            return simple_translations
        translations_with_many_words = sorted(set([translation['target'] for
                                                   translation in translations
                                                   if
                                                   'headword' in translation[
                                                       'source']]))
        logger.debug(
            f"Translations with many words found for '{word_or_phrase}': {translations_with_many_words}")
        return translations_with_many_words


    def __str__(self):
        return f"Server URL: {self._server_url}\n" \
               f"Is API Key not null?: {not self._api_key}\n" \
               f"Language Pair: {self._language_pair}\n" \
               f"Input Language: {self._input_language}\n" \
               f"Include Examples: {self._include_examples}"
