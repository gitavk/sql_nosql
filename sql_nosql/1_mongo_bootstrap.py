import random

import pymongo
from faker import Faker

from sql_nosql import utils


def mongo_bootstrap():
    """Initial data"""

    with pymongo.MongoClient(**utils.mongo_config) as client:
        collection = client.traindb.person

        fake = Faker()
        cities = [fake.city() for _ in range(5)]
        dist = [.3, .3, .2, .1, .1]

        new_persons = [{'first_name': fake.first_name(),
                        'last_name': fake.last_name(),
                        'date_of_birth': str(fake.date_of_birth()),
                        'hometown': random.choices(cities, dist)[0],
                        'phone': [{'number': fake.phone_number(),
                                   'type': random.choice(utils.PHONE_TYPE)}
                                  for _ in range(random.randint(1, 3))],
                        'address': [{'address': fake.address(),
                                     'city': random.choices(cities, dist)[0],
                                     'type': random.choice(utils.ADDRESS_TYPE)}
                                    for _ in range(random.randint(1, 3))]}
                       for _ in range(500)]

        collection.insert_many(new_persons)


if __name__ == '__main__':
    mongo_bootstrap()
