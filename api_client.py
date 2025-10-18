"""
API Client Helper - Use this in your Telegram bot, LLM integration, or scheduler.
This makes it easy to interact with the Personal Coach API.
"""
import requests
from typing import Dict, List, Optional, Any
from datetime import date


class CoachAPIClient:
    """Client for interacting with the Personal Coach API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the API client.
        
        Args:
            base_url: The base URL of your API (change when deployed)
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    # ==================== USERS ====================
    
    def get_or_create_user(self, telegram_id: str, name: str) -> Dict:
        """Get existing user by Telegram ID or create new one.
        
        Use this when a user starts chatting with your Telegram bot.
        
        Args:
            telegram_id: User's Telegram ID
            name: User's name
            
        Returns:
            User data dictionary
            
        Example:
            >>> client = CoachAPIClient()
            >>> user = client.get_or_create_user("12345", "John Doe")
            >>> print(user['id'])  # UUID for future API calls
        """
        # Try to get existing user
        try:
            response = self.session.get(f"{self.base_url}/users/telegram/{telegram_id}")
            if response.status_code == 200:
                return response.json()
        except:
            pass
        
        # Create new user if doesn't exist
        user_data = {
            "telegram_id": telegram_id,
            "name": name
        }
        response = self.session.post(f"{self.base_url}/users/", json=user_data)
        response.raise_for_status()
        return response.json()
    
    def update_user_preferences(self, user_id: str, preferences: Dict) -> Dict:
        """Update user's coaching preferences.
        
        Example:
            >>> client.update_user_preferences(user_id, {
            ...     "check_in_frequency": "daily",
            ...     "preferred_time": "09:00",
            ...     "communication_style": "motivational"
            ... })
        """
        response = self.session.put(
            f"{self.base_url}/users/{user_id}",
            json={"coaching_preferences": preferences}
        )
        response.raise_for_status()
        return response.json()
    
    # ==================== CONVERSATIONS ====================
    
    def save_message(self, user_id: str, role: str, content: str, 
                    check_in_id: Optional[str] = None, metadata: Optional[Dict] = None) -> Dict:
        """Save a conversation message.
        
        Use this to log every message in your chat.
        
        Args:
            user_id: User's UUID
            role: "user", "assistant", or "system"
            content: The message text
            check_in_id: Optional check-in session ID
            metadata: Optional metadata (tokens, model, etc.)
            
        Example:
            >>> # User sends message
            >>> client.save_message(user_id, "user", "I want to learn Python")
            >>> 
            >>> # Assistant responds
            >>> client.save_message(user_id, "assistant", "Great goal! Let's start...",
            ...                    metadata={"model": "gpt-4", "tokens": 50})
        """
        message_data = {
            "user_id": user_id,
            "role": role,
            "content": content,
            "check_in_id": check_in_id,
            "message_metadata": metadata or {}
        }
        response = self.session.post(f"{self.base_url}/conversations/", json=message_data)
        response.raise_for_status()
        return response.json()
    
    def get_conversation_history(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get conversation history for context.
        
        Use this to provide context to your LLM.
        
        Example:
            >>> history = client.get_conversation_history(user_id, limit=10)
            >>> for msg in history:
            ...     print(f"{msg['role']}: {msg['content']}")
        """
        response = self.session.get(
            f"{self.base_url}/conversations/",
            params={"user_id": user_id, "limit": limit}
        )
        response.raise_for_status()
        return response.json()
    
    # ==================== GOALS ====================
    
    def create_goal(self, user_id: str, title: str, description: str = "",
                   category: str = "other", priority: str = "medium",
                   goal_metadata: Optional[Dict] = None) -> Dict:
        """Create a new goal from extracted information.
        
        Use this after your LLM extracts goal information from conversation.
        
        Args:
            user_id: User's UUID
            title: Goal title
            description: Detailed description
            category: "career", "health", "learning", "personal", "other"
            priority: "high", "medium", "low"
            goal_metadata: Additional info (motivation, obstacles, resources)
            
        Example:
            >>> # After LLM extracts: "User wants to learn Python for data science"
            >>> goal = client.create_goal(
            ...     user_id=user_id,
            ...     title="Learn Python for Data Science",
            ...     description="Master Python and transition to data science career",
            ...     category="learning",
            ...     priority="high",
            ...     goal_metadata={
            ...         "motivation": "Career change",
            ...         "obstacles": ["Limited time", "No experience"],
            ...         "timeline": "3 months"
            ...     }
            ... )
            >>> goal_id = goal['id']
        """
        goal_data = {
            "user_id": user_id,
            "title": title,
            "description": description,
            "category": category,
            "priority": priority,
            "goal_metadata": goal_metadata or {}
        }
        response = self.session.post(f"{self.base_url}/goals/", json=goal_data)
        response.raise_for_status()
        return response.json()
    
    def update_goal_progress(self, goal_id: str, progress_percentage: int) -> Dict:
        """Update goal progress.
        
        Example:
            >>> client.update_goal_progress(goal_id, 35)
        """
        response = self.session.put(
            f"{self.base_url}/goals/{goal_id}",
            json={"progress_percentage": progress_percentage}
        )
        response.raise_for_status()
        return response.json()
    
    def get_user_goals(self, user_id: str, status: str = "active") -> List[Dict]:
        """Get user's goals.
        
        Example:
            >>> goals = client.get_user_goals(user_id, status="active")
            >>> for goal in goals:
            ...     print(f"{goal['title']}: {goal['progress_percentage']}%")
        """
        response = self.session.get(
            f"{self.base_url}/goals/",
            params={"user_id": user_id, "status": status}
        )
        response.raise_for_status()
        return response.json()
    
    # ==================== PLANS ====================
    
    def create_plan(self, goal_id: str, user_id: str, plan_content: Dict,
                   generated_by: str = "gpt-4") -> Dict:
        """Save an AI-generated plan.
        
        Use this after your LLM generates a personalized plan.
        
        Args:
            goal_id: Goal UUID
            user_id: User UUID
            plan_content: The plan structure (phases, milestones, etc.)
            generated_by: Model name
            
        Example:
            >>> # After LLM generates a plan
            >>> plan = client.create_plan(
            ...     goal_id=goal_id,
            ...     user_id=user_id,
            ...     plan_content={
            ...         "overview": "3-month Python learning path",
            ...         "phases": [
            ...             {
            ...                 "phase_number": 1,
            ...                 "title": "Python Basics",
            ...                 "duration_weeks": 4,
            ...                 "milestones": ["Complete course", "Build project"]
            ...             }
            ...         ],
            ...         "weekly_time_commitment": "10 hours"
            ...     },
            ...     generated_by="gpt-4"
            ... )
        """
        plan_data = {
            "goal_id": goal_id,
            "user_id": user_id,
            "plan_content": plan_content,
            "generated_by": generated_by
        }
        response = self.session.post(f"{self.base_url}/plans/", json=plan_data)
        response.raise_for_status()
        return response.json()
    
    # ==================== MILESTONES ====================
    
    def create_milestone(self, goal_id: str, title: str, description: str = "",
                        order_index: int = 0, plan_id: Optional[str] = None) -> Dict:
        """Create a milestone for a goal.
        
        Example:
            >>> milestone = client.create_milestone(
            ...     goal_id=goal_id,
            ...     title="Complete Python basics course",
            ...     description="Finish all modules on Codecademy",
            ...     order_index=1
            ... )
        """
        milestone_data = {
            "goal_id": goal_id,
            "title": title,
            "description": description,
            "order_index": order_index,
            "plan_id": plan_id
        }
        response = self.session.post(f"{self.base_url}/milestones/", json=milestone_data)
        response.raise_for_status()
        return response.json()
    
    def complete_milestone(self, milestone_id: str) -> Dict:
        """Mark a milestone as completed.
        
        Example:
            >>> client.complete_milestone(milestone_id)
        """
        response = self.session.put(
            f"{self.base_url}/milestones/{milestone_id}",
            json={"status": "completed"}
        )
        response.raise_for_status()
        return response.json()
    
    def get_goal_milestones(self, goal_id: str) -> List[Dict]:
        """Get all milestones for a goal.
        
        Example:
            >>> milestones = client.get_goal_milestones(goal_id)
        """
        response = self.session.get(
            f"{self.base_url}/milestones/",
            params={"goal_id": goal_id}
        )
        response.raise_for_status()
        return response.json()
    
    # ==================== CHECK-INS ====================
    
    def create_checkin(self, user_id: str, checkin_type: str = "user_initiated",
                      channel: str = "telegram_text", sentiment: str = "neutral",
                      summary: Optional[str] = None, action_items: Optional[List[Dict]] = None) -> Dict:
        """Create a check-in session.
        
        Use this to record coaching sessions.
        
        Args:
            user_id: User UUID
            checkin_type: "user_initiated", "scheduled", "milestone_trigger"
            channel: "telegram_text", "telegram_voice", "call"
            sentiment: "positive", "neutral", "struggling", "unmotivated"
            summary: AI-generated summary of the session
            action_items: List of action items
            
        Example:
            >>> checkin = client.create_checkin(
            ...     user_id=user_id,
            ...     checkin_type="user_initiated",
            ...     sentiment="positive",
            ...     summary="User completed first milestone, very motivated",
            ...     action_items=[
            ...         {"action": "Start next course", "status": "pending"}
            ...     ]
            ... )
            >>> checkin_id = checkin['id']
        """
        checkin_data = {
            "user_id": user_id,
            "type": checkin_type,
            "channel": channel,
            "sentiment": sentiment,
            "conversation_summary": summary,
            "action_items": action_items or []
        }
        response = self.session.post(f"{self.base_url}/checkins/", json=checkin_data)
        response.raise_for_status()
        return response.json()
    
    def update_checkin_summary(self, checkin_id: str, summary: str, 
                              sentiment: str, action_items: List[Dict]) -> Dict:
        """Update check-in with AI-generated summary.
        
        Use this after analyzing the conversation.
        
        Example:
            >>> # After conversation ends, LLM analyzes it
            >>> client.update_checkin_summary(
            ...     checkin_id=checkin_id,
            ...     summary="User struggling with time management but motivated",
            ...     sentiment="struggling",
            ...     action_items=[
            ...         {"action": "Block 1 hour daily for study", "status": "pending"}
            ...     ]
            ... )
        """
        response = self.session.put(
            f"{self.base_url}/checkins/{checkin_id}",
            json={
                "conversation_summary": summary,
                "sentiment": sentiment,
                "action_items": action_items
            }
        )
        response.raise_for_status()
        return response.json()
    
    # ==================== HELPER METHODS ====================
    
    def get_user_context(self, user_id: str) -> Dict:
        """Get complete user context for LLM.
        
        Returns user info, active goals, recent conversations.
        Use this to build context for your LLM prompts.
        
        Example:
            >>> context = client.get_user_context(user_id)
            >>> print(f"User: {context['user']['name']}")
            >>> print(f"Goals: {len(context['goals'])}")
            >>> print(f"Recent messages: {len(context['recent_conversations'])}")
        """
        # Get user
        user_response = self.session.get(f"{self.base_url}/users/{user_id}")
        user = user_response.json()
        
        # Get active goals
        goals_response = self.session.get(
            f"{self.base_url}/goals/",
            params={"user_id": user_id, "status": "active"}
        )
        goals = goals_response.json()
        
        # Get recent conversations
        conv_response = self.session.get(
            f"{self.base_url}/conversations/",
            params={"user_id": user_id, "limit": 20}
        )
        conversations = conv_response.json()
        
        return {
            "user": user,
            "goals": goals,
            "recent_conversations": conversations
        }


# ==================== EXAMPLE USAGE ====================

if __name__ == "__main__":
    # Initialize client
    client = CoachAPIClient("http://localhost:8000")
    
    # Example 1: New user starts chatting
    print("=== Example 1: New User ===")
    user = client.get_or_create_user(
        telegram_id="test_12345",
        name="Test User"
    )
    print(f"User ID: {user['id']}")
    user_id = user['id']
    
    # Example 2: Save conversation
    print("\n=== Example 2: Conversation ===")
    client.save_message(user_id, "user", "I want to learn Python for data science")
    client.save_message(
        user_id, 
        "assistant", 
        "That's a great goal! Let me help you create a structured plan.",
        metadata={"model": "gpt-4", "tokens": 25}
    )
    
    # Example 3: Create goal from extracted info
    print("\n=== Example 3: Create Goal ===")
    goal = client.create_goal(
        user_id=user_id,
        title="Learn Python for Data Science",
        description="Master Python programming and data analysis",
        category="learning",
        priority="high",
        goal_metadata={
            "motivation": "Career transition",
            "obstacles": ["Limited time", "No prior experience"],
            "resources": ["Online courses", "Mentor"]
        }
    )
    print(f"Goal ID: {goal['id']}")
    goal_id = goal['id']
    
    # Example 4: Create AI-generated plan
    print("\n=== Example 4: Create Plan ===")
    plan = client.create_plan(
        goal_id=goal_id,
        user_id=user_id,
        plan_content={
            "overview": "3-month Python learning roadmap",
            "phases": [
                {
                    "phase_number": 1,
                    "title": "Python Fundamentals",
                    "duration_weeks": 4,
                    "milestones": ["Complete basics", "Build 3 projects"]
                },
                {
                    "phase_number": 2,
                    "title": "Data Analysis",
                    "duration_weeks": 4,
                    "milestones": ["Learn Pandas", "Analyze datasets"]
                }
            ],
            "weekly_time_commitment": "10 hours"
        },
        generated_by="gpt-4"
    )
    print(f"Plan ID: {plan['id']}")
    
    # Example 5: Create milestones
    print("\n=== Example 5: Create Milestones ===")
    milestone1 = client.create_milestone(
        goal_id=goal_id,
        title="Complete Python Basics Course",
        description="Finish Codecademy Python course",
        order_index=1
    )
    print(f"Milestone ID: {milestone1['id']}")
    
    # Example 6: Start a check-in
    print("\n=== Example 6: Check-in ===")
    checkin = client.create_checkin(
        user_id=user_id,
        checkin_type="user_initiated",
        channel="telegram_text",
        sentiment="positive"
    )
    print(f"Check-in ID: {checkin['id']}")
    
    # Example 7: Get context for LLM
    print("\n=== Example 7: Get Context ===")
    context = client.get_user_context(user_id)
    print(f"User: {context['user']['name']}")
    print(f"Active Goals: {len(context['goals'])}")
    print(f"Recent Messages: {len(context['recent_conversations'])}")
    
    print("\n✅ All examples completed!")

