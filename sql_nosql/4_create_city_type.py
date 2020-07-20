import psycopg2
from sql_nosql import utils


def create_city_type():
    """Create city type"""

    with open('sql_queries/4_create_table_city.sql', 'r') as create_table_city, \
            open('sql_queries/4_population_per_city.sql', 'r') as population_per_city, \
            open('sql_queries/4_insert_city.sql', 'r') as insert_city, \
            open('sql_queries/4_add_foreign_key_on_address.sql', 'r') as add_foreign_key_on_address:
        create_table_city_query = create_table_city.read()
        population_per_city_query = population_per_city.read()
        insert_city_query = insert_city.read()
        add_foreign_key_on_address_query = add_foreign_key_on_address.read()

    with psycopg2.connect(**utils.postgres_config) as client_postgres:
        with client_postgres.cursor() as cur:
            cur.execute(create_table_city_query)

            cur.execute(population_per_city_query)
            population_per_city = {city[0]: city[1] for city in cur.fetchall()}
            number_of_people = sum(population_per_city.values())

            for city, population in population_per_city.items():
                if population / number_of_people > .25:
                    city_type = 'megapolis'
                elif population / number_of_people < .15:
                    city_type = 'village'
                else:
                    city_type = 'town'
                cur.execute(insert_city_query, (city, city_type))

            cur.execute(add_foreign_key_on_address_query)


if __name__ == "__main__":
    create_city_type()
