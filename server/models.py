from datetime import datetime
from typing import Optional

from bson.errors import InvalidId
from fastapi import Form
from pydantic import BaseModel, Field
from bson.objectid import ObjectId


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            ObjectId(str(v))
        except InvalidId:
            raise ValueError("Not a valid ObjectId")
        return str(v)


class FileCreate(BaseModel):
    filename: str = Field(...)
    file_id: ObjectIdStr = Field(...)
    upload_date: datetime = Field(...)
    user_id: int = Field(...)


class FileRetrieve(BaseModel):
    id: ObjectIdStr = Field(..., alias='_id')
    filename: str = Field(...)
    file_id: ObjectIdStr = Field(...)
    upload_date: datetime
    user_id: int = Field(default=4)


class FileUpdate(BaseModel):
    filename: Optional[str]