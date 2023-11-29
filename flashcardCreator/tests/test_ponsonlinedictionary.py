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

from flashcardcreator.translator import online_dictionary


class TestGettingTranslationsFromOnlineDictionary(unittest.TestCase):
    def setUp(self) -> None:
        self.online_dictionary = online_dictionary
        if online_dictionary is None:
            self.fail("The API key for the PONS dictionary is not configured")


    def test_word_with_multiple_meanings(self):
        self.assertEqual(
            set(['side', 'flank', 'face', 'cheek', 'country', 'land',
                 'direction', 'aspect', 'feature', 'point', 'respect', 'party',
                 'contractor', 'intervenor', 'litigant',
                 'advantage/disadvantage',
                 'subscriber',
                 'inside/outside']),
            self.online_dictionary.get_target_single_word_translations_from(
                'страна'))

    def test_word_with_one_meanings(self):
        self.assertEqual(
            set(['sun', 'sunbathe']),
            self.online_dictionary.get_target_single_word_translations_from(
                'слънце'))

    def test_incorrect_word(self):
        self.assertEqual(
            None,
            self.online_dictionary.get_target_single_word_translations_from(
                'слънцетттт'))


if __name__ == '__main__':
    unittest.main()
