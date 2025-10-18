"""Check-in management endpoints using Supabase REST API."""
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from uuid import UUID

from app.supabase_client import get_supabase
from app.schemas import CheckInCreate, CheckInUpdate, CheckInResponse
from app.utils import convert_uuids_to_strings

router = APIRouter(prefix="/checkins", tags=["check-ins"])


@router.post("/", response_model=CheckInResponse, status_code=status.HTTP_201_CREATED)
def create_checkin(checkin: CheckInCreate):
    """Create a new check-in."""
    supabase = get_supabase()
    
    # Verify user exists
    user_check = supabase.table("users").select("id").eq("id", str(checkin.user_id)).execute()
    if not user_check.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Create check-in
    checkin_data = convert_uuids_to_strings(checkin.model_dump())
    result = supabase.table("check_ins").insert(checkin_data).execute()
    if not result.data:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create check-in")
    
    return result.data[0]


@router.get("/", response_model=List[CheckInResponse])
def list_checkins(
    user_id: Optional[UUID] = None,
    skip: int = 0,
    limit: int = 100
):
    """List check-ins with optional filtering."""
    supabase = get_supabase()
    
    query = supabase.table("check_ins").select("*")
    
    if user_id:
        query = query.eq("user_id", str(user_id))
    
    result = query.order("created_at", desc=True).range(skip, skip + limit - 1).execute()
    return result.data


@router.get("/{checkin_id}", response_model=CheckInResponse)
def get_checkin(checkin_id: UUID):
    """Get a specific check-in."""
    supabase = get_supabase()
    result = supabase.table("check_ins").select("*").eq("id", str(checkin_id)).execute()
    
    if not result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Check-in not found")
    
    return result.data[0]


@router.put("/{checkin_id}", response_model=CheckInResponse)
def update_checkin(checkin_id: UUID, checkin_update: CheckInUpdate):
    """Update a check-in."""
    supabase = get_supabase()
    
    # Check if check-in exists
    existing = supabase.table("check_ins").select("*").eq("id", str(checkin_id)).execute()
    if not existing.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Check-in not found")
    
    # Update check-in
    update_data = checkin_update.model_dump(exclude_unset=True)
    result = supabase.table("check_ins").update(update_data).eq("id", str(checkin_id)).execute()
    
    return result.data[0]


@router.delete("/{checkin_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_checkin(checkin_id: UUID):
    """Delete a check-in."""
    supabase = get_supabase()
    
    # Check if check-in exists
    existing = supabase.table("check_ins").select("*").eq("id", str(checkin_id)).execute()
    if not existing.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Check-in not found")
    
    # Delete check-in
    supabase.table("check_ins").delete().eq("id", str(checkin_id)).execute()
    return None

