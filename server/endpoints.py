from random import randint
from fastapi import APIRouter, Body, responses, Depends, File, UploadFile

from core.db.mongodb import AsyncIOMotorClient, get_database

from server.crud import (
    delete_file,
    retrieve_files,
    retrieve_file,
    update_file,
    add_file_to_fs,
    download_file
)
from server.models import (
    FileRetrieve,
    FileUpdate,
    ObjectIdStr
)

router = APIRouter()


async def get_user_id() -> int:
    return randint(1, 10)


@router.post("/", response_model=FileRetrieve)
async def create_file(
        file: UploadFile = File(...),
        user_id: int = Depends(get_user_id),
        db: AsyncIOMotorClient = Depends(get_database),
):
    new_file = await add_file_to_fs(file, user_id, db)
    return new_file


@router.get("/", response_model=list[FileRetrieve])
async def get_files_data(db: AsyncIOMotorClient = Depends(get_database)):
    files = await retrieve_files(db)
    return files


@router.get("/{id}/", response_model=FileRetrieve)
async def get_files_data(
        id: ObjectIdStr,
        db: AsyncIOMotorClient = Depends(get_database),
):
    file = await retrieve_file(id, db)
    return file


@router.put("/{id}", response_model=FileRetrieve)
async def update_file_data(
        id: ObjectIdStr,
        body: FileUpdate = Body(...),
        db: AsyncIOMotorClient = Depends(get_database),
):
    updated_file = await update_file(id, body.dict(), db)
    return updated_file


@router.delete("/{id}", response_description="File data deleted from the database")
async def delete_file_data(
        id: ObjectIdStr,
        db: AsyncIOMotorClient = Depends(get_database),
):
    await delete_file(id, db)
    return responses.JSONResponse(status_code=204)


@router.get("/download/{file_id}/")
async def download_file_data(
        file_id: ObjectIdStr,
        db: AsyncIOMotorClient = Depends(get_database),
):
    content, content_type = await download_file(file_id, db)
    return responses.StreamingResponse(content, media_type=content_type)

