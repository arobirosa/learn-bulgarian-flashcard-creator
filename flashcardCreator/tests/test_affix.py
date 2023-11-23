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
from flashcardcreator.affix import _calculate_all_derivative_forms


class TestDerivativeFormsGeneration(unittest.TestCase):
    def test_regular_noun(self):
        self.assertEqual(['маса', 'масата', 'маси', 'масите'],
                         _calculate_all_derivative_forms('маса', 'а, [^аъиеоуяю]а\nа\nата\nи\nите\n-\n'))

    def test_regular_noun_with_irregular_plural(self):
        self.assertEqual(['гол', 'гола', 'голът', 'голове', 'головете', 'гола'],
                         _calculate_all_derivative_forms('гол', '0, [^аъиеоуяю]\n0\nа\nът\nове\nовете\nа\n-\n'))

    def test_noun_with_multiple_replacements(self):
        self.assertEqual(['певец', 'певеца', 'певецът', 'певеци', 'певеците', 'певеца', 'певецо'],
                         _calculate_all_derivative_forms('певец', 'е[ц]\nе?\nе?а\nе?ът\n?и\n?ите\nе?а\nо\n'))


if __name__ == '__main__':
    unittest.main()
