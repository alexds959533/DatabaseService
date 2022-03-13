from datetime import datetime
import gridfs
from bson.objectid import ObjectId
from fastapi import HTTPException, File
from motor.motor_asyncio import AsyncIOMotorGridFSBucket, AsyncIOMotorDatabase

from core.settings import DATABASE_FILES_COLLECTION
from server.models import ObjectIdStr


async def chunk_generator(grid_out):
    while True:
        chunk = await grid_out.readchunk()
        if not chunk:
            break
        yield chunk


async def upload_file_to_fs(file: File, conn: AsyncIOMotorDatabase) -> (ObjectIdStr, datetime):
    """upload file to mongo file storage"""
    fs = AsyncIOMotorGridFSBucket(conn)
    file_id = await fs.upload_from_stream(
        file.filename,
        file.file,
        metadata={"contentType": file.content_type}
    )
    if file_id is None:
        raise HTTPException(status_code=400, detail="error in file upload")
    return file_id, file_id.generation_time


async def download_file_from_fs(file_id, conn: AsyncIOMotorDatabase):
    """download file from mongo file storage"""
    fs = AsyncIOMotorGridFSBucket(conn)
    try:
        grid_out = await fs.open_download_stream(ObjectId(file_id))
    except gridfs.errors.NoFile:
        raise HTTPException(status_code=404, detail="File not found")

    content_type = grid_out.metadata.get('contentType')
    return chunk_generator(grid_out), content_type


async def delete_file_from_fs(file_id: ObjectIdStr, conn: AsyncIOMotorDatabase):
    """delete file from mongo file storage"""
    fs = AsyncIOMotorGridFSBucket(conn)
    await fs.delete(ObjectId(file_id))