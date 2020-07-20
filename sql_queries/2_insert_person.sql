INSERT INTO person
(first_name, last_name, date_of_birth, hometown)
VALUES (%s, %s, %s, %s) RETURNING id
