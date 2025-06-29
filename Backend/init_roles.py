import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import json

MONGO_URL = "mongodb://idfit-mongo:27017" 
DB_NAME = "my_database"
COLLECTION_NAME = "roles"

async def insert_roles():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    await db["roles"].delete_many({})

    existing_count = await collection.count_documents({})
    if existing_count == 0:
        with open("roles.json", encoding="utf-8") as f:
            data = json.load(f)
            await collection.insert_many(data)
            print(f"🚀 Inserted {len(data)} roles.")
    else:
        print(f"✅ Found {existing_count} roles. Skipping insert.")

if __name__ == "__main__":
    asyncio.run(insert_roles())
