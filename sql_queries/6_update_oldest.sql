UPDATE person as p
SET date_of_birth=(current_date - INTERVAL '60 years')
WHERE date_of_birth=(
SELECT min(date_of_birth) FROM person
JOIN city ON person.hometown = city.city
WHERE city.type = 'megapolis')
RETURNING p.first_name, p.last_name, p.date_of_birth
