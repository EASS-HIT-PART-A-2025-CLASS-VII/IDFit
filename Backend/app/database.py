from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings
import app.repositories as repos  # <-- מוודא שהמתקין מכיר את המודול repositories

client: AsyncIOMotorClient | None = None
db = None  # AsyncIOMotorDatabase

async def connect_to_mongo():
    global client, db
    print("🔌 connect_to_mongo() called")
    try:
        # התחברות למונגו-די.בי
        client = AsyncIOMotorClient(settings.mongodb_url)  # חיבור עם ה-URL שנמצא בהגדרות
        db = client[settings.db_name]  # התחברות למסד נתונים ספציפי
        repos.db = db  # מעדכן את מודול ה-repositories עם החיבור הנוכחי
        print("✔️ Connected to MongoDB, db is", db)
    except Exception as e:
        # אם יש שגיאה, נדפיס את השגיאה
        print(f"❌ Error connecting to MongoDB: {e}")
        raise

async def close_mongo():
    global client
    print("🔒 close_mongo() called")
    if client:
        client.close()
        print("🔒 MongoDB connection closed")
