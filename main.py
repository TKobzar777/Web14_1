"""
Main module for the FastAPI application.

This module initializes the FastAPI application, sets up caching and rate limiting,
and includes routers for authentication and contacts.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from fastapi_limiter import FastAPILimiter

from config.general import settings
from src.auth.routers import router as router_auth
from src.contacts.routers import router as router_contacts

from fastapi.middleware.cors import CORSMiddleware


origins = [
    "http://localhost:3000"
    ]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for application startup and shutdown events.

    Args:
        app (FastAPI): The FastAPI application instance.

    During startup:
        - Initializes Redis connection.
        - Sets up FastAPI Cache and FastAPI Limiter.

    During shutdown:
        - Closes the Redis connection.
    """
    redis = aioredis.from_url(settings.redis_url, encoding="utf-8")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    await FastAPILimiter.init(redis)
    yield
    # Shutdown event
    await redis.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router_contacts, prefix="/contacts", tags=["contacts"])
app.include_router(router_auth, prefix="/auth", tags=["auth"])

@app.get("/ping")
async def ping():
    """ return ping"""
    return {"message": "pong"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




