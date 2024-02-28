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
import unittest
import flashcardcreator.translator

class TestDeepLTranslator(unittest.TestCase):
    def setUp(self) -> None:
        self._free_translator = flashcardcreator.translator.free_translator

    def _return_one_translate_sentence(self, word):
        result = self._free_translator.translate_text(
            word,
            source_lang='BG',
            target_lang='EN-GB')
        return result.text

    def test_translation_of_expression(self):
        self.assertEqual(self._return_one_translate_sentence('нищо подобно'), 'nothing like')


if __name__ == '__main__':
    unittest.main()
