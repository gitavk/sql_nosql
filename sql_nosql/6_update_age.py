import psycopg2
import pymongo
from sql_nosql import utils


def update_age():
    """Update the age of the persons so, the youngest man living in the village
    should be 20 years old, and the oldest man in the megalopolis
    should be 60 years. ( change only year)

    Synchronize the values with mongo db, only for updated values."""

    with open('sql_queries/6_update_youngest.sql', 'r') as update_youngest, \
            open('sql_queries/6_update_oldest.sql', 'r') as update_oldest:
        update_youngest_query = update_youngest.read()
        update_oldest_query = update_oldest.read()

    with psycopg2.connect(**utils.postgres_config) as client_postgres:
        with client_postgres.cursor() as cur:
            cur.execute(update_youngest_query)
            youngest = cur.fetchone()

            cur.execute(update_oldest_query)
            oldest = cur.fetchone()

    with pymongo.MongoClient(**utils.mongo_config) as client_mongo:
        collection = client_mongo.traindb.person

        collection.find_one_and_update(
            {'first_name': youngest[0], 'last_name': youngest[1]},
            {'$set': {'date_of_birth': str(youngest[2])}})

        collection.find_one_and_update(
            {'first_name': oldest[0], 'last_name': oldest[1]},
            {'$set': {'date_of_birth': str(oldest[2])}})


if __name__ == "__main__":
    update_age()
