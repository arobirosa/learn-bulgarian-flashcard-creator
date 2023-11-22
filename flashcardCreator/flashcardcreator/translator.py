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
import deepl
import configparser

API_KEYS_FILENAME = 'apiKeys.ini'

logger = logging.getLogger(__name__)

def init_function_create_deepl_translator():
    logger.debug("Initialization function has been called.")
    api_keys_config = configparser.ConfigParser(interpolation=None)
    api_keys_config.read(API_KEYS_FILENAME)
    deepl_api_key = api_keys_config[api_keys_config.default_section].get("deepl")
    if not deepl_api_key:
        raise ValueError("DeepL API key is not configured. Please visit https://www.deepl.com/pro-api and get a Free API key")

    return deepl.Translator(auth_key=deepl_api_key, send_platform_info=False).set_app_info("Flashcard "
                                                                                                      "Creator", '0.0.1')


# The following code will run when the module is imported
free_translator = init_function_create_deepl_translator()


def translate_text_to_english(word_or_phrase_to_translate, debug_client_calls=False):
    if debug_client_calls:
        logging.getLogger('deepl').setLevel(logging.DEBUG)
    else:
        logging.getLogger('deepl').setLevel(logging.WARNING)
    return free_translator.translate_text(word_or_phrase_to_translate, source_lang='BG', target_lang='EN-GB')


