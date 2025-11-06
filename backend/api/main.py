from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app:FastAPI):
    #pre start
    yield
    #post start


app = FastAPI(lifespan=lifespan)