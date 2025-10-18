"""Milestone management endpoints using Supabase REST API."""
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from app.supabase_client import get_supabase
from app.schemas import MilestoneCreate, MilestoneUpdate, MilestoneResponse
from app.utils import convert_uuids_to_strings

router = APIRouter(prefix="/milestones", tags=["milestones"])


@router.post("/", response_model=MilestoneResponse, status_code=status.HTTP_201_CREATED)
def create_milestone(milestone: MilestoneCreate):
    """Create a new milestone."""
    supabase = get_supabase()
    
    # Verify goal exists
    goal_check = supabase.table("goals").select("id").eq("id", str(milestone.goal_id)).execute()
    if not goal_check.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    
    # Create milestone
    milestone_data = convert_uuids_to_strings(milestone.model_dump())
    result = supabase.table("milestones").insert(milestone_data).execute()
    if not result.data:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create milestone")
    
    return result.data[0]


@router.get("/", response_model=List[MilestoneResponse])
def list_milestones(
    goal_id: Optional[UUID] = None,
    status_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    """List milestones with optional filtering."""
    supabase = get_supabase()
    
    query = supabase.table("milestones").select("*")
    
    if goal_id:
        query = query.eq("goal_id", str(goal_id))
    if status_filter:
        query = query.eq("status", status_filter)
    
    result = query.order("order_index").range(skip, skip + limit - 1).execute()
    return result.data


@router.get("/{milestone_id}", response_model=MilestoneResponse)
def get_milestone(milestone_id: UUID):
    """Get a specific milestone."""
    supabase = get_supabase()
    result = supabase.table("milestones").select("*").eq("id", str(milestone_id)).execute()
    
    if not result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Milestone not found")
    
    return result.data[0]


@router.put("/{milestone_id}", response_model=MilestoneResponse)
def update_milestone(milestone_id: UUID, milestone_update: MilestoneUpdate):
    """Update a milestone."""
    supabase = get_supabase()
    
    # Check if milestone exists
    existing = supabase.table("milestones").select("*").eq("id", str(milestone_id)).execute()
    if not existing.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Milestone not found")
    
    # Prepare update data
    update_data = milestone_update.model_dump(exclude_unset=True)
    
    # Auto-set completed_at when status changes to completed
    if "status" in update_data and update_data["status"] == "completed":
        if "completed_at" not in update_data or not update_data["completed_at"]:
            update_data["completed_at"] = datetime.utcnow().isoformat()
    
    # Update milestone
    result = supabase.table("milestones").update(update_data).eq("id", str(milestone_id)).execute()
    
    return result.data[0]


@router.delete("/{milestone_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_milestone(milestone_id: UUID):
    """Delete a milestone."""
    supabase = get_supabase()
    
    # Check if milestone exists
    existing = supabase.table("milestones").select("*").eq("id", str(milestone_id)).execute()
    if not existing.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Milestone not found")
    
    # Delete milestone
    supabase.table("milestones").delete().eq("id", str(milestone_id)).execute()
    return None

