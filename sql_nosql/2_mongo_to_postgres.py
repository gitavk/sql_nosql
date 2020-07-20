import psycopg2
import pymongo
from sql_nosql import utils


def mongo_to_postgres():
    """Load data from Mongo to PostgreSQL"""

    with open('sql_queries/2_insert_person.sql', 'r') as insert_person, \
            open('sql_queries/2_insert_phone.sql', 'r') as insert_phone, \
            open('sql_queries/2_insert_address.sql', 'r') as insert_address:
        insert_person_query = insert_person.read()
        insert_phone_query = insert_phone.read()
        insert_address_query = insert_address.read()

    with pymongo.MongoClient(**utils.mongo_config) as client_mongo:
        collection = client_mongo.traindb.person
        mongo_data = collection.find({})

    with psycopg2.connect(**utils.postgres_config) as client_postgres:
        with client_postgres.cursor() as cur:
            for person in mongo_data:
                cur.execute(insert_person_query,
                            (person['first_name'], person['last_name'],
                             person['date_of_birth'], person['hometown']))

                idx = cur.fetchone()[0]
                for phone in person['phone']:
                    cur.execute(insert_phone_query,
                                (phone['number'], phone['type'], idx))
                for address in person['address']:
                    cur.execute(insert_address_query,
                                (address['address'], address['city'], address['type'], idx))


if __name__ == '__main__':
    mongo_to_postgres()
