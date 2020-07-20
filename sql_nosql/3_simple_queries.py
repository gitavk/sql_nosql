import pprint

import psycopg2

from sql_nosql import utils


def simple_queries():
    """Base select"""

    with psycopg2.connect(**utils.postgres_config) as client_postgres:
        with client_postgres.cursor() as cur:
            # 1) Get records person + phones + address
            cur.execute(
                """
                SELECT person.*, 
                string_agg(DISTINCT phone.number, ', ')  as numbers,
                string_agg(DISTINCT address.address, ', ')  as addresses
                FROM person
                LEFT JOIN phone ON person.id = phone.person_id
                LEFT JOIN address ON person.id = address.person_id
                GROUP BY person.id
                """
            )
            result = cur.fetchall()
            pprint.pprint(result)

            # 2) Get top 10 most younger person
            cur.execute(
                """
                SELECT * FROM person ORDER BY date_of_birth DESC LIMIT 10
                """
            )
            result = cur.fetchall()
            pprint.pprint(result)

            # 3) Get top 10 most old person
            cur.execute(
                """
                SELECT * FROM person ORDER BY date_of_birth LIMIT 10
                """
            )
            result = cur.fetchall()
            pprint.pprint(result)

            # 4) Get most younger person per city
            cur.execute(
                """
                SELECT p1.* FROM person as p1 
                JOIN (SELECT hometown, max(date_of_birth) as date_of_birth 
                FROM person GROUP BY hometown) as p2 
                ON p1.date_of_birth = p2.date_of_birth 
                AND p1.hometown = p2.hometown
                """
            )
            result = cur.fetchall()
            pprint.pprint(result)

            # 5) Get mean age per city
            cur.execute(
                """
                SELECT hometown, AVG(AGE(date_of_birth)) AS mean_age 
                FROM person 
                GROUP BY hometown
                """
            )
            result = cur.fetchall()
            pprint.pprint(result)


if __name__ == "__main__":
    simple_queries()
