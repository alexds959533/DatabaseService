from bson.objectid import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from core.settings import DATABASE_FILES_COLLECTION
from .models import FileCreate, ObjectIdStr


async def retrieve_files(conn: AsyncIOMotorDatabase) -> [dict]:
    files = []
    async for file in conn[DATABASE_FILES_COLLECTION].find():
        files.append(file)
    return files


async def create_file(file: FileCreate, conn: AsyncIOMotorDatabase) -> dict:
    id = await conn[DATABASE_FILES_COLLECTION].insert_one(file.dict())
    if id is None:
        raise HTTPException(status_code=400, detail="error in file metadata upload")
    file_metadata = await conn[DATABASE_FILES_COLLECTION].find_one({"_id": id.inserted_id})
    return file_metadata


# Retrieve a file with a matching ID
async def retrieve_file(id: ObjectIdStr, conn: AsyncIOMotorDatabase) -> dict:
    file = await conn[DATABASE_FILES_COLLECTION].find_one({"_id": ObjectId(id)})
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return file


# Update a file with a matching ID
async def update_file(id: ObjectIdStr, data: dict, conn: AsyncIOMotorDatabase) -> dict:
    await conn[DATABASE_FILES_COLLECTION].update_one(
        {"_id": ObjectId(id)}, {"$set": {k : v for k, v in data.items() if v}}
    )
    file = await conn[DATABASE_FILES_COLLECTION].find_one({"_id": ObjectId(id)})
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return file


async def delete_file(id: str, conn: AsyncIOMotorDatabase) -> ObjectIdStr:
    file = await conn[DATABASE_FILES_COLLECTION].find_one({"_id": ObjectId(id)})
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")

    # delete file metadata
    await conn[DATABASE_FILES_COLLECTION].delete_one({"_id": ObjectId(id)})
    return file.get('file_id')
