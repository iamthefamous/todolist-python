from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom type for handling MongoDB ObjectId in Pydantic"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class TodoBase(BaseModel):
    """Base Todo model with common fields"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: bool = Field(default=False)


class TodoCreate(TodoBase):
    """Model for creating a new Todo"""
    pass


class TodoUpdate(BaseModel):
    """Model for updating an existing Todo (all fields optional)"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None


class TodoInDB(TodoBase):
    """Model representing a Todo in the database"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "title": "Learn FastAPI",
                "description": "Complete the FastAPI tutorial",
                "completed": False
            }
        }


class TodoResponse(BaseModel):
    """Model for Todo API responses"""
    id: str
    title: str
    description: Optional[str] = None
    completed: bool
    createdAt: datetime
    updatedAt: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "title": "Learn FastAPI",
                "description": "Complete the FastAPI tutorial",
                "completed": False,
                "createdAt": "2025-11-24T10:00:00",
                "updatedAt": "2025-11-24T10:00:00"
            }
        }
