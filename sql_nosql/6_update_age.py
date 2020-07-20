import psycopg2
import pymongo

from sql_nosql import utils


def update_age():
    """Update the age of the persons so, the youngest man living in the village
    should be 20 years old, and the oldest man in the megalopolis
    should be 60 years. ( change only year)

    Synchronize the values with mongo db, only for updated values."""

    with psycopg2.connect(**utils.postgres_config) as client_postgres:
        with client_postgres.cursor() as cur:
            cur.execute(
                """
                UPDATE person as p
                SET date_of_birth=(current_date - INTERVAL '20 years')
                WHERE date_of_birth=(
                SELECT max(date_of_birth) FROM person
                JOIN city ON person.hometown = city.city 
                WHERE city.type = 'village') 
                RETURNING p.first_name, p.last_name, p.date_of_birth
                """
            )

            youngest = cur.fetchone()

            cur.execute(
                """
                UPDATE person as p
                SET date_of_birth=(current_date - INTERVAL '60 years')
                WHERE date_of_birth=(
                SELECT min(date_of_birth) FROM person 
                JOIN city ON person.hometown = city.city 
                WHERE city.type = 'megapolis') 
                RETURNING p.first_name, p.last_name, p.date_of_birth
                """
            )

            oldest = cur.fetchone()

    with pymongo.MongoClient(**utils.mongo_config) as client_mongo:
        collection = client_mongo.traindb.person

        collection.find_one_and_update({'first_name': youngest[0], 'last_name': youngest[1]}, {'$set': {'date_of_birth': str(youngest[2])}})
        collection.find_one_and_update({'first_name': oldest[0], 'last_name': oldest[1]}, {'$set': {'date_of_birth': str(oldest[2])}})


if __name__ == "__main__":
    update_age()
