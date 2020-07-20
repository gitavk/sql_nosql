import psycopg2

from sql_nosql import utils


def create_city_type():
    """Create city type"""

    with psycopg2.connect(**utils.postgres_config) as client_postgres:
        with client_postgres.cursor() as cur:
            cur.execute(
                """
                CREATE TYPE city_type
                AS ENUM ('megapolis', 'town', 'village');

                CREATE TABLE city (
                city VARCHAR(64) PRIMARY KEY,
                type city_type
                );
                """
            )

            cur.execute(
                """
                SELECT hometown, COUNT(*) FROM person GROUP BY hometown
                """
            )
            population_per_city = {city[0]: city[1] for city in cur.fetchall()}
            number_of_people = sum(population_per_city.values())

            for city, population in population_per_city.items():
                if population / number_of_people > .25:
                    city_type = 'megapolis'
                elif population / number_of_people < .15:
                    city_type = 'village'
                else:
                    city_type = 'town'

                cur.execute(
                    """
                    INSERT INTO city (city, type) VALUES (%s, %s)
                    """, (city, city_type)
                )

            cur.execute(
                """
                ALTER TABLE address
                ADD CONSTRAINT const_name
                FOREIGN KEY (city) REFERENCES city(city)
                """
            )


if __name__ == "__main__":
    create_city_type()
