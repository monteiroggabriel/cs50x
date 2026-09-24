CREATE INDEX name_index ON people (name);
CREATE INDEX person_index ON stars (person_id);

SELECT title FROM shows WHERE id IN 
    (SELECT show_id FROM stars WHERE person_id = 
        (SELECT id FROM people WHERE name = 'Steve Carell'));
