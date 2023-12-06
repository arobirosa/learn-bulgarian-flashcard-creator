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

# Methods to access the database

import sqlite3
import logging
from flashcardcreator.util import convert_to_absolute_path

logger = logging.getLogger(__name__)


def return_rows_of_sql_statement(database_file, sql_statement: str,
                                 params):
    with sqlite3.connect(database_file) as db_connection:
        db_cursor = db_connection.cursor()
        db_cursor.execute(sql_statement, params)
        return db_cursor.fetchall()


def insert_noun(database_file, noun_fields):
    logger.info(
        f'Adding a flashcard for the noun with the fields: {noun_fields}')
    with sqlite3.connect(database_file) as db_connection:
        db_cursor = db_connection.cursor()
        db_cursor.execute('''
        insert into nouns (noun, meaningInEnglish, genderAbrev, irregularPluralEnding, irregularDefiniteArticle,
                   countableEnding, irregularPluralWithArticle,
                   externalWordId)
        values (:noun, :meaningInEnglish, :genderAbrev, :irregularPluralEnding, :irregularDefiniteArticle,
                   :countableEnding, :irregularPluralWithArticle,
                   :externalWordId);
        ''', noun_fields)
        db_connection.commit()
        logger.info(
            f'The noun {noun_fields["noun"]} was added to the flashcard database')


def insert_adjective(database_file, adjective_fields):
    logger.info(
        f'Adding a flashcard for the adjective with the fields: {adjective_fields}')
    with sqlite3.connect(database_file) as db_connection:
        db_cursor = db_connection.cursor()
        db_cursor.execute('''
        insert into adjetives (masculineForm, meaningInEnglish, femenineForm, neutralForm, pluralForm, externalWordId)
        values (:masculineForm, :meaningInEnglish, :femenineForm, :neutralForm, :pluralForm, :externalWordId);
        ''', adjective_fields)
        db_connection.commit()
        logger.info(
            f'The adjective {adjective_fields["masculineForm"]} was added to the flashcard database')


def insert_verb_meaning_with_cursor(db_cursor, meaning_in_english,
                                    external_word_id,
                                    present_singular1):
    logger.info(
        f'Adding a flashcard for the verb meaning with the presentSingular1 fields: {present_singular1}')
    db_cursor.execute('''
    insert into verbMeanings (meaningInEnglish, externalWordId, presentSingular1)
    values (?, ?, ?);
    ''', (meaning_in_english, external_word_id, present_singular1))
    logger.info(
        f'The meaning of the verb meaning {present_singular1} was added to the flashcard database')


def insert_other_word_type_with_cursor(db_cursor, word_fields):
    db_cursor.execute('''
        insert into otherWordTypes (word, meaningInEnglish, type, externalWordId)
        values (:word, :meaningInEnglish, :type, :externalWordId);
        ''', word_fields)


def insert_participles_with_cursor(db_cursor, verb_participles,
                                   final_translation, word_id):
    for participle_name, derivative_form in verb_participles.items():
        word_fields = {
            'word': derivative_form,
            'meaningInEnglish': final_translation,
            'type': participle_name,
            'externalWordId': word_id
        }
        insert_other_word_type_with_cursor(db_cursor, word_fields)


def insert_verb_tense_with_cursor(db_cursor, present_singular1, tense,
                                  imperfect,
                                  singular1, singular2, plural3, plural2=None):
    logger.info(
        f'Adding a flashcard for the verb tense {tense} with the presentSingular1 fields: {present_singular1}')
    db_cursor.execute('''
    insert into verbs4 (presentSingular1, tense, imperfect, singular1, singular2, plural2, plural3)
    values (?, ?, ?, ?, ?, ?, ?);
            ''', (
        present_singular1, tense, imperfect, singular1, singular2,
        plural2, plural3))
    logger.info(
        f'The tense {tense} of the verb {present_singular1} was added to the flashcard database')


def insert_other_word_type(database_file, word_fields):
    logger.info(
        f'Adding a flashcard for the other word with the fields: {word_fields}')
    with sqlite3.connect(database_file) as db_connection:
        db_cursor = db_connection.cursor()
        insert_other_word_type_with_cursor(db_cursor, word_fields)
        db_connection.commit()
        logger.info(
            f'The word {word_fields["word"]} was added to the flashcard database')


def verb_pair_not_exists(db_cursor, terminative_verb, imperfective_verb):
    """
    Returns if the given verb pair already exists.
    The transaction management must be done by the calller.

    :param db_cursor: Required. Open cursor.
    :param terminative_verb: Required. Verb's root word
    :param imperfective_verb: Required.  Verb's root word
    :return: True or False
    """
    db_cursor.execute('''
        SELECT 1
        FROM verbsPairs
        WHERE terminativeVerb = ?
        AND imperfectVerb = ?;
    ''', (terminative_verb, imperfective_verb))
    return db_cursor.fetchone() is None


def verb_pair_insert(db_cursor, terminative_verb, imperfective_verb):
    logger.info(
        f'Adding a verb pair with terminative verb {terminative_verb} and imperfective verb {imperfective_verb}')
    db_cursor.execute('''
        insert into verbsPairs (terminativeVerb, imperfectVerb)
        values (?, ?);
                ''', (terminative_verb, imperfective_verb))
    logger.info('The verb pair was added to the flashcard database')


GRAMMATICAL_DATABASE_LOCAL_FILENAME = convert_to_absolute_path(
    'data/grammatical_dictionary.db')
