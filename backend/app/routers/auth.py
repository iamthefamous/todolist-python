from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from bson import ObjectId

from app.models.user import UserCreate, UserLogin, UserResponse, Token
from app.utils.auth import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    get_current_user,
    user_helper
)
from app.config.database import get_database


router = APIRouter(
    prefix="/api/auth",
    tags=["authentication"]
)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    """
    Register a new user
    - **email**: User email address (must be unique)
    - **username**: Username (must be unique)
    - **password**: User password (minimum 6 characters)
    """
    db = await get_database()
    
    # Check if user with email already exists
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    existing_username = await db.users.find_one({"username": user.username})
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Hash the password
    hashed_password = get_password_hash(user.password)
    
    # Create user document
    now = datetime.utcnow()
    user_dict = {
        "email": user.email,
        "username": user.username,
        "hashed_password": hashed_password,
        "createdAt": now,
        "updatedAt": now
    }
    
    # Insert user into database
    result = await db.users.insert_one(user_dict)
    created_user = await db.users.find_one({"_id": result.inserted_id})
    
    return user_helper(created_user)


@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """
    Login with email and password
    - **email**: User email address
    - **password**: User password
    
    Returns a JWT access token for authentication
    """
    db = await get_database()
    
    # Find user by email
    user = await db.users.find_one({"email": user_credentials.email})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(user_credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user["email"]})
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: UserResponse = Depends(get_current_user)):
    """
    Get current authenticated user profile
    
    Requires authentication via JWT token in Authorization header:
    Authorization: Bearer <token>
    """
    return current_user
