from redis.asyncio import Redis
from src.config import Config
import json
from datetime import timedelta

redis = Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    decode_responses=True  # strings instead of bytes
)

async def store_refresh_token(refresh_token:str, user_id:int, user_email:str, expiry_in_days:timedelta):
    value = json.dumps({
        "user_id":user_id,
        "user_email":user_email
    })

    await redis.setex(
        f"refresh:{refresh_token}",
        int(expiry_in_days.total_seconds()),
        value
    )

async def get_refresh_token_data(refresh_token:str):
    user_details = await redis.get(f"refresh:{refresh_token}")
    print("user_details --->", user_details)
    return json.loads(user_details) if user_details else None   # convert str to dict again

async def revoke_refresh_token(refresh_token:str):
    await redis.delete(f"refresh:{refresh_token}")


