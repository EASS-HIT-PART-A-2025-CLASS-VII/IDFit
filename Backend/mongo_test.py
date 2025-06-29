from pymongo import MongoClient
from app.config import settings

try:
    client = MongoClient(
        settings.mongodb_url,
        serverSelectionTimeoutMS=5000
    )
    db = client[settings.db_name]
    print("✅ Success! Databases:", client.list_database_names())
except Exception as e:
    print("❌ Failed to connect to MongoDB:", e)
