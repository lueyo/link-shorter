from pymongo import MongoClient
from os import environ

MONGO_URI = environ.get("MONGO_URI")

db_client = MongoClient(MONGO_URI).get_database("linkShort")