SELECT p.first_name, p.last_name,
string_agg(DISTINCT phone.number, ', ')  as numbers,
string_agg(DISTINCT address.address, ', ')  as addresses
FROM person as p
LEFT JOIN phone ON p.id = phone.person_id
LEFT JOIN address ON p.id = address.person_id
GROUP BY p.id
