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

DEFAULT_SERVER_URL='https://api.pons.com/v1/dictionary'
DEFAULT_LANGUAGE_PAIR='bgen'
DEFAULT_INPUT_LANGUAGE='bg'

logger = logging.getLogger(__name__)


class OnlineDictionary:

    def __init__(self, server_url=DEFAULT_SERVER_URL, language_pair=DEFAULT_LANGUAGE_PAIR, input_language=DEFAULT_INPUT_LANGUAGE, include_examples=False) -> None:
        super().__init__()
        self._server_url= server_url
        self._language_pair= language_pair
        self._input_language= input_language
        self._include_examples= include_examples

    def get_translations_from(self, word_or_phrase : str):
        pass

    def __str__(self):
        return f"Server URL: {self._server_url}\n" \
               f"Language Pair: {self._language_pair}\n" \
               f"Input Language: {self._input_language}\n" \
               f"Include Examples: {self._include_examples}"
