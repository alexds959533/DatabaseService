from random import randint
from fastapi import APIRouter, Body, responses, Depends, File, UploadFile

from core.db.mongodb import AsyncIOMotorDatabase, get_database

from .crud import (
    create_file,
    retrieve_files,
    retrieve_file,
    update_file,
    delete_file,
)
from .models import (
    FileRetrieve,
    FileUpdate,
    ObjectIdStr,
    FileCreate,
)
from .utils import upload_file_to_fs, download_file_from_fs, delete_file_from_fs

router = APIRouter()


async def get_user_id() -> int:
    return randint(1, 10)


@router.post("/", response_model=FileRetrieve, status_code=201)
async def create_file_data(
        file: UploadFile = File(...),
        user_id: int = Depends(get_user_id),
        db: AsyncIOMotorDatabase = Depends(get_database),
):
    file_id, upload_date = await upload_file_to_fs(file, db)
    file_create = FileCreate(
        filename=file.filename,
        file_id=str(file_id),
        upload_date=str(file_id.generation_time),
        user_id=user_id
    )
    data = await create_file(file_create, db)
    return data


@router.get("/", response_model=list[FileRetrieve])
async def get_files_data(db: AsyncIOMotorDatabase = Depends(get_database)):
    files = await retrieve_files(db)
    return files


@router.get("/{id}/", response_model=FileRetrieve)
async def get_files_data(
        id: ObjectIdStr,
        db: AsyncIOMotorDatabase = Depends(get_database),
):
    file = await retrieve_file(id, db)
    return file


@router.put("/{id}", response_model=FileRetrieve)
async def update_file_data(
        id: ObjectIdStr,
        body: FileUpdate = Body(...),
        db: AsyncIOMotorDatabase = Depends(get_database),
):
    updated_file = await update_file(id, body.dict(), db)
    return updated_file


@router.delete("/{id}", response_description="File data deleted from the database")
async def delete_file_data(
        id: ObjectIdStr,
        db: AsyncIOMotorDatabase = Depends(get_database),
):
    file_id = await delete_file(id, db)
    await delete_file_from_fs(file_id, db)
    return responses.JSONResponse(status_code=204)


@router.get("/download/{file_id}/")
async def download_file_data(
        file_id: ObjectIdStr,
        db: AsyncIOMotorDatabase = Depends(get_database),
):
    content, content_type = await download_file_from_fs(file_id, db)
    return responses.StreamingResponse(content, media_type=content_type)

