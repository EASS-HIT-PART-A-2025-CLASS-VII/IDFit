from bson import ObjectId, errors
from app.db_instance import db

if db is None:
    raise RuntimeError("❌ Database not initialized (db is None)")

async def get_all_roles() -> list[dict]:
    """שולף את כל התפקידים ממסד הנתונים"""
    print("📬 Attempting to fetch roles from the database...")
    roles = []
    async for doc in db.roles.find({}):
        doc["id"] = str(doc["_id"])  # המרת ObjectId למחרוזת
        roles.append(doc)

    if not roles:
        print("📬 No roles found in the database.")
    else:
        print(f"📦 Total roles found: {len(roles)}")
        role_names = [role['name'] for role in roles]
        print("📌 Role names:", ", ".join(role_names))

    return roles

async def load_profile(pid: str) -> dict | None:
    """מעלה פרופיל לפי ID. אם אין או שהוא לא חוקי, מחזיר None."""
    try:
        oid = ObjectId(pid)
    except errors.InvalidId:
        print(f"⚠️ Invalid ObjectId: {pid}")
        return None

    profile = await db.profiles.find_one({"_id": oid})
    if not profile:
        print(f"⚠️ No profile found with id: {pid}")
    return profile

async def save_profile(data: dict) -> str:
    """שומר פרופיל חדש ומחזיר את המזהה שלו כמחרוזת"""
    print("💾 save_profile() called with:", data)

    if db is None:
        print("❌ Database connection is not initialized!")
        raise RuntimeError("❌ Database not initialized (db is None)")

    result = await db.profiles.insert_one(data)
    print(f"✅ insert_one returned: {result.inserted_id}")
    return str(result.inserted_id)
