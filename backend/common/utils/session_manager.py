import redis.asyncio as redis
import os

class SessionManager:
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")  # Especificar base de datos 0
        self.redis = None

    async def connect(self):
        if not self.redis:
            self.redis = redis.from_url(self.redis_url, decode_responses=True)

    async def store_jwt(self, session_id: str, token: str):
        await self.connect()
        await self.redis.set(session_id, token, ex=1800)  # Expira en 30 minutos

    async def get_jwt(self, session_id: str):
        await self.connect()
        token = await self.redis.get(session_id)
        return token

    async def delete_jwt(self, session_id: str):
        await self.connect()
        await self.redis.delete(session_id)