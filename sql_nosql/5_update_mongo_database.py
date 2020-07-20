import psycopg2
import pymongo

from sql_nosql import utils


def update_mongo_database():
    """Update the collection in the mongo to
    synchronize it with new data in the PostgreSQL."""

    with psycopg2.connect(**utils.postgres_config) as client_postgres:
        with client_postgres.cursor() as cur:
            cur.execute(
                """
                SELECT city, type FROM city
                """
            )
            cities = {city[0]: city[1] for city in cur.fetchall()}

    with pymongo.MongoClient(**utils.mongo_config) as client_mongo:
        collection = client_mongo.traindb.person

        for city, city_type in cities.items():
            collection.update_many(
                {'hometown': {'$eq': city}},
                {'$set': {'city_type': city_type}}
            )
            collection.update_many(
                {},
                {'$set': {'address.$[addr].city_type': city_type}},
                array_filters=[{'addr.city': {'$eq': city}}]
            )


if __name__ == "__main__":
    update_mongo_database()
