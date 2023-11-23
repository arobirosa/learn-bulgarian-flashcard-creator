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
