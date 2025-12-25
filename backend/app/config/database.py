from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os


class Database:
    client: Optional[AsyncIOMotorClient] = None
    
    
db = Database()


async def get_database():
    """Get the MongoDB database instance"""
    return db.client.todolist_db


async def connect_to_mongo():
    """Create database connection"""
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    print(f"Connecting to MongoDB at {mongodb_url}")
    db.client = AsyncIOMotorClient(mongodb_url)
    print("Connected to MongoDB successfully")


async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        print("MongoDB connection closed")
