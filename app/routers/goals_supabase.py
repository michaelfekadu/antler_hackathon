"""Goal management endpoints using Supabase REST API."""
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from uuid import UUID

from app.supabase_client import get_supabase
from app.schemas import GoalCreate, GoalUpdate, GoalResponse
from app.utils import convert_uuids_to_strings

router = APIRouter(prefix="/goals", tags=["goals"])


@router.post("/", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
def create_goal(goal: GoalCreate):
    """Create a new goal."""
    supabase = get_supabase()
    
    # Verify user exists
    user_check = supabase.table("users").select("id").eq("id", str(goal.user_id)).execute()
    if not user_check.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Create goal - map goal_metadata to metadata for database
    goal_data = goal.model_dump()
    if 'goal_metadata' in goal_data:
        goal_data['metadata'] = goal_data.pop('goal_metadata')
    
    # Convert UUIDs to strings for JSON serialization
    goal_data = convert_uuids_to_strings(goal_data)
    
    result = supabase.table("goals").insert(goal_data).execute()
    if not result.data:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create goal")
    
    # Map metadata back to goal_metadata for response
    response_data = result.data[0]
    if 'metadata' in response_data:
        response_data['goal_metadata'] = response_data['metadata']
    
    return response_data


@router.get("/", response_model=List[GoalResponse])
def list_goals(
    user_id: Optional[UUID] = None,
    status_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    """List goals with optional filtering."""
    supabase = get_supabase()
    
    query = supabase.table("goals").select("*")
    
    if user_id:
        query = query.eq("user_id", str(user_id))
    if status_filter:
        query = query.eq("status", status_filter)
    
    result = query.range(skip, skip + limit - 1).execute()
    
    # Map metadata to goal_metadata for all results
    for goal in result.data:
        if 'metadata' in goal:
            goal['goal_metadata'] = goal['metadata']
    
    return result.data


@router.get("/{goal_id}", response_model=GoalResponse)
def get_goal(goal_id: UUID):
    """Get a specific goal."""
    supabase = get_supabase()
    result = supabase.table("goals").select("*").eq("id", str(goal_id)).execute()
    
    if not result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    
    # Map metadata to goal_metadata
    response_data = result.data[0]
    if 'metadata' in response_data:
        response_data['goal_metadata'] = response_data['metadata']
    
    return response_data


@router.put("/{goal_id}", response_model=GoalResponse)
def update_goal(goal_id: UUID, goal_update: GoalUpdate):
    """Update a goal."""
    supabase = get_supabase()
    
    # Check if goal exists
    existing = supabase.table("goals").select("*").eq("id", str(goal_id)).execute()
    if not existing.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    
    # Update goal - map goal_metadata to metadata
    update_data = goal_update.model_dump(exclude_unset=True)
    if 'goal_metadata' in update_data:
        update_data['metadata'] = update_data.pop('goal_metadata')
    
    result = supabase.table("goals").update(update_data).eq("id", str(goal_id)).execute()
    
    # Map metadata back to goal_metadata
    response_data = result.data[0]
    if 'metadata' in response_data:
        response_data['goal_metadata'] = response_data['metadata']
    
    return response_data


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(goal_id: UUID):
    """Delete a goal."""
    supabase = get_supabase()
    
    # Check if goal exists
    existing = supabase.table("goals").select("*").eq("id", str(goal_id)).execute()
    if not existing.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    
    # Delete goal
    supabase.table("goals").delete().eq("id", str(goal_id)).execute()
    return None

