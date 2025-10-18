"""Plan management endpoints using Supabase REST API."""
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from uuid import UUID

from app.supabase_client import get_supabase
from app.schemas import PlanCreate, PlanUpdate, PlanResponse
from app.utils import convert_uuids_to_strings

router = APIRouter(prefix="/plans", tags=["plans"])


@router.post("/", response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
def create_plan(plan: PlanCreate):
    """Create a new plan for a goal."""
    supabase = get_supabase()
    
    # Verify goal exists
    goal_check = supabase.table("goals").select("id").eq("id", str(plan.goal_id)).execute()
    if not goal_check.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    
    # Create plan
    plan_data = convert_uuids_to_strings(plan.model_dump())
    result = supabase.table("plans").insert(plan_data).execute()
    if not result.data:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create plan")
    
    return result.data[0]


@router.get("/", response_model=List[PlanResponse])
def list_plans(
    user_id: Optional[UUID] = None,
    goal_id: Optional[UUID] = None,
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100
):
    """List plans with optional filtering."""
    supabase = get_supabase()
    
    query = supabase.table("plans").select("*")
    
    if user_id:
        query = query.eq("user_id", str(user_id))
    if goal_id:
        query = query.eq("goal_id", str(goal_id))
    if is_active is not None:
        query = query.eq("is_active", is_active)
    
    result = query.range(skip, skip + limit - 1).execute()
    return result.data


@router.get("/{plan_id}", response_model=PlanResponse)
def get_plan(plan_id: UUID):
    """Get a specific plan."""
    supabase = get_supabase()
    result = supabase.table("plans").select("*").eq("id", str(plan_id)).execute()
    
    if not result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    
    return result.data[0]


@router.put("/{plan_id}", response_model=PlanResponse)
def update_plan(plan_id: UUID, plan_update: PlanUpdate):
    """Update a plan."""
    supabase = get_supabase()
    
    # Check if plan exists
    existing = supabase.table("plans").select("*").eq("id", str(plan_id)).execute()
    if not existing.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    
    # Update plan
    update_data = plan_update.model_dump(exclude_unset=True)
    result = supabase.table("plans").update(update_data).eq("id", str(plan_id)).execute()
    
    return result.data[0]


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plan(plan_id: UUID):
    """Delete a plan."""
    supabase = get_supabase()
    
    # Check if plan exists
    existing = supabase.table("plans").select("*").eq("id", str(plan_id)).execute()
    if not existing.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    
    # Delete plan
    supabase.table("plans").delete().eq("id", str(plan_id)).execute()
    return None

