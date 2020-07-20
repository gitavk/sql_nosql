import pprint

import pymongo

from sql_nosql import utils


def update_mongo_database():
    """Create select from the mongo:

    Get the biggest megalopolis.
    Get the list of persons living in the smallest village."""

    with pymongo.MongoClient(**utils.mongo_config) as client_mongo:
        collection = client_mongo.traindb.person

        pprint.pprint(list(collection.aggregate([
            {'$match': {'city_type': {'$eq': 'megapolis'}}},
            {'$group': {'_id': '$hometown', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 1}
        ])))

        smallest_village = list(collection.aggregate([
            {'$match': {'city_type': {'$eq': 'village'}}},
            {'$group': {'_id': '$hometown', 'count': {'$sum': 1}}},
            {'$sort': {'count': 1}},
            {'$limit': 1}
        ]))[0]['_id']
        pprint.pprint(list(collection.find({'hometown': smallest_village})))


if __name__ == "__main__":
    update_mongo_database()
