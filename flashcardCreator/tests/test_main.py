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
from flashcardcreator.affix import \
    calculate_derivative_forms_with_english_field_names
from flashcardcreator.main import first_cyrillic_letter_upper_case


class TestCovertingSearchWordToAName(unittest.TestCase):
    def test_first_cyrillic_letter_upper_case(self):
        self.assertEqual(first_cyrillic_letter_upper_case('софия'), 'София')
        self.assertEqual(first_cyrillic_letter_upper_case('москва'), 'Москва')
        self.assertEqual(first_cyrillic_letter_upper_case('париж'), 'Париж')
        self.assertEqual(first_cyrillic_letter_upper_case('белград'), 'Белград')

    def test_first_cyrillic_letter_upper_case_no_change(self):
        # Test when the word is empty or doesn't start with a Cyrillic letter
        self.assertEqual(first_cyrillic_letter_upper_case(''), '')
        self.assertEqual(first_cyrillic_letter_upper_case('123'), '123')
        self.assertEqual(first_cyrillic_letter_upper_case('abc'), 'abc')

    def test_first_cyrillic_letter_upper_case_mixed_case(self):
        # Test when the first letter is already uppercase
        self.assertEqual(first_cyrillic_letter_upper_case('София'), 'София')
        self.assertEqual(first_cyrillic_letter_upper_case('Москва'), 'Москва')
        self.assertEqual(first_cyrillic_letter_upper_case('Париж'), 'Париж')
        self.assertEqual(first_cyrillic_letter_upper_case('Белград'), 'Белград')


if __name__ == '__main__':
    unittest.main()
