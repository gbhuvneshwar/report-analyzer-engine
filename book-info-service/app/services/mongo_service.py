from pymongo import MongoClient
from typing import Optional, List

class MongoService:
    def __init__(self, mongo_url: str, database: str):
        self.client = MongoClient(mongo_url)
        self.db = self.client[database]

    def get_collection(self, collection: str):
        return self.db[collection]

    async def get_record(self, collection: str, record_id: str) -> Optional[dict]:
        return self.get_collection(collection).find_one({"_id": record_id})

    async def create_record(self, collection: str, record: dict) -> dict:
        record["_id"] = record.pop("id")
        result = self.get_collection(collection).insert_one(record)
        return record

    async def update_record(self, collection: str, record_id: str, updates: dict) -> Optional[dict]:
        updates.pop("_id", None)
        result = self.get_collection(collection).update_one(
            {"_id": record_id}, {"$set": updates}
        )
        return await self.get_record(collection, record_id) if result.modified_count else None

    async def delete_record(self, collection: str, record_id: str) -> bool:
        result = self.get_collection(collection).delete_one({"_id": record_id})
        return result.deleted_count == 1

    def close(self):
        self.client.close()