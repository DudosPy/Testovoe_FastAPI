from pymongo import MongoClient
from app.config import settings

client = MongoClient(f"mongodb://{settings.mongo_host}:{settings.mongo_port}/")
db = client.delivery_logs
logs_collection = db.calculations