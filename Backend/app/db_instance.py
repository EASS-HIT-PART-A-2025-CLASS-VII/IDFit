from motor.motor_asyncio import AsyncIOMotorClient

db = AsyncIOMotorClient("mongodb://idfit-mongo:27017").my_database
