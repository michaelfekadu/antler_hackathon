"""Conversation history endpoints using Supabase REST API."""
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from uuid import UUID

from app.supabase_client import get_supabase
from app.schemas import ConversationCreate, ConversationResponse
from app.utils import convert_uuids_to_strings

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("/", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
def create_conversation(conversation: ConversationCreate):
    """Create a new conversation message."""
    supabase = get_supabase()
    
    # Verify user exists
    user_check = supabase.table("users").select("id").eq("id", str(conversation.user_id)).execute()
    if not user_check.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Create conversation
    conversation_data = convert_uuids_to_strings(conversation.model_dump())
    result = supabase.table("conversations").insert(conversation_data).execute()
    if not result.data:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create conversation")
    
    return result.data[0]


@router.get("/", response_model=List[ConversationResponse])
def list_conversations(
    user_id: Optional[UUID] = None,
    check_in_id: Optional[UUID] = None,
    skip: int = 0,
    limit: int = 100
):
    """List conversation messages with optional filtering."""
    supabase = get_supabase()
    
    query = supabase.table("conversations").select("*")
    
    if user_id:
        query = query.eq("user_id", str(user_id))
    if check_in_id:
        query = query.eq("check_in_id", str(check_in_id))
    
    result = query.order("created_at", desc=False).range(skip, skip + limit - 1).execute()
    return result.data


@router.get("/{conversation_id}", response_model=ConversationResponse)
def get_conversation(conversation_id: UUID):
    """Get a specific conversation message."""
    supabase = get_supabase()
    result = supabase.table("conversations").select("*").eq("id", str(conversation_id)).execute()
    
    if not result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    
    return result.data[0]


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(conversation_id: UUID):
    """Delete a conversation message."""
    supabase = get_supabase()
    
    # Check if conversation exists
    existing = supabase.table("conversations").select("*").eq("id", str(conversation_id)).execute()
    if not existing.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    
    # Delete conversation
    supabase.table("conversations").delete().eq("id", str(conversation_id)).execute()
    return None

