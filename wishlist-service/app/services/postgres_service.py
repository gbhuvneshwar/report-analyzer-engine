import asyncpg
from typing import Optional, List

class PostgresService:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.database_url)

    async def get_record(self, table: str, record_id: str) -> Optional[dict]:
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(
                f"SELECT * FROM {table} WHERE id = $1", record_id
            )

    async def create_record(self, table: str, record: dict) -> dict:
        async with self.pool.acquire() as connection:
            columns = ", ".join(record.keys())
            placeholders = ", ".join(f"${i+1}" for i in range(len(record)))
            values = list(record.values())
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING *"
            return await connection.fetchrow(query, *values)

    async def update_record(self, table: str, record_id: str, updates: dict) -> Optional[dict]:
        async with self.pool.acquire() as connection:
            set_clause = ", ".join(f"{k} = ${i+2}" for i, k in enumerate(updates.keys()))
            values = [record_id] + list(updates.values())
            query = f"UPDATE {table} SET {set_clause} WHERE id = $1 RETURNING *"
            return await connection.fetchrow(query, *values)

    async def delete_record(self, table: str, record_id: str) -> bool:
        async with self.pool.acquire() as connection:
            result = await connection.execute(
                f"DELETE FROM {table} WHERE id = $1", record_id
            )
            return result == "DELETE 1"

    async def close(self):
        if self.pool:
            await self.pool.close()