from pymongo import MongoClient
from os import environ
from passlib.context import CryptContext

MONGO_URI = environ.get("MONGO_URI")
PASSKEY = environ.get("PASSKEY")
SALT = environ.get("SALT")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db_client = MongoClient(MONGO_URI).get_database("linkShort")