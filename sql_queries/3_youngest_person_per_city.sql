SELECT p1.first_name, p1.last_name, date_of_birth, hometown
FROM person as p1 JOIN
(SELECT hometown, max(date_of_birth) as date_of_birth
FROM person GROUP BY hometown) as p2
USING (date_of_birth, hometown)
