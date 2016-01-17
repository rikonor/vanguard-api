import os
from pymongo import MongoClient

MONGO_URL = os.environ.get("MONGO_URL")
if MONGO_URL is None:
    raise EnvironmentError("Please provide a MONGO_URL")

CLIENT = MongoClient(MONGO_URL)
DB = CLIENT.vanguard
