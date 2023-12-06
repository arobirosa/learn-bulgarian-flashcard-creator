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


/** word_types with irregularities except for the verb tenses

      # Сегашно време
    'сег.вр., 1л., ед.ч.',
    'сег.вр., 2л., ед.ч.',
    'сег.вр., 3л., мн.ч.',  # Some "я" mutate to "е" or "а" like ям
    # Минало свършено време (аорист)
    'мин.св.вр., 1л., ед.ч.',
    'мин.св.вр., 2л., ед.ч.',
    # Минало несвършено време (имперфект)
    'мин.несв.вр., 1л., ед.ч.',
    'мин.несв.вр., 2л., ед.ч.',
 */

select word_from_word_type.speech_part, word_from_word_type.id word_type_id, w2.name,
       df.name "повелително наклонение, ед.ч.", df2.name "повелително наклонение, мн.ч."
from (select wt.speech_part, wt.id, min(w.id) word_id_max
      from word_type wt
               join word w on wt.id = w.type_id
      where speech_part = 'verb_intransitive_terminative'
      group by wt.speech_part, wt.id) word_from_word_type
join word w2
    on word_from_word_type.word_id_max = w2.id
join derivative_form df
    on w2.id = df.base_word_id
    and df.description = 'повелително наклонение, ед.ч.'
join derivative_form df2
     on w2.id = df2.base_word_id
         and df2.description = 'повелително наклонение, мн.ч.'
where substr(w2.name, 0, length(w2.name)) || 'и' <> df.name
and substr(w2.name, 0, length(w2.name)) || 'й' <> df.name
order by word_from_word_type.speech_part, word_from_word_type.id ;


select word_from_word_type.speech_part, word_from_word_type.id word_type_id, w2.name, df.name "мин.св.вр., 2л., ед.ч.",
       df3.name "мин.деят.св.прич. м.р.", df4.name "мин.деят.св.прич. мн.ч.",
       df5.name "мин.деят.несв.прич. м.р."
from (select wt.speech_part, wt.id, min(w.id) word_id_max
      from word_type wt
               join word w on wt.id = w.type_id
      where speech_part = 'verb_intransitive_terminative'
      group by wt.speech_part, wt.id) word_from_word_type
         join word w2
              on word_from_word_type.word_id_max = w2.id
         join derivative_form df
              on w2.id = df.base_word_id
                  and df.description = 'мин.св.вр., 2л., ед.ч.'
         join derivative_form df3
              on w2.id = df3.base_word_id
                  and df3.description = 'мин.деят.св.прич. м.р.'
         join derivative_form df4
              on w2.id = df4.base_word_id
                  and df4.description = 'мин.деят.св.прич. мн.ч.'
         join derivative_form df5
              on w2.id = df5.base_word_id
                  and df5.description = 'мин.деят.несв.прич. м.р.'
where df.name || 'л' <> df3.name
   or df.name || 'ли' <> df4.name
order by word_from_word_type.speech_part, word_from_word_type.id ;
