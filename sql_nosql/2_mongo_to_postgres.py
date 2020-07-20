import psycopg2
import pymongo

from sql_nosql import utils


def mongo_to_postgres():
    """Load data from Mongo to PostgreSQL"""

    with pymongo.MongoClient(**utils.mongo_config) as client_mongo:
        collection = client_mongo.traindb.person
        mongo_data = collection.find({})

    with psycopg2.connect(**utils.postgres_config) as client_postgres:
        with client_postgres.cursor() as cur:
            for person in mongo_data:
                cur.execute(
                    """
                    INSERT INTO person 
                    (first_name, last_name, date_of_birth, hometown)
                    VALUES (%s, %s, %s, %s) RETURNING id
                    """,
                    (person['first_name'], person['last_name'], person['date_of_birth'], person['hometown'])
                )

                idx = cur.fetchone()[0]
                for phone in person['phone']:
                    cur.execute(
                        """
                        INSERT INTO phone 
                        (number, type, person_id) 
                        VALUES (%s, %s, %s)
                        """,
                        (phone['number'], phone['type'], idx)
                    )
                for address in person['address']:
                    cur.execute(
                        """
                        INSERT INTO address (address, city, type, person_id) 
                        VALUES (%s, %s, %s, %s)
                        """,
                        (address['address'], address['city'], address['type'], idx)
                    )


if __name__ == '__main__':
    mongo_to_postgres()
