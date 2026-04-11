from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from helpers.config import settings

uri = settings.DB_URI

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

database = client.mini_perplexity

# All collections for the database
queries_collection = database.queries_history   