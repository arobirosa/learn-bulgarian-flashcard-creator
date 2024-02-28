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
import unittest.mock

from flashcardcreator.database import insert_participles_with_cursor, \
    SQL_INSERT_OTHER_WORD


class TestInsertParticiplesWithCursor(unittest.TestCase):
    def setUp(self):
        self.db_cursor = unittest.mock.Mock()
        self.verb_participles = {
            'мин.деят.несв.прич. м.р.': 'завалял',
            'мин.деят.св.прич. мн.ч.': 'завалели',
            'мин.деят.св.прич. м.р.': 'завалял'
        }
        self.final_translation = 'final_translation'
        self.word_id = 123

    def test_inserts_unique_participles(self):
        insert_participles_with_cursor(self.db_cursor, self.verb_participles, self.final_translation, self.word_id)
        expected_calls = [
            unittest.mock.call(SQL_INSERT_OTHER_WORD, {
                'word': 'завалял',
                'meaningInEnglish': self.final_translation,
                'type': 'мин.деят.св.прич. м.р., мин.деят.несв.прич. м.р.',
                'externalWordId': self.word_id
            }),
            unittest.mock.call(SQL_INSERT_OTHER_WORD, {
                'word': 'завалели',
                'meaningInEnglish': self.final_translation,
                'type': 'мин.деят.св.прич. мн.ч.',
                'externalWordId': self.word_id
            })
        ]
        self.db_cursor.execute.assert_has_calls(expected_calls, any_order=True)

    def test_inserts_no_participles_when_none_provided(self):
        insert_participles_with_cursor(self.db_cursor, {}, self.final_translation, self.word_id)
        self.db_cursor.execute.assert_not_called()

    def test_inserts_single_participle(self):
        single_verb_participle = {'мин.деят.несв.прич. м.р.': 'завалял'}
        insert_participles_with_cursor(self.db_cursor, single_verb_participle, self.final_translation, self.word_id)
        self.db_cursor.execute.assert_called_once_with(
            SQL_INSERT_OTHER_WORD,
            {
                'word': 'завалял',
                'meaningInEnglish': 'final_translation',
                'type': 'мин.деят.несв.прич. м.р.',
                'externalWordId': 123
            }
        )

if __name__ == '__main__':
    unittest.main()
