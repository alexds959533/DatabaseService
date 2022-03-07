import logging

from motor.motor_asyncio import AsyncIOMotorClient
from ..settings import MONGO_URL
from .mongodb import db


async def connect_to_mongo():
    db.client = AsyncIOMotorClient(str(MONGO_URL))
    logging.info("open connect to mongodb")


async def close_mongo_connection():
    db.client.close()
    logging.info("connect to mongodb is closed")