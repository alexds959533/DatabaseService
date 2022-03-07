import gridfs
from bson.objectid import ObjectId
from fastapi import HTTPException, File
from motor.motor_asyncio import AsyncIOMotorGridFSBucket

from motor.motor_asyncio import AsyncIOMotorClient
from core.settings import database_name, files_collection
from .models import ObjectIdStr


async def retrieve_files(conn: AsyncIOMotorClient) -> [dict]:
    files = []
    async for file in conn[database_name][files_collection].find():
        files.append(file)
    return files


# Add a new file into to the database
async def add_file_to_fs(file: File, user_id: int, conn: AsyncIOMotorClient) -> dict:
    fs = AsyncIOMotorGridFSBucket(conn[database_name])
    file_id = await fs.upload_from_stream(
        file.filename,
        file.file,
        metadata={"contentType": file.content_type}
    )
    if file_id is None:
        raise HTTPException(status_code=400, detail="error in file upload")

    file_metadata = dict(
        filename=file.filename,
        file_id=str(file_id),
        upload_date=str(file_id.generation_time),
        user_id=user_id
    )
    file_metadata_id = await conn[database_name][files_collection].insert_one(file_metadata)
    if file_metadata_id is  None:
        raise HTTPException(status_code=400, detail="error in file metadata upload")
    file_metadata = await conn[database_name][files_collection].find_one({"_id": file_metadata_id.inserted_id})
    return file_metadata


# Retrieve a file with a matching ID
async def retrieve_file(id: ObjectIdStr, conn: AsyncIOMotorClient) -> dict:
    file = await conn[database_name][files_collection].find_one({"_id": ObjectId(id)})
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return file


# Update a file with a matching ID
async def update_file(id: ObjectIdStr, data: dict, conn: AsyncIOMotorClient) -> dict:
    await conn[database_name][files_collection].update_one(
        {"_id": ObjectId(id)}, {"$set": {k : v for k, v in data.items() if v}}
    )
    file = await conn[database_name][files_collection].find_one({"_id": ObjectId(id)})
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return file


# Delete a file from the database
async def delete_file(id: str, conn: AsyncIOMotorClient):
    file = await conn[database_name][files_collection].find_one({"_id": ObjectId(id)})
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")

    # delete file metadata
    await conn[database_name][files_collection].delete_one({"_id": ObjectId(id)})

    # delete file
    fs = AsyncIOMotorGridFSBucket(conn[database_name])
    await fs.delete(ObjectId(file.get('file_id')))


async def chunk_generator(grid_out):
    while True:
        chunk = await grid_out.readchunk()
        if not chunk:
            break
        yield chunk


async def download_file(file_id, conn: AsyncIOMotorClient):
    """Returns iterator over AsyncIOMotorGridOut object"""
    fs = AsyncIOMotorGridFSBucket(conn[database_name])
    try:
        grid_out = await fs.open_download_stream(ObjectId(file_id))
    except gridfs.errors.NoFile:
        raise HTTPException(status_code=404, detail="File not found")

    content_type = grid_out.metadata.get('contentType')
    return chunk_generator(grid_out), content_type