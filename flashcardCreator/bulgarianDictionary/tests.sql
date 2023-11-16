SELECT df.id, df.name, df.description, w.id, w.meaning, w.type_id, wt.speech_part, wt.comment, wt.rules, wt.rules_test, wt.example_word
FROM derivative_form as df
	join word as w
		on w.id = df.base_word_id
    join word_type as wt
		on w.type_id = wt.id
where df.name in ('мъж','мъже', 'легна', 'лягам');
select * from word where id = 85167;
select * from word_type where id = 46;

select * from word_type;
