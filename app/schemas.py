"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from uuid import UUID
from enum import Enum


# Enum types
class GoalCategory(str, Enum):
    career = "career"
    health = "health"
    learning = "learning"
    personal = "personal"
    other = "other"


class GoalStatus(str, Enum):
    active = "active"
    completed = "completed"
    paused = "paused"
    abandoned = "abandoned"


class PriorityLevel(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class MilestoneStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    skipped = "skipped"


class CheckInType(str, Enum):
    scheduled = "scheduled"
    user_initiated = "user_initiated"
    milestone_trigger = "milestone_trigger"


class CommunicationChannel(str, Enum):
    telegram_text = "telegram_text"
    telegram_voice = "telegram_voice"
    call = "call"


class SentimentType(str, Enum):
    positive = "positive"
    neutral = "neutral"
    struggling = "struggling"
    unmotivated = "unmotivated"


class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"


# User Schemas
class UserBase(BaseModel):
    telegram_id: str
    name: str
    email: Optional[str] = None
    timezone: str = "UTC"
    coaching_preferences: Optional[Dict[str, Any]] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    timezone: Optional[str] = None
    coaching_preferences: Optional[Dict[str, Any]] = None
    onboarding_completed: Optional[bool] = None


class UserResponse(UserBase):
    id: UUID
    onboarding_completed: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Goal Schemas
class GoalBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: GoalCategory = GoalCategory.other
    status: GoalStatus = GoalStatus.active
    priority: PriorityLevel = PriorityLevel.medium
    target_date: Optional[date] = None
    progress_percentage: int = Field(default=0, ge=0, le=100)
    goal_metadata: Optional[Dict[str, Any]] = None


class GoalCreate(GoalBase):
    user_id: UUID


class GoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[GoalCategory] = None
    status: Optional[GoalStatus] = None
    priority: Optional[PriorityLevel] = None
    target_date: Optional[date] = None
    progress_percentage: Optional[int] = Field(None, ge=0, le=100)
    goal_metadata: Optional[Dict[str, Any]] = None


class GoalResponse(GoalBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Plan Schemas
class PlanBase(BaseModel):
    plan_content: Dict[str, Any]
    generated_by: Optional[str] = None
    version: int = 1
    is_active: bool = True


class PlanCreate(PlanBase):
    goal_id: UUID
    user_id: UUID


class PlanUpdate(BaseModel):
    plan_content: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class PlanResponse(PlanBase):
    id: UUID
    goal_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Milestone Schemas
class MilestoneBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: MilestoneStatus = MilestoneStatus.pending
    due_date: Optional[date] = None
    order_index: int = 0


class MilestoneCreate(MilestoneBase):
    goal_id: UUID
    plan_id: Optional[UUID] = None


class MilestoneUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[MilestoneStatus] = None
    due_date: Optional[date] = None
    order_index: Optional[int] = None
    completed_at: Optional[datetime] = None


class MilestoneResponse(MilestoneBase):
    id: UUID
    goal_id: UUID
    plan_id: Optional[UUID]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# CheckIn Schemas
class CheckInBase(BaseModel):
    type: CheckInType = CheckInType.user_initiated
    channel: CommunicationChannel = CommunicationChannel.telegram_text
    conversation_summary: Optional[str] = None
    sentiment: Optional[SentimentType] = SentimentType.neutral
    action_items: Optional[List[Dict[str, Any]]] = []
    goals_discussed: Optional[List[str]] = []


class CheckInCreate(CheckInBase):
    user_id: UUID


class CheckInUpdate(BaseModel):
    conversation_summary: Optional[str] = None
    sentiment: Optional[SentimentType] = None
    action_items: Optional[List[Dict[str, Any]]] = None
    goals_discussed: Optional[List[str]] = None


class CheckInResponse(CheckInBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Conversation Schemas
class ConversationBase(BaseModel):
    role: MessageRole
    content: str
    message_metadata: Optional[Dict[str, Any]] = {}


class ConversationCreate(ConversationBase):
    user_id: UUID
    check_in_id: Optional[UUID] = None


class ConversationResponse(ConversationBase):
    id: UUID
    user_id: UUID
    check_in_id: Optional[UUID]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Composite response with related data
class GoalWithDetails(GoalResponse):
    milestones: List[MilestoneResponse] = []
    active_plan: Optional[PlanResponse] = None


class UserWithGoals(UserResponse):
    goals: List[GoalResponse] = []

