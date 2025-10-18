# AI Personal Coach API

Backend API for AI-powered personal coaching with Telegram integration.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Create `.env` file:
```bash
SUPABASE_URL=https://cqmorgaahmuyxqetxmcd.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNxbW9yZ2FhaG11eXhxZXR4bWNkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA3NDQ2NDksImV4cCI6MjA3NjMyMDY0OX0.iLaA4bF_PqYO5dRdtU2GB_wyyaSVJhipDV5HffOXMv0
API_HOST=0.0.0.0
API_PORT=8000
```

### 3. Set Up Database
Run the SQL migration in Supabase:
1. Go to https://app.supabase.com/project/cqmorgaahmuyxqetxmcd/sql
2. Copy contents of `migrations/001_initial_schema.sql`
3. Paste and run in SQL Editor

Optional - Add sample data: Run `migrations/002_sample_data.sql`

### 4. Start Server
```bash
python3 -m app.main
```

API will be available at: http://localhost:8000

### 5. Test It
```bash
python3 quick_test.py
```

View API docs: http://localhost:8000/docs

---

## 📊 Database Schema

### Core Tables
- **users** - User profiles with Telegram ID and coaching preferences
- **goals** - User goals with metadata (motivation, obstacles, resources)
- **plans** - AI-generated personalized plans (JSONB format)
- **milestones** - Trackable sub-goals with progress
- **check_ins** - Coaching sessions with sentiment analysis
- **conversations** - Full message history for AI context

---

## 🔌 API Endpoints

### Users
- `POST /users/` - Create user
- `GET /users/telegram/{telegram_id}` - Get user by Telegram ID
- `GET /users/{user_id}` - Get user by ID
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Goals
- `POST /goals/` - Create goal
- `GET /goals/?user_id={id}` - List user's goals
- `GET /goals/{goal_id}` - Get specific goal
- `PUT /goals/{goal_id}` - Update goal (including progress)
- `DELETE /goals/{goal_id}` - Delete goal

### Plans
- `POST /plans/` - Create AI-generated plan
- `GET /plans/?goal_id={id}` - List plans for goal
- `GET /plans/{plan_id}` - Get specific plan
- `PUT /plans/{plan_id}` - Update plan
- `DELETE /plans/{plan_id}` - Delete plan

### Milestones
- `POST /milestones/` - Create milestone
- `GET /milestones/?goal_id={id}` - List milestones for goal
- `GET /milestones/{milestone_id}` - Get specific milestone
- `PUT /milestones/{milestone_id}` - Update milestone (auto-completes)
- `DELETE /milestones/{milestone_id}` - Delete milestone

### Conversations
- `POST /conversations/` - Save message
- `GET /conversations/?user_id={id}` - Get conversation history
- `DELETE /conversations/{conversation_id}` - Delete message

### Check-ins
- `POST /checkins/` - Create check-in session
- `GET /checkins/?user_id={id}` - List user's check-ins
- `PUT /checkins/{checkin_id}` - Update check-in
- `DELETE /checkins/{checkin_id}` - Delete check-in

---

## 💻 Integration Guide

### Using the Python Client

```python
from api_client import CoachAPIClient

# Initialize
client = CoachAPIClient("http://localhost:8000")

# 1. Get or create user (from Telegram)
user = client.get_or_create_user(
    telegram_id="123456789",
    name="John Doe"
)

# 2. Save conversation
client.save_message(user['id'], "user", "I want to learn Python")
client.save_message(user['id'], "assistant", "Great! Let's create a plan")

# 3. Get conversation history (for LLM context)
history = client.get_conversation_history(user['id'], limit=10)

# 4. Create goal (from LLM extraction)
goal = client.create_goal(
    user_id=user['id'],
    title="Learn Python for Data Science",
    description="Master Python and data analysis",
    category="learning",
    priority="high",
    goal_metadata={
        "motivation": "Career change",
        "obstacles": ["Limited time", "No experience"],
        "timeline": "3 months"
    }
)

# 5. Create AI-generated plan
plan = client.create_plan(
    goal_id=goal['id'],
    user_id=user['id'],
    plan_content={
        "overview": "3-month learning roadmap",
        "phases": [
            {
                "phase_number": 1,
                "title": "Python Basics",
                "duration_weeks": 4,
                "milestones": ["Complete course", "Build 3 projects"]
            }
        ]
    },
    generated_by="gpt-4"
)

# 6. Create milestones
milestone = client.create_milestone(
    goal_id=goal['id'],
    title="Complete Python Basics Course",
    order_index=1
)

# 7. Update progress
client.update_goal_progress(goal['id'], 25)
client.complete_milestone(milestone['id'])

# 8. Create check-in
checkin = client.create_checkin(
    user_id=user['id'],
    sentiment="positive",
    summary="User completed first course, very motivated"
)
```

### Key Workflows

**Telegram Bot Flow:**
```
1. User sends message → get_or_create_user()
2. Save message → save_message()
3. Get context → get_conversation_history()
4. Call LLM with context
5. Save response → save_message()
```

**Goal Intake Flow:**
```
1. Have conversation with user
2. LLM extracts goal info
3. Create goal → create_goal()
4. Generate plan → create_plan()
5. Create milestones → create_milestone()
```

**Check-in Flow:**
```
1. Start session → create_checkin()
2. Save messages → save_message()
3. LLM analyzes conversation
4. Update with summary → update_checkin_summary()
5. Update goal progress → update_goal_progress()
```

---

## 📦 Data Formats

### Goal Metadata (Flexible JSONB)
```json
{
  "motivation": "Why this goal matters",
  "obstacles": ["Time", "Experience"],
  "resources": ["Course", "Mentor"],
  "timeline": "3 months",
  "any_custom_field": "value"
}
```

### Plan Content (AI-Generated)
```json
{
  "overview": "Plan description",
  "phases": [
    {
      "phase_number": 1,
      "title": "Phase name",
      "duration_weeks": 4,
      "milestones": ["Milestone 1", "Milestone 2"]
    }
  ],
  "weekly_time_commitment": "10 hours",
  "success_metrics": ["Metric 1", "Metric 2"]
}
```

### Coaching Preferences
```json
{
  "check_in_frequency": "daily",
  "preferred_time": "09:00",
  "communication_style": "motivational",
  "voice_enabled": true
}
```

---

## 🏗️ Project Structure

```
antler_hackathon/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── supabase_client.py   # Supabase connection
│   ├── schemas.py           # Pydantic models
│   ├── utils.py             # Helper functions
│   └── routers/             # API endpoints
│       ├── users_supabase.py
│       ├── goals_supabase.py
│       ├── plans_supabase.py
│       ├── milestones_supabase.py
│       ├── conversations_supabase.py
│       └── checkins_supabase.py
├── migrations/
│   ├── 001_initial_schema.sql   # Database schema
│   └── 002_sample_data.sql      # Sample data
├── api_client.py            # Python client library
├── quick_test.py            # API test script
├── requirements.txt         # Dependencies
└── README.md               # This file
```

---

## 🔧 Development

### Run server with auto-reload
```bash
python3 -m app.main
```

### Test all endpoints
```bash
python3 quick_test.py
```

### View API documentation
```
http://localhost:8000/docs        # Swagger UI
http://localhost:8000/redoc       # ReDoc
```

### View data in Supabase
```
https://app.supabase.com/project/cqmorgaahmuyxqetxmcd/editor
```

---

## 🎯 For Your Team

### Building Telegram Bot?
- Use `client.get_or_create_user(telegram_id, name)`
- Save all messages with `client.save_message()`
- Get history with `client.get_conversation_history()`

### Building LLM Integration?
- Get context with `client.get_user_context(user_id)`
- Extract goal info and save with `client.create_goal()`
- Generate plans and save with `client.create_plan()`

### Building Scheduler?
- Query users: `client.get_user_context(user_id)`
- Check preferences in user's `coaching_preferences`
- Create scheduled check-ins with `client.create_checkin()`

---

## 📝 API Client Methods

**Users:**
- `get_or_create_user(telegram_id, name)`
- `update_user_preferences(user_id, preferences)`

**Conversations:**
- `save_message(user_id, role, content, check_in_id, metadata)`
- `get_conversation_history(user_id, limit)`

**Goals:**
- `create_goal(user_id, title, description, category, priority, goal_metadata)`
- `update_goal_progress(goal_id, progress_percentage)`
- `get_user_goals(user_id, status)`

**Plans:**
- `create_plan(goal_id, user_id, plan_content, generated_by)`

**Milestones:**
- `create_milestone(goal_id, title, description, order_index)`
- `complete_milestone(milestone_id)`
- `get_goal_milestones(goal_id)`

**Check-ins:**
- `create_checkin(user_id, type, channel, sentiment)`
- `update_checkin_summary(checkin_id, summary, sentiment, action_items)`

**Context:**
- `get_user_context(user_id)` - Returns user, goals, and conversation history

---

## 🚀 Deployment

### Environment Variables
```bash
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
API_HOST=0.0.0.0
API_PORT=8000
```

### Quick Deploy Options
- **Railway**: Connect GitHub repo, auto-deploys
- **Render**: Free tier available
- **Fly.io**: Global edge deployment

---

## ✅ Testing

**Quick test (7 operations):**
```bash
python3 quick_test.py
```

**Interactive testing:**
Open http://localhost:8000/docs and test endpoints directly

**View results:**
Check Supabase dashboard to see data created

---

## 🎯 Built For Hackathon

- ✅ Fast setup (5 minutes)
- ✅ No database configuration needed
- ✅ Auto-generated API docs
- ✅ Modular architecture
- ✅ Team-ready endpoints
- ✅ Sample data included

---

## 📄 License

MIT License - Built for Antler Hackathon
