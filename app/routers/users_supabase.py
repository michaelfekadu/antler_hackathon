"""User management endpoints using Supabase REST API."""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from uuid import UUID

from app.supabase_client import get_supabase
from app.schemas import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    """Create a new user."""
    supabase = get_supabase()
    
    # Check if telegram_id already exists
    existing = supabase.table("users").select("*").eq("telegram_id", user.telegram_id).execute()
    if existing.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this telegram_id already exists"
        )
    
    # Create user
    result = supabase.table("users").insert(user.model_dump()).execute()
    if not result.data:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user")
    
    return result.data[0]


@router.get("/", response_model=List[UserResponse])
def list_users(skip: int = 0, limit: int = 100):
    """List all users."""
    supabase = get_supabase()
    result = supabase.table("users").select("*").range(skip, skip + limit - 1).execute()
    return result.data


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: UUID):
    """Get a specific user by ID."""
    supabase = get_supabase()
    result = supabase.table("users").select("*").eq("id", str(user_id)).execute()
    
    if not result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return result.data[0]


@router.get("/telegram/{telegram_id}", response_model=UserResponse)
def get_user_by_telegram_id(telegram_id: str):
    """Get a user by their Telegram ID."""
    supabase = get_supabase()
    result = supabase.table("users").select("*").eq("telegram_id", telegram_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return result.data[0]


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: UUID, user_update: UserUpdate):
    """Update a user."""
    supabase = get_supabase()
    
    # Check if user exists
    existing = supabase.table("users").select("*").eq("id", str(user_id)).execute()
    if not existing.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Update user
    update_data = user_update.model_dump(exclude_unset=True)
    result = supabase.table("users").update(update_data).eq("id", str(user_id)).execute()
    
    return result.data[0]


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID):
    """Delete a user."""
    supabase = get_supabase()
    
    # Check if user exists
    existing = supabase.table("users").select("*").eq("id", str(user_id)).execute()
    if not existing.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Delete user
    supabase.table("users").delete().eq("id", str(user_id)).execute()
    return None

