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
from flashcardcreator.main import first_cyrillic_letter_upper_case, ParsedLine, \
    parse_line
from flashcardcreator.util import OTHER_WORD_TYPES


class TestConvertingSearchWordToAName(unittest.TestCase):
    def test_first_cyrillic_letter_upper_case(self):
        self.assertEqual(first_cyrillic_letter_upper_case('софия'), 'София')
        self.assertEqual(first_cyrillic_letter_upper_case('москва'), 'Москва')
        self.assertEqual(first_cyrillic_letter_upper_case('париж'), 'Париж')
        self.assertEqual(first_cyrillic_letter_upper_case('белград'),
                         'Белград')


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
        self.assertEqual(first_cyrillic_letter_upper_case('Белград'),
                         'Белград')


class TestParsedLineClass(unittest.TestCase):
    def setUp(self):
        self.parsed_line = ParsedLine("original line", "word", "translation",
                                      "word_type", "error", False)


    def test_word_type_setter_valid_word_type(self):
        self.parsed_line.word_type = "expression"
        self.assertEqual(self.parsed_line.word_type, "expression")


    def test_word_type_setter_invalid_word_type(self):
        self.parsed_line.word_type = "invalid_word_type"
        self.assertEqual(self.parsed_line.error,
                         f"Invalid word type. Must be one of {OTHER_WORD_TYPES}.")


    def test_word_type_setter_none_word_type(self):
        self.parsed_line.word_type = None
        self.assertEqual(self.parsed_line.error,
                         f"Invalid word type. Must be one of {OTHER_WORD_TYPES}.")


    def test_word_type_setter_empty_word_type(self):
        self.parsed_line.word_type = ""
        self.assertEqual(self.parsed_line.error,
                         f"Invalid word type. Must be one of {OTHER_WORD_TYPES}.")


class TestParseLineMethod(unittest.TestCase):
    def setUp(self):
        self.test_line_comment = "# This is a comment"
        self.test_line_comment_with_spaces = "   # This is a comment"
        self.test_line_empty = ""
        self.test_line_word_translation = "слово = word"
        self.test_line_word_translation_type = "слово = word = noun"
        self.test_line_invalid_format = "слово = word = noun = extra"
        self.test_line_latin_characters = "word = слово"


    def test_parse_line_handles_comment(self):
        parsed_line = parse_line(self.test_line_comment)
        self.assertTrue(parsed_line.is_comment)


    def test_parse_line_handles_comment_with_spaces(self):
        parsed_line = parse_line(self.test_line_comment_with_spaces)
        self.assertTrue(parsed_line.is_comment)


    def test_parse_line_handles_empty_line(self):
        parsed_line = parse_line(self.test_line_empty)
        self.assertTrue(parsed_line.is_comment)


    def test_parse_line_handles_word_translation(self):
        parsed_line = parse_line(self.test_line_word_translation)
        self.assertEqual(parsed_line.word_or_phrase, "слово")
        self.assertEqual(parsed_line.translation, "word")
        self.assertIsNone(parsed_line.word_type)
        self.assertIsNone(parsed_line.error)


    def test_parse_line_handles_word_translation_type(self):
        parsed_line = parse_line(self.test_line_word_translation_type)
        self.assertEqual(parsed_line.word_or_phrase, "слово")
        self.assertEqual(parsed_line.translation, "word")
        self.assertEqual(parsed_line.word_type, "noun")
        self.assertIsNone(parsed_line.error)


    def test_parse_line_handles_invalid_format(self):
        with self.assertRaises(ValueError):
            parse_line(self.test_line_invalid_format)


    def test_parse_line_handles_latin_characters(self):
        parsed_line = parse_line(self.test_line_latin_characters)
        self.assertIsNotNone(parsed_line.error)


if __name__ == '__main__':
    unittest.main()
