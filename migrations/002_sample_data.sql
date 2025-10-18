-- Sample Data for AI Personal Coach
-- Run this in Supabase SQL Editor to populate tables with example data

-- Clear existing sample data (optional)
DELETE FROM conversations;
DELETE FROM check_ins;
DELETE FROM milestones;
DELETE FROM plans;
DELETE FROM goals;
DELETE FROM users WHERE telegram_id IN ('test_user_123', 'alice_tel_456', 'bob_tel_789', 'carol_tel_012');

-- Insert Sample Users
INSERT INTO users (id, telegram_id, name, email, timezone, coaching_preferences, onboarding_completed, created_at) VALUES
(
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'alice_tel_456',
    'Alice Johnson',
    'alice.johnson@email.com',
    'America/New_York',
    '{
        "check_in_frequency": "daily",
        "preferred_time": "09:00",
        "communication_style": "supportive",
        "voice_enabled": true
    }'::jsonb,
    true,
    NOW() - INTERVAL '30 days'
),
(
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12',
    'bob_tel_789',
    'Bob Martinez',
    'bob.m@email.com',
    'America/Los_Angeles',
    '{
        "check_in_frequency": "weekly",
        "preferred_time": "18:00",
        "communication_style": "direct",
        "voice_enabled": false
    }'::jsonb,
    true,
    NOW() - INTERVAL '15 days'
),
(
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a13',
    'carol_tel_012',
    'Carol Chen',
    'carol.chen@email.com',
    'Asia/Singapore',
    '{
        "check_in_frequency": "daily",
        "preferred_time": "07:30",
        "communication_style": "motivational",
        "voice_enabled": true
    }'::jsonb,
    false,
    NOW() - INTERVAL '3 days'
);

-- Insert Sample Goals for Alice
INSERT INTO goals (id, user_id, title, description, category, status, priority, target_date, progress_percentage, metadata, created_at) VALUES
(
    'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'Learn Python for Data Science',
    'Master Python programming and data analysis to transition into a data science career within 3 months',
    'learning',
    'active',
    'high',
    CURRENT_DATE + INTERVAL '60 days',
    35,
    '{
        "motivation": "Career transition from marketing to data science",
        "obstacles": ["Limited time due to current job", "No prior programming experience", "Math anxiety"],
        "resources": ["Codecademy Pro subscription", "Mentor from DataCamp", "Study group on Discord"],
        "target_salary": "$80,000",
        "inspiration": "Saw a friend successfully transition"
    }'::jsonb,
    NOW() - INTERVAL '25 days'
),
(
    'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a12',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'Run a Half Marathon',
    'Complete first half marathon by summer',
    'health',
    'active',
    'medium',
    CURRENT_DATE + INTERVAL '90 days',
    20,
    '{
        "motivation": "Get healthier and prove I can do hard things",
        "obstacles": ["Knee pain sometimes", "Early morning runs are hard"],
        "resources": ["Running coach app", "Local running club"],
        "current_distance": "5K",
        "target_time": "under 2 hours"
    }'::jsonb,
    NOW() - INTERVAL '20 days'
);

-- Insert Sample Goals for Bob
INSERT INTO goals (id, user_id, title, description, category, status, priority, target_date, progress_percentage, metadata, created_at) VALUES
(
    'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a13',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12',
    'Get Promoted to Senior Engineer',
    'Achieve senior engineer position at current company',
    'career',
    'active',
    'high',
    CURRENT_DATE + INTERVAL '180 days',
    60,
    '{
        "motivation": "Ready for more responsibility and better compensation",
        "obstacles": ["Need to lead more projects", "Communication skills improvement needed"],
        "resources": ["Manager mentorship", "Leadership training course"],
        "requirements": ["Lead 2 major projects", "Present at team meetings", "Mentor junior devs"],
        "current_level": "Mid-level Engineer II"
    }'::jsonb,
    NOW() - INTERVAL '90 days'
),
(
    'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a14',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12',
    'Learn Spanish',
    'Achieve conversational fluency in Spanish',
    'learning',
    'paused',
    'low',
    CURRENT_DATE + INTERVAL '365 days',
    15,
    '{
        "motivation": "Want to travel to South America",
        "obstacles": ["Hard to practice regularly", "Pronunciation challenges"],
        "resources": ["Duolingo", "Spanish tutor on iTalki"],
        "paused_reason": "Focusing on career goal first"
    }'::jsonb,
    NOW() - INTERVAL '60 days'
);

-- Insert Sample Goals for Carol
INSERT INTO goals (id, user_id, title, description, category, status, priority, target_date, progress_percentage, metadata, created_at) VALUES
(
    'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a15',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a13',
    'Launch My Side Business',
    'Start freelance graphic design business',
    'career',
    'active',
    'high',
    CURRENT_DATE + INTERVAL '45 days',
    10,
    '{
        "motivation": "Want financial independence and creative freedom",
        "obstacles": ["No client base yet", "Pricing strategy unclear", "Time management"],
        "resources": ["Freelancer portfolio template", "Business coach", "Design software"],
        "target_monthly_income": "$2000",
        "services": ["Logo design", "Brand identity", "Social media graphics"]
    }'::jsonb,
    NOW() - INTERVAL '3 days'
);

-- Insert Sample Plans
INSERT INTO plans (id, goal_id, user_id, plan_content, generated_by, version, is_active, created_at) VALUES
(
    'c1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    '{
        "overview": "3-month intensive Python and Data Science learning path with hands-on projects",
        "total_duration_weeks": 12,
        "phases": [
            {
                "phase_number": 1,
                "title": "Python Fundamentals",
                "duration_weeks": 4,
                "description": "Master basic Python syntax, data types, and programming concepts",
                "key_topics": ["Variables & Data Types", "Control Flow", "Functions", "Object-Oriented Programming"],
                "deliverables": ["Complete Codecademy Python course", "Build 3 small CLI projects", "Pass Python basics quiz"],
                "estimated_hours_per_week": 10
            },
            {
                "phase_number": 2,
                "title": "Data Analysis Libraries",
                "duration_weeks": 4,
                "description": "Learn NumPy, Pandas, and Matplotlib for data manipulation and visualization",
                "key_topics": ["NumPy arrays", "Pandas DataFrames", "Data cleaning", "Visualization with Matplotlib"],
                "deliverables": ["Analyze 2 real datasets (Kaggle)", "Create data visualizations", "Write analysis report"],
                "estimated_hours_per_week": 12
            },
            {
                "phase_number": 3,
                "title": "Machine Learning Basics",
                "duration_weeks": 4,
                "description": "Introduction to ML algorithms and scikit-learn",
                "key_topics": ["Supervised learning", "Model evaluation", "Feature engineering", "scikit-learn"],
                "deliverables": ["Build 2 ML models", "Complete capstone project", "Create portfolio"],
                "estimated_hours_per_week": 15
            }
        ],
        "success_metrics": [
            "Complete all phase deliverables",
            "Build portfolio with 5+ projects",
            "Pass technical assessment",
            "Land first interview"
        ],
        "weekly_time_commitment": "10-15 hours",
        "checkpoints": ["Weekly progress reviews", "Bi-weekly mentor sessions"],
        "resources": ["Codecademy Pro", "Kaggle datasets", "YouTube tutorials", "DataCamp mentor"]
    }'::jsonb,
    'gpt-4',
    1,
    true,
    NOW() - INTERVAL '24 days'
),
(
    'c1eebc99-9c0b-4ef8-bb6d-6bb9bd380a12',
    'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a13',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12',
    '{
        "overview": "6-month strategic plan to achieve senior engineer promotion",
        "total_duration_weeks": 24,
        "phases": [
            {
                "phase_number": 1,
                "title": "Technical Leadership",
                "duration_weeks": 8,
                "description": "Lead major technical project and demonstrate architectural thinking",
                "key_actions": ["Propose new architecture for payment system", "Lead implementation team", "Document decisions"],
                "deliverables": ["Successfully launch project", "Present at architecture review"],
                "estimated_hours_per_week": 5
            },
            {
                "phase_number": 2,
                "title": "Communication & Visibility",
                "duration_weeks": 8,
                "description": "Improve communication skills and increase visibility",
                "key_actions": ["Present at team meetings", "Write technical blog posts", "Mentor 2 junior developers"],
                "deliverables": ["Monthly presentations", "3 blog posts", "Positive mentee feedback"],
                "estimated_hours_per_week": 3
            },
            {
                "phase_number": 3,
                "title": "Promotion Preparation",
                "duration_weeks": 8,
                "description": "Gather evidence and make the case for promotion",
                "key_actions": ["Document achievements", "Get peer reviews", "Schedule promotion discussion"],
                "deliverables": ["Promotion packet", "Manager support", "Peer endorsements"],
                "estimated_hours_per_week": 2
            }
        ],
        "success_metrics": ["Lead 2 major projects", "Mentor 2 junior devs", "Positive 360 reviews", "Manager nomination"],
        "key_stakeholders": ["Engineering manager", "Tech lead", "Director of Engineering"]
    }'::jsonb,
    'claude-3',
    1,
    true,
    NOW() - INTERVAL '85 days'
);

-- Insert Sample Milestones for Alice's Python Goal
INSERT INTO milestones (id, goal_id, plan_id, title, description, status, due_date, order_index, completed_at, created_at) VALUES
(
    'd1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'c1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'Complete Python Basics Course',
    'Finish all modules of Codecademy Python course',
    'completed',
    CURRENT_DATE - INTERVAL '10 days',
    1,
    NOW() - INTERVAL '12 days',
    NOW() - INTERVAL '24 days'
),
(
    'd1eebc99-9c0b-4ef8-bb6d-6bb9bd380a12',
    'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'c1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'Build Calculator CLI App',
    'Create a command-line calculator with advanced functions',
    'completed',
    CURRENT_DATE - INTERVAL '5 days',
    2,
    NOW() - INTERVAL '7 days',
    NOW() - INTERVAL '24 days'
),
(
    'd1eebc99-9c0b-4ef8-bb6d-6bb9bd380a13',
    'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'c1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'Build To-Do List App',
    'Create a CLI to-do list app with file persistence',
    'in_progress',
    CURRENT_DATE + INTERVAL '3 days',
    3,
    NULL,
    NOW() - INTERVAL '24 days'
),
(
    'd1eebc99-9c0b-4ef8-bb6d-6bb9bd380a14',
    'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'c1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'Learn Pandas Basics',
    'Complete Pandas tutorial and practice exercises',
    'pending',
    CURRENT_DATE + INTERVAL '15 days',
    4,
    NULL,
    NOW() - INTERVAL '24 days'
),
(
    'd1eebc99-9c0b-4ef8-bb6d-6bb9bd380a15',
    'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'c1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'Analyze First Dataset',
    'Complete full analysis of Titanic dataset from Kaggle',
    'pending',
    CURRENT_DATE + INTERVAL '25 days',
    5,
    NULL,
    NOW() - INTERVAL '24 days'
);

-- Insert Sample Milestones for Bob's Career Goal
INSERT INTO milestones (id, goal_id, plan_id, title, description, status, due_date, order_index, completed_at, created_at) VALUES
(
    'd1eebc99-9c0b-4ef8-bb6d-6bb9bd380a16',
    'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a13',
    'c1eebc99-9c0b-4ef8-bb6d-6bb9bd380a12',
    'Propose Payment System Architecture',
    'Create and present new payment system architecture proposal',
    'completed',
    CURRENT_DATE - INTERVAL '60 days',
    1,
    NOW() - INTERVAL '62 days',
    NOW() - INTERVAL '85 days'
),
(
    'd1eebc99-9c0b-4ef8-bb6d-6bb9bd380a17',
    'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a13',
    'c1eebc99-9c0b-4ef8-bb6d-6bb9bd380a12',
    'Lead Implementation Team',
    'Successfully lead 4-person team to implement new system',
    'completed',
    CURRENT_DATE - INTERVAL '15 days',
    2,
    NOW() - INTERVAL '18 days',
    NOW() - INTERVAL '85 days'
),
(
    'd1eebc99-9c0b-4ef8-bb6d-6bb9bd380a18',
    'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a13',
    'c1eebc99-9c0b-4ef8-bb6d-6bb9bd380a12',
    'Present at Team All-Hands',
    'Give technical presentation at monthly all-hands meeting',
    'in_progress',
    CURRENT_DATE + INTERVAL '5 days',
    3,
    NULL,
    NOW() - INTERVAL '85 days'
),
(
    'd1eebc99-9c0b-4ef8-bb6d-6bb9bd380a19',
    'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a13',
    'c1eebc99-9c0b-4ef8-bb6d-6bb9bd380a12',
    'Mentor Junior Developer',
    'Start mentoring relationship with new junior dev',
    'pending',
    CURRENT_DATE + INTERVAL '30 days',
    4,
    NULL,
    NOW() - INTERVAL '85 days'
);

-- Insert Sample Check-ins for Alice
INSERT INTO check_ins (id, user_id, type, channel, conversation_summary, sentiment, action_items, goals_discussed, created_at) VALUES
(
    'e1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'user_initiated',
    'telegram_text',
    'Alice reported completing the Python basics course ahead of schedule. Very excited about progress. Concerns about time management with full-time job. Discussed strategies for consistent daily practice.',
    'positive',
    '[
        {"action": "Schedule daily 1-hour study blocks before work", "status": "completed", "priority": "high"},
        {"action": "Join Python study group on Discord", "status": "completed", "priority": "medium"},
        {"action": "Set up project GitHub repository", "status": "pending", "priority": "medium"}
    ]'::jsonb,
    '["b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"]'::jsonb,
    NOW() - INTERVAL '12 days'
),
(
    'e1eebc99-9c0b-4ef8-bb6d-6bb9bd380a12',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'scheduled',
    'telegram_text',
    'Weekly check-in. Alice completed calculator app project and started to-do list app. Feeling confident but experiencing some imposter syndrome. Discussed that this is normal and part of the learning journey.',
    'neutral',
    '[
        {"action": "Read article about imposter syndrome in tech", "status": "completed", "priority": "low"},
        {"action": "Complete to-do list app by Friday", "status": "in_progress", "priority": "high"},
        {"action": "Schedule call with DataCamp mentor", "status": "pending", "priority": "medium"}
    ]'::jsonb,
    '["b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"]'::jsonb,
    NOW() - INTERVAL '5 days'
),
(
    'e1eebc99-9c0b-4ef8-bb6d-6bb9bd380a13',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'scheduled',
    'telegram_text',
    'Daily motivation check. Alice worked on to-do app last night. Made good progress but stuck on file I/O. Provided debugging tips and encouragement.',
    'positive',
    '[
        {"action": "Review Python file handling documentation", "status": "completed", "priority": "high"},
        {"action": "Ask study group for help if still stuck", "status": "not_needed", "priority": "low"}
    ]'::jsonb,
    '["b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"]'::jsonb,
    NOW() - INTERVAL '2 days'
);

-- Insert Sample Check-ins for Bob
INSERT INTO check_ins (id, user_id, type, channel, conversation_summary, sentiment, action_items, goals_discussed, created_at) VALUES
(
    'e1eebc99-9c0b-4ef8-bb6d-6bb9bd380a14',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12',
    'user_initiated',
    'telegram_text',
    'Bob successfully completed payment system project! Team launch went smoothly. Received positive feedback from director. Feeling proud and motivated. Discussed next steps for promotion.',
    'positive',
    '[
        {"action": "Schedule 1-on-1 with manager about promotion timeline", "status": "completed", "priority": "high"},
        {"action": "Start drafting technical blog post about project", "status": "in_progress", "priority": "medium"},
        {"action": "Prepare presentation for all-hands meeting", "status": "in_progress", "priority": "high"}
    ]'::jsonb,
    '["b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a13"]'::jsonb,
    NOW() - INTERVAL '18 days'
),
(
    'e1eebc99-9c0b-4ef8-bb6d-6bb9bd380a15',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12',
    'scheduled',
    'telegram_text',
    'Weekly check-in. Bob is nervous about upcoming all-hands presentation. First time presenting to 50+ people. Discussed presentation tips and offered to review slides.',
    'struggling',
    '[
        {"action": "Practice presentation with wife", "status": "completed", "priority": "high"},
        {"action": "Reduce slide count to 10 max", "status": "completed", "priority": "medium"},
        {"action": "Prepare for Q&A session", "status": "in_progress", "priority": "high"},
        {"action": "Do breathing exercises before presentation", "status": "pending", "priority": "low"}
    ]'::jsonb,
    '["b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a13"]'::jsonb,
    NOW() - INTERVAL '7 days'
);

-- Insert Sample Conversations for Alice's most recent check-in
INSERT INTO conversations (id, user_id, check_in_id, role, content, message_metadata, created_at) VALUES
(
    'f1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'e1eebc99-9c0b-4ef8-bb6d-6bb9bd380a13',
    'user',
    'Hey! I worked on my to-do app last night and made good progress! 🎉',
    '{"tokens": 15, "message_type": "text"}'::jsonb,
    NOW() - INTERVAL '2 days'
),
(
    'f1eebc99-9c0b-4ef8-bb6d-6bb9bd380a12',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'e1eebc99-9c0b-4ef8-bb6d-6bb9bd380a13',
    'assistant',
    'That''s fantastic, Alice! I love your enthusiasm! 🌟 Tell me more - what parts did you work on?',
    '{"tokens": 22, "model": "gpt-4", "message_type": "text"}'::jsonb,
    NOW() - INTERVAL '2 days' + INTERVAL '30 seconds'
),
(
    'f1eebc99-9c0b-4ef8-bb6d-6bb9bd380a13',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'e1eebc99-9c0b-4ef8-bb6d-6bb9bd380a13',
    'user',
    'I got the basic CRUD operations working - add, remove, and list tasks. But I''m stuck on saving the tasks to a file so they persist between runs.',
    '{"tokens": 35, "message_type": "text"}'::jsonb,
    NOW() - INTERVAL '2 days' + INTERVAL '1 minute'
),
(
    'f1eebc99-9c0b-4ef8-bb6d-6bb9bd380a14',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'e1eebc99-9c0b-4ef8-bb6d-6bb9bd380a13',
    'assistant',
    'Great progress on the CRUD operations! File I/O can be tricky at first. Are you getting an error message, or are you unsure about the approach?',
    '{"tokens": 35, "model": "gpt-4", "message_type": "text"}'::jsonb,
    NOW() - INTERVAL '2 days' + INTERVAL '1 minute 30 seconds'
),
(
    'f1eebc99-9c0b-4ef8-bb6d-6bb9bd380a15',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'e1eebc99-9c0b-4ef8-bb6d-6bb9bd380a13',
    'user',
    'A bit of both! I tried using open() and write() but I''m not sure how to convert my list of tasks to a format I can save.',
    '{"tokens": 32, "message_type": "text"}'::jsonb,
    NOW() - INTERVAL '2 days' + INTERVAL '2 minutes'
),
(
    'f1eebc99-9c0b-4ef8-bb6d-6bb9bd380a16',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'e1eebc99-9c0b-4ef8-bb6d-6bb9bd380a13',
    'assistant',
    'Ah, I see! You need to serialize your data. Have you learned about the json module in Python? It''s perfect for this - you can convert your list to JSON format and save it to a file. Here''s the approach:\n\n1. Import json module\n2. Use json.dump() to write your list to a file\n3. Use json.load() to read it back\n\nWant to review the Python docs on file handling, or would you like me to point you to a specific tutorial?',
    '{"tokens": 95, "model": "gpt-4", "message_type": "text", "code_snippet": true}'::jsonb,
    NOW() - INTERVAL '2 days' + INTERVAL '2 minutes 45 seconds'
),
(
    'f1eebc99-9c0b-4ef8-bb6d-6bb9bd380a17',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'e1eebc99-9c0b-4ef8-bb6d-6bb9bd380a13',
    'user',
    'Oh! JSON! We covered that briefly in the course. I''ll review the docs on json.dump() and json.load(). Thanks!',
    '{"tokens": 28, "message_type": "text"}'::jsonb,
    NOW() - INTERVAL '2 days' + INTERVAL '3 minutes'
),
(
    'f1eebc99-9c0b-4ef8-bb6d-6bb9bd380a18',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'e1eebc99-9c0b-4ef8-bb6d-6bb9bd380a13',
    'assistant',
    'Perfect! You''ve got this! 💪 If you get stuck after reviewing the docs, your study group is also a great resource. Remember - every developer googles things constantly. That''s part of the process!',
    '{"tokens": 42, "model": "gpt-4", "message_type": "text"}'::jsonb,
    NOW() - INTERVAL '2 days' + INTERVAL '3 minutes 20 seconds'
);

-- Insert Sample Conversations for Bob's presentation anxiety
INSERT INTO conversations (id, user_id, check_in_id, role, content, message_metadata, created_at) VALUES
(
    'f1eebc99-9c0b-4ef8-bb6d-6bb9bd380a21',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12',
    'e1eebc99-9c0b-4ef8-bb6d-6bb9bd380a15',
    'assistant',
    'Hey Bob! How''s the week going? Your all-hands presentation is coming up soon.',
    '{"tokens": 16, "model": "gpt-4", "message_type": "text"}'::jsonb,
    NOW() - INTERVAL '7 days'
),
(
    'f1eebc99-9c0b-4ef8-bb6d-6bb9bd380a22',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12',
    'e1eebc99-9c0b-4ef8-bb6d-6bb9bd380a15',
    'user',
    'Honestly? Pretty nervous. I''ve never presented to this many people before. What if I freeze up or someone asks a question I can''t answer?',
    '{"tokens": 32, "message_type": "text"}'::jsonb,
    NOW() - INTERVAL '7 days' + INTERVAL '1 minute'
),
(
    'f1eebc99-9c0b-4ef8-bb6d-6bb9bd380a23',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12',
    'e1eebc99-9c0b-4ef8-bb6d-6bb9bd380a15',
    'assistant',
    'Those feelings are completely normal, Bob. Even experienced presenters get nervous! Let''s work through this. First - you KNOW this material. You led the entire project. You''re the expert in the room.\n\nSecond - it''s okay to say "I don''t know, let me get back to you" if someone asks something you''re unsure about. That''s professional, not a weakness.\n\nHave you practiced your presentation out loud yet?',
    '{"tokens": 82, "model": "gpt-4", "message_type": "text"}'::jsonb,
    NOW() - INTERVAL '7 days' + INTERVAL '2 minutes'
),
(
    'f1eebc99-9c0b-4ef8-bb6d-6bb9bd380a24',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12',
    'e1eebc99-9c0b-4ef8-bb6d-6bb9bd380a15',
    'user',
    'Not yet. I have 20 slides right now. Is that too many?',
    '{"tokens": 16, "message_type": "text"}'::jsonb,
    NOW() - INTERVAL '7 days' + INTERVAL '3 minutes'
),
(
    'f1eebc99-9c0b-4ef8-bb6d-6bb9bd380a25',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12',
    'e1eebc99-9c0b-4ef8-bb6d-6bb9bd380a15',
    'assistant',
    'For a 15-20 minute presentation? Yes, probably too many. Aim for about 1 slide per minute, max. So 10-15 slides. Quality over quantity!\n\nHere''s your action plan:\n1. Cut down to 10 key slides\n2. Practice out loud - maybe with your wife?\n3. Prepare 2-3 likely questions and your answers\n4. Do some breathing exercises before you go on\n\nYou''ve got this! The hard part (the actual work) is done. This is just sharing what you accomplished. 💪',
    '{"tokens": 110, "model": "gpt-4", "message_type": "text"}'::jsonb,
    NOW() - INTERVAL '7 days' + INTERVAL '4 minutes'
),
(
    'f1eebc99-9c0b-4ef8-bb6d-6bb9bd380a26',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12',
    'e1eebc99-9c0b-4ef8-bb6d-6bb9bd380a15',
    'user',
    'Thanks. That actually helps. I''ll cut it down tonight and practice this weekend.',
    '{"tokens": 18, "message_type": "text"}'::jsonb,
    NOW() - INTERVAL '7 days' + INTERVAL '5 minutes'
);

-- Verify data insertion
SELECT 'Sample data inserted successfully!' as status;
SELECT 'Users created: ' || COUNT(*)::text as users FROM users;
SELECT 'Goals created: ' || COUNT(*)::text as goals FROM goals;
SELECT 'Plans created: ' || COUNT(*)::text as plans FROM plans;
SELECT 'Milestones created: ' || COUNT(*)::text as milestones FROM milestones;
SELECT 'Check-ins created: ' || COUNT(*)::text as checkins FROM check_ins;
SELECT 'Conversations created: ' || COUNT(*)::text as conversations FROM conversations;

