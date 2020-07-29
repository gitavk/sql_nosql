SELECT hometown, AVG(AGE(date_of_birth)) AS mean_age
FROM person
GROUP BY hometown
