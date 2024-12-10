from contextlib import asynccontextmanager


from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from config.general import settings
from src.contacts.routers import router as contacts_router
from src.auth.routers import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    redis = aioredis.from_url(settings.redis_url, encoding="utf-8")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    # Shutdown event
    await redis.close()

app = FastAPI(lifespan=lifespan)
app.include_router(contacts_router, prefix="/contacts", tags=["contacts"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.get("/ping")
async def ping():
    return {"msg": "pong"}



@app.get("/")
async def root():
    return {"message": "Hello World"}


