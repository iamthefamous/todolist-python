from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

from app.models.todo import TodoCreate, TodoUpdate, TodoResponse
from app.config.database import get_database


router = APIRouter(
    prefix="/api/todos",
    tags=["todos"]
)


def todo_helper(todo) -> dict:
    """Convert MongoDB document to dict"""
    return {
        "id": str(todo["_id"]),
        "title": todo["title"],
        "description": todo.get("description"),
        "completed": todo["completed"],
        "createdAt": todo["createdAt"],
        "updatedAt": todo["updatedAt"]
    }


@router.get("", response_model=List[TodoResponse])
async def get_todos(completed: Optional[bool] = Query(None)):
    """
    Get all todos with optional filtering by completion status
    - **completed**: Optional filter (true for completed, false for active)
    """
    db = await get_database()
    
    # Build query filter
    query = {}
    if completed is not None:
        query["completed"] = completed
    
    todos = []
    async for todo in db.todos.find(query):
        todos.append(todo_helper(todo))
    
    return todos


@router.get("/search", response_model=List[TodoResponse])
async def search_todos(title: str = Query(..., min_length=1)):
    """
    Search todos by title using case-insensitive regex
    - **title**: Search query string
    """
    db = await get_database()
    
    # Case-insensitive search using regex
    query = {"title": {"$regex": title, "$options": "i"}}
    
    todos = []
    async for todo in db.todos.find(query):
        todos.append(todo_helper(todo))
    
    return todos


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: str):
    """
    Get a specific todo by ID
    - **todo_id**: The ID of the todo to retrieve
    """
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid todo ID format"
        )
    
    db = await get_database()
    todo = await db.todos.find_one({"_id": ObjectId(todo_id)})
    
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    
    return todo_helper(todo)


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate):
    """
    Create a new todo
    - **title**: Title of the todo (required)
    - **description**: Description of the todo (optional)
    - **completed**: Completion status (default: false)
    """
    db = await get_database()
    
    now = datetime.utcnow()
    todo_dict = {
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
        "createdAt": now,
        "updatedAt": now
    }
    
    result = await db.todos.insert_one(todo_dict)
    created_todo = await db.todos.find_one({"_id": result.inserted_id})
    
    return todo_helper(created_todo)


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: str, todo_update: TodoUpdate):
    """
    Update an existing todo
    - **todo_id**: The ID of the todo to update
    - **title**: New title (optional)
    - **description**: New description (optional)
    - **completed**: New completion status (optional)
    """
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid todo ID format"
        )
    
    db = await get_database()
    
    # Check if todo exists
    existing_todo = await db.todos.find_one({"_id": ObjectId(todo_id)})
    if existing_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    
    # Build update document with only provided fields
    update_data = {k: v for k, v in todo_update.model_dump(exclude_unset=True).items()}
    
    if update_data:
        update_data["updatedAt"] = datetime.utcnow()
        await db.todos.update_one(
            {"_id": ObjectId(todo_id)},
            {"$set": update_data}
        )
    
    updated_todo = await db.todos.find_one({"_id": ObjectId(todo_id)})
    return todo_helper(updated_todo)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: str):
    """
    Delete a specific todo
    - **todo_id**: The ID of the todo to delete
    """
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid todo ID format"
        )
    
    db = await get_database()
    
    result = await db.todos.delete_one({"_id": ObjectId(todo_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    
    return None


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_todos():
    """
    Delete all todos
    
    WARNING: This endpoint is intended for development/testing only.
    In production, this should be protected with proper authentication/authorization.
    """
    db = await get_database()
    await db.todos.delete_many({})
    return None
