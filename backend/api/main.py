from fastapi import FastAPI
from contextlib import asynccontextmanager
from .routes import router


@asynccontextmanager
async def lifespan(app:FastAPI):
    #pre start
    yield
    #post start


app = FastAPI(lifespan=lifespan)


app.include_router(router)