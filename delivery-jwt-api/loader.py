from database import DatabaseAdapter
from fastapi import FastAPI
from contextlib import asynccontextmanager

from config import DATABASE_URL


app = FastAPI(title="Delivery Service API")
AdapterDB = DatabaseAdapter(DATABASE_URL)

@asynccontextmanager
async def lifespan(_: FastAPI):
    """Инициализация базы данных

    :param _: app FastAPI
    :type _: FastAPI
    """
    await AdapterDB.init()
    yield

app = FastAPI(lifespan=lifespan, title="Delivery Service API")