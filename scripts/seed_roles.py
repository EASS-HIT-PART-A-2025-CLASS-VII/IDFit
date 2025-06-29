import json, asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

async def seed():
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client[settings.db_name]
    # מוודא שה־roles.json נמצא בשורש הפרויקט
    with open("roles.json", encoding="utf-8") as f:
        roles = json.load(f)
    # שוטף את הישנים ומוסיף את החדשים
    await db.roles.delete_many({})
    await db.roles.insert_many(roles)
    print(f"Seeded {len(roles)} roles.")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed())
