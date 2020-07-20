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
                SELECT p.first_name, p.last_name, 
                string_agg(DISTINCT phone.number, ', ')  as numbers,
                string_agg(DISTINCT address.address, ', ')  as addresses
                FROM person as p
                LEFT JOIN phone ON p.id = phone.person_id
                LEFT JOIN address ON p.id = address.person_id
                GROUP BY p.id
                """
            )
            result = cur.fetchall()
            pprint.pprint(result)

            # 2) Get top 10 most younger person
            cur.execute(
                """
                SELECT first_name, last_name, date_of_birth 
                FROM person ORDER BY date_of_birth DESC LIMIT 10
                """
            )
            result = cur.fetchall()
            pprint.pprint(result)

            # 3) Get top 10 most old person
            cur.execute(
                """
                SELECT first_name, last_name, date_of_birth 
                FROM person ORDER BY date_of_birth LIMIT 10
                """
            )
            result = cur.fetchall()
            pprint.pprint(result)

            # 4) Get most younger person per city
            cur.execute(
                """
                SELECT p1.first_name, p1.last_name, date_of_birth, hometown 
                FROM person as p1 JOIN
                (SELECT hometown, max(date_of_birth) as date_of_birth 
                FROM person GROUP BY hometown) as p2 
                USING (date_of_birth, hometown)
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
