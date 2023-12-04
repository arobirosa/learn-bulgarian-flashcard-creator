/*
 * Copyright (c) 2023 Antonio Robirosa <flashcard.creator@areko.consulting>
 *
 * This file is part of the Bulgarian Flashcard Creator.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 *  (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, see <http://www.gnu.org/licenses/>.
 *
 */

/** Сегашно време **/
select df2s.name singular2, wt.speech_part, df1p.name, df1p.description
from derivative_form df2s
         inner join word w
                    on w.id = df2s.base_word_id
         inner join word_type wt
                    on wt.id = w.type_id
         inner join derivative_form df1p
                    on w.id = df1p.base_word_id
                        and df1p.description = 'сег.вр., 1л., мн.ч.'
                        and df1p.name <> df2s.name /** There are 37 verbs with the 1. singular in all derivative forms**/
                        and df1p.name <> substr(df2s.name, 0, length(df2s.name)) || 'ме'
                        and df1p.name <> substr(df2s.name, 0, length(df2s.name)) || 'м'
where df2s.description = 'сег.вр., 2л., ед.ч.'
union all
select df2s.name singular2, wt.speech_part, df_other.name, df_other.description
from derivative_form df2s
         inner join word w
                    on w.id = df2s.base_word_id
         inner join word_type wt
                    on wt.id = w.type_id
         inner join derivative_form df_other
                    on w.id = df_other.base_word_id
                        and df_other.description = 'сег.вр., 2л., мн.ч.'
                        and
                       df_other.name <> df2s.name /** There are 37 verbs with the 1. singular in all derivative forms**/
                        and df_other.name <> substr(df2s.name, 0, length(df2s.name)) || 'те'
where df2s.description = 'сег.вр., 2л., ед.ч.'

union all
select df2s.name singular2, wt.speech_part, df_other.name, df_other.description
from derivative_form df2s
         inner join word w
                    on w.id = df2s.base_word_id
         inner join word_type wt
                    on wt.id = w.type_id
         inner join derivative_form df_other
                    on w.id = df_other.base_word_id
                        and df_other.description = 'сег.вр., 3л., мн.ч.'
                        and df_other.name <> df2s.name /** There are 37 verbs with the 1. singular in all derivative forms**/
                        and df_other.name <> (df2s.name || 'т')
                        and df_other.name <> substr(df2s.name, 0, length(df2s.name)) || 'т'
where df2s.description = 'сег.вр., 1л., ед.ч.'

union all
select df2s.name singular2, wt.speech_part, df_other.name, df_other.description
from derivative_form df2s
         inner join word w
                    on w.id = df2s.base_word_id
         inner join word_type wt
                    on wt.id = w.type_id
         inner join derivative_form df_other
                    on w.id = df_other.base_word_id
                        and df_other.description = 'сег.вр., 3л., ед.ч.'
                        and
                       df_other.name <> df2s.name /** There are 37 verbs with the 1. singular in all derivative forms**/
                        and df_other.name <> substr(df2s.name, 0, length(df2s.name))
where df2s.description = 'сег.вр., 2л., ед.ч.'

/** Минало свършено време (аорист) **/
union all
select df2s.name singular2, wt.speech_part, df_other.name, df_other.description
from derivative_form df2s
         inner join word w
                    on w.id = df2s.base_word_id
         inner join word_type wt
                    on wt.id = w.type_id
         inner join derivative_form df_other
                    on w.id = df_other.base_word_id
                        and df_other.description = 'мин.св.вр., 3л., ед.ч.'
                        and df_other.name <> df2s.name
where df2s.description = 'мин.св.вр., 2л., ед.ч.'

union all
select df2s.name singular2, wt.speech_part, df_other.name, df_other.description
from derivative_form df2s
         inner join word w
                    on w.id = df2s.base_word_id
         inner join word_type wt
                    on wt.id = w.type_id
         inner join derivative_form df_other
                    on w.id = df_other.base_word_id
                        and df_other.description = 'мин.св.вр., 1л., мн.ч.'
                        and df_other.name <> df2s.name /** There are 37 verbs with the 1. singular in all derivative forms**/
                        and df_other.name <> df2s.name || 'ме'
where df2s.description = 'мин.св.вр., 1л., ед.ч.'

union all
select df2s.name singular2, wt.speech_part, df_other.name, df_other.description
from derivative_form df2s
         inner join word w
                    on w.id = df2s.base_word_id
         inner join word_type wt
                    on wt.id = w.type_id
         inner join derivative_form df_other
                    on w.id = df_other.base_word_id
                        and df_other.description = 'мин.св.вр., 2л., мн.ч.'
                        and df_other.name <> df2s.name /** There are 37 verbs with the 1. singular in all derivative forms**/
                        and df_other.name <> df2s.name || 'те'
where df2s.description = 'мин.св.вр., 1л., ед.ч.'

union all
select df2s.name singular2, wt.speech_part, df_other.name, df_other.description
from derivative_form df2s
         inner join word w
                    on w.id = df2s.base_word_id
         inner join word_type wt
                    on wt.id = w.type_id
         inner join derivative_form df_other
                    on w.id = df_other.base_word_id
                        and df_other.description = 'мин.св.вр., 3л., мн.ч.'
                        and df_other.name <> df2s.name /** There are 37 verbs with the 1. singular in all derivative forms**/
                        and df_other.name <> df2s.name || 'а'
where df2s.description = 'мин.св.вр., 1л., ед.ч.'

/** Минало несвършено време (имперфект) **/
union all
select df2s.name singular2, wt.speech_part, df_other.name, df_other.description
from derivative_form df2s
         inner join word w
                    on w.id = df2s.base_word_id
         inner join word_type wt
                    on wt.id = w.type_id
         inner join derivative_form df_other
                    on w.id = df_other.base_word_id
                        and df_other.description = 'мин.несв.вр., 3л., ед.ч.'
                        and df_other.name <> df2s.name
where df2s.description = 'мин.несв.вр., 2л., ед.ч.'

union all
select df2s.name singular2, wt.speech_part, df_other.name, df_other.description
from derivative_form df2s
         inner join word w
                    on w.id = df2s.base_word_id
         inner join word_type wt
                    on wt.id = w.type_id
         inner join derivative_form df_other
                    on w.id = df_other.base_word_id
                        and df_other.description = 'мин.несв.вр., 1л., мн.ч.'
                        and df_other.name <> df2s.name /** There are 37 verbs with the 1. singular in all derivative forms**/
                        and df_other.name <> df2s.name || 'ме'
where df2s.description = 'мин.несв.вр., 1л., ед.ч.'

union all
select df2s.name singular2, wt.speech_part, df_other.name, df_other.description
from derivative_form df2s
         inner join word w
                    on w.id = df2s.base_word_id
         inner join word_type wt
                    on wt.id = w.type_id
         inner join derivative_form df_other
                    on w.id = df_other.base_word_id
                        and df_other.description = 'мин.несв.вр., 2л., мн.ч.'
                        and df_other.name <> df2s.name /** There are 37 verbs with the 1. singular in all derivative forms**/
                        and df_other.name <> df2s.name || 'те'
where df2s.description = 'мин.несв.вр., 1л., ед.ч.'

union all
select df2s.name singular2, wt.speech_part, df_other.name, df_other.description
from derivative_form df2s
         inner join word w
                    on w.id = df2s.base_word_id
         inner join word_type wt
                    on wt.id = w.type_id
         inner join derivative_form df_other
                    on w.id = df_other.base_word_id
                        and df_other.description = 'мин.несв.вр., 3л., мн.ч.'
                        and df_other.name <> df2s.name /** There are 37 verbs with the 1. singular in all derivative forms**/
                        and df_other.name <> df2s.name || 'а'
where df2s.description = 'мин.несв.вр., 1л., ед.ч.'

/** Причастия (отглаголни прилагателни) **/
union all
select df2s.name singular2, wt.speech_part, df_other.name, df_other.description
from derivative_form df2s
         inner join word w
                    on w.id = df2s.base_word_id
         inner join word_type wt
                    on wt.id = w.type_id
         inner join derivative_form df_other
                    on w.id = df_other.base_word_id
                        and df_other.description = 'сег.деят.прич. м.р. пълен член'
                        and df_other.name <> df2s.name /** There are 37 verbs with the 1. singular in all derivative forms**/
                        and df_other.name <> df2s.name || 'ият'
where df2s.description = 'сег.деят.прич. м.р.'
;
