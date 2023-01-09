from motor.motor_asyncio import AsyncIOMotorClient

mongo_client: AsyncIOMotorClient = None

def init(**kwargs) -> AsyncIOMotorClient:
    global mongo_client
    if mongo_client is None:
        mongo_client = AsyncIOMotorClient(**kwargs)
    return mongo_client
