import pprint
import psycopg2
from sql_nosql import utils


def simple_queries():
    """Base select"""

    with open('sql_queries/3_person_phone_address.sql', 'r') as person_phone_address, \
            open('sql_queries/3_top_ten_youngest_persons.sql', 'r') as top_ten_youngest_persons, \
            open('sql_queries/3_top_ten_oldest_persons.sql', 'r') as top_ten_oldest_persons, \
            open('sql_queries/3_youngest_person_per_city.sql', 'r') as youngest_person_per_city, \
            open('sql_queries/3_mean_age_per_city.sql', 'r') as mean_age_per_city:
        person_phone_address_query = person_phone_address.read()
        top_ten_youngest_persons_query = top_ten_youngest_persons.read()
        top_ten_oldest_persons_query = top_ten_oldest_persons.read()
        youngest_person_per_city_query = youngest_person_per_city.read()
        mean_age_per_city_query = mean_age_per_city.read()

    with psycopg2.connect(**utils.postgres_config) as client_postgres:
        with client_postgres.cursor() as cur:
            # 1) Get records person + phones + address
            cur.execute(person_phone_address_query)
            result = cur.fetchall()
            pprint.pprint(result)

            # 2) Get top 10 youngest person
            cur.execute(top_ten_youngest_persons_query)
            result = cur.fetchall()
            pprint.pprint(result)

            # 3) Get top 10 oldest person
            cur.execute(top_ten_oldest_persons_query)
            result = cur.fetchall()
            pprint.pprint(result)

            # 4) Get youngest person per city
            cur.execute(youngest_person_per_city_query)
            result = cur.fetchall()
            pprint.pprint(result)

            # 5) Get mean age per city
            cur.execute(mean_age_per_city_query)
            result = cur.fetchall()
            pprint.pprint(result)


if __name__ == "__main__":
    simple_queries()
