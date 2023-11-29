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


class TestDerivativeFormsGeneration(unittest.TestCase):
    def test_regular_female_noun(self):
        self.assertEqual({'plural_definite': 'масите',
                          'plural_indefinite': 'маси',
                          'singular_definite': 'масата',
                          'singular_indefinite': 'маса'},
                         calculate_derivative_forms_with_english_field_names(
                             17599))


    def test_regular_neutral_noun(self):
        self.assertEqual({'plural_definite': 'вниманията',
                          'plural_indefinite': 'внимания',
                          'singular_definite': 'вниманието',
                          'singular_indefinite': 'внимание'},
                         calculate_derivative_forms_with_english_field_names(
                             78270))


    def test_regular_noun_with_irregular_plural(self):
        self.assertEqual(
            {'contable': 'гола',
             'plural_definite': 'головете',
             'plural_indefinite': 'голове',
             'singular_definite': 'голът',
             'singular_indefinite': 'гол'},
            calculate_derivative_forms_with_english_field_names(241))


    def test_noun_with_multiple_replacements(self):
        self.assertEqual(
            {'contable': 'певци',
             'plural_definite': 'певците',
             'plural_indefinite': 'певци',
             'singular_definite': 'певецът',
             'singular_indefinite': 'певец'},
            calculate_derivative_forms_with_english_field_names(70670))


if __name__ == '__main__':
    unittest.main()
