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
      where speech_part in ('verb_intransitive_terminative', 'verb_transitive_imperfective', 'verb_intransitive_imperfective')
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
      where speech_part in ('verb_intransitive_terminative', 'verb_transitive_imperfective', 'verb_intransitive_imperfective')
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


select word_from_word_type.speech_part, word_from_word_type.id word_type_id, w2.name,
       df.name "ед.ч. пълен член",
       df3.name "мн.ч.", df4.name "мн.ч. членувано",
       df5.name "бройна форма"
from (select wt.speech_part, wt.id, min(w.id) word_id_max
      from word_type wt
               join word w on wt.id = w.type_id
      where speech_part = 'noun_male'
      group by wt.speech_part, wt.id) word_from_word_type
         join word w2
              on word_from_word_type.word_id_max = w2.id
         join derivative_form df
              on w2.id = df.base_word_id
                  and df.description = 'ед.ч. пълен член'
         join derivative_form df3
              on w2.id = df3.base_word_id
                  and df3.description = 'мн.ч.'
         join derivative_form df4
              on w2.id = df4.base_word_id
                  and df4.description = 'мн.ч. членувано'
         join derivative_form df5
              on w2.id = df5.base_word_id
                  and df5.description = 'бройна форма'
where /*w2.name || 'ът' <> df.name
   or w2.name || 'и' <> df3.name
   or df3.name || 'те' <> df4.name
    or */ w2.name || 'а' <> df5.name
order by word_from_word_type.speech_part, word_from_word_type.id ;

select word_from_word_type.speech_part, word_from_word_type.id word_type_id, w2.name,
       df.name "ед.ч. членувано",
       df3.name "мн.ч.", df4.name "мн.ч. членувано",
       df5.name "звателна форма"
from (select wt.speech_part, wt.id, min(w.id) word_id_max
      from word_type wt
               join word w on wt.id = w.type_id
      where speech_part = 'noun_female'
      group by wt.speech_part, wt.id) word_from_word_type
         join word w2
              on word_from_word_type.word_id_max = w2.id
         left join derivative_form df
              on w2.id = df.base_word_id
                  and df.description = 'ед.ч. членувано'
         left join derivative_form df3
              on w2.id = df3.base_word_id
                  and df3.description = 'мн.ч.'
         left join derivative_form df4
              on w2.id = df4.base_word_id
                  and df4.description = 'мн.ч. членувано'
         left join derivative_form df5
              on w2.id = df5.base_word_id
                  and df5.description = 'звателна форма'
/*where /*w2.name || 'та' <> df.name
   or substr(w2.name,0, length(w2.name)) || 'и' <> df3.name
   and w2.name || 'и' <> df3.name
   or  df3.name || 'те' <> df4.name
     or  w2.name || 'а' <> df5.name*/
order by word_from_word_type.speech_part, word_from_word_type.id ;

select word_from_word_type.speech_part, word_from_word_type.id word_type_id, w2.name,
       df.name "ед.ч. членувано",
       df3.name "мн.ч.", df4.name "мн.ч. членувано"
from (select wt.speech_part, wt.id, min(w.id) word_id_max
      from word_type wt
               join word w on wt.id = w.type_id
      where speech_part = 'noun_neutral'
      group by wt.speech_part, wt.id) word_from_word_type
         join word w2
              on word_from_word_type.word_id_max = w2.id
         left join derivative_form df
                   on w2.id = df.base_word_id
                       and df.description = 'ед.ч. членувано'
         left join derivative_form df3
                   on w2.id = df3.base_word_id
                       and df3.description = 'мн.ч.'
         left join derivative_form df4
                   on w2.id = df4.base_word_id
                       and df4.description = 'мн.ч. членувано'
where /*w2.name || 'то' <> df.name
   or (substr(w2.name,0, length(w2.name)) || 'а' <> df3.name
           and substr(w2.name,0, length(w2.name)) || 'е' <> df3.name)
   or  */ (df3.name || 'те' <> df4.name
        and df3.name || 'та' <> df4.name)
order by word_from_word_type.speech_part, word_from_word_type.id ;

select word_from_word_type.speech_part, word_from_word_type.id word_type_id, w2.name,
       df.name "м.р. непълен член", df2.name "м.р. пълен член",
       df3.name "мн.ч.", df4.name "мн.ч. членувано",
       df5.name "ж.р.", df6.name "ж.р. членувано",
       df7.name "ср.р.", df8.name "ср.р. членувано"
from (select wt.speech_part, wt.id, min(w.id) word_id_max
      from word_type wt
               join word w on wt.id = w.type_id
      where speech_part = 'adjective'
      group by wt.speech_part, wt.id) word_from_word_type
         join word w2
              on word_from_word_type.word_id_max = w2.id
         left join derivative_form df
                   on w2.id = df.base_word_id
                       and df.description = 'м.р. непълен член'
         left join derivative_form df2
                   on w2.id = df2.base_word_id
                       and df2.description = 'м.р. пълен член'
         left join derivative_form df3
                   on w2.id = df3.base_word_id
                       and df3.description = 'мн.ч.'
         left join derivative_form df4
                   on w2.id = df4.base_word_id
                       and df4.description = 'мн.ч. членувано'
         left join derivative_form df5
                   on w2.id = df5.base_word_id
                       and df5.description = 'ж.р.'
         left join derivative_form df6
                   on w2.id = df6.base_word_id
                       and df6.description = 'ж.р. членувано'
         left join derivative_form df7
                   on w2.id = df7.base_word_id
                       and df7.description = 'ср.р.'
         left join derivative_form df8
                   on w2.id = df8.base_word_id
                       and df8.description = 'ср.р. членувано'
/*where /*df.name <> df3.name || 'я'
    or df3.name <> w2.name || 'и' and df3.name <> w2.name and w2.name not like '%ен'
    or df4.name <> df3.name || 'те'
        or
        df5.name <> substr(w2.name,0, length(w2.name)) || 'а'
            and df5.name <> w2.name || 'а'
            and df5.name <> w2.name and w2.name not like '%ен'
   or df6.name <> df5.name || 'та'
    or */
        /*df7.name <> substr(df5.name,0, length(df5.name)) || 'о'
        /*
    or df8.name <> df7.name || 'то'
   /*
   or (substr(w2.name,0, length(w2.name)) || 'а' <> df3.name
           and substr(w2.name,0, length(w2.name)) || 'е' <> df3.name)
   or  (df3.name || 'те' <> df4.name
    and df3.name || 'та' <> df4.name)*/
order by word_from_word_type.speech_part, word_from_word_type.id ;










select distinct df.description
    from derivative_form df
    join word w
        on w.id = df.base_word_id
    join word_type wt
        on wt.id = w.type_id
        and wt.speech_part in ('adjective');
