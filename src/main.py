from contextlib import asynccontextmanager

from fastapi import FastAPI

from core import get_redis, load_translations_to_cache
from database import engine
from database.models import Base
from routers import router_health, router_root, router_shortener


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    r = get_redis()
    await r.ping()  # type: ignore

    load_translations_to_cache()
    yield
    await engine.dispose()

    await r.aclose()


app = FastAPI(title="URL Shortener", lifespan=lifespan)


app.include_router(router=router_root)
app.include_router(router=router_health)
app.include_router(router=router_shortener, prefix="/api")
