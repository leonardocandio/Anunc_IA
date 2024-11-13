import redis.asyncio as aioredis
from datetime import timedelta

SESSION_TIMEOUT = timedelta(minutes=30)

class SessionManager:
    def __init__(self, redis_url=None):
        if redis_url is None:
            redis_url = "redis://redis:6379"
        print(f"Conectando a Redis en: {redis_url}")  # Agrega esta línea
        self.redis = aioredis.from_url(redis_url, decode_responses=True)

    async def store_jwt(self, session_id: str, jwt_token: str):
        await self.redis.set(session_id, jwt_token, ex=int(SESSION_TIMEOUT.total_seconds()))

    async def get_jwt(self, session_id: str):
        return await self.redis.get(session_id)

    async def delete_jwt(self, session_id: str):
        await self.redis.delete(session_id)
