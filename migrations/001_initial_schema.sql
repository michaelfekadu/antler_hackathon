-- AI-Powered Personal Coach Agent - Database Schema
-- Run this in Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create enum types
CREATE TYPE goal_category AS ENUM ('career', 'health', 'learning', 'personal', 'other');
CREATE TYPE goal_status AS ENUM ('active', 'completed', 'paused', 'abandoned');
CREATE TYPE priority_level AS ENUM ('high', 'medium', 'low');
CREATE TYPE milestone_status AS ENUM ('pending', 'in_progress', 'completed', 'skipped');
CREATE TYPE checkin_type AS ENUM ('scheduled', 'user_initiated', 'milestone_trigger');
CREATE TYPE communication_channel AS ENUM ('telegram_text', 'telegram_voice', 'call');
CREATE TYPE sentiment_type AS ENUM ('positive', 'neutral', 'struggling', 'unmotivated');
CREATE TYPE message_role AS ENUM ('user', 'assistant', 'system');

-- Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    telegram_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    timezone VARCHAR(50) DEFAULT 'UTC',
    coaching_preferences JSONB DEFAULT '{
        "check_in_frequency": "daily",
        "preferred_time": "09:00",
        "communication_style": "motivational",
        "voice_enabled": true
    }'::jsonb,
    onboarding_completed BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Goals Table
CREATE TABLE goals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    category goal_category NOT NULL DEFAULT 'other',
    status goal_status NOT NULL DEFAULT 'active',
    priority priority_level NOT NULL DEFAULT 'medium',
    target_date DATE,
    progress_percentage INTEGER DEFAULT 0 CHECK (progress_percentage >= 0 AND progress_percentage <= 100),
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Plans Table
CREATE TABLE plans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    goal_id UUID NOT NULL REFERENCES goals(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    plan_content JSONB NOT NULL,
    generated_by VARCHAR(100),
    version INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Milestones Table
CREATE TABLE milestones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    goal_id UUID NOT NULL REFERENCES goals(id) ON DELETE CASCADE,
    plan_id UUID REFERENCES plans(id) ON DELETE SET NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    status milestone_status NOT NULL DEFAULT 'pending',
    due_date DATE,
    order_index INTEGER DEFAULT 0,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Check-ins Table
CREATE TABLE check_ins (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type checkin_type NOT NULL DEFAULT 'user_initiated',
    channel communication_channel NOT NULL DEFAULT 'telegram_text',
    conversation_summary TEXT,
    sentiment sentiment_type DEFAULT 'neutral',
    action_items JSONB DEFAULT '[]'::jsonb,
    goals_discussed JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Conversations Table
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    check_in_id UUID REFERENCES check_ins(id) ON DELETE SET NULL,
    role message_role NOT NULL,
    content TEXT NOT NULL,
    message_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_goals_user_id ON goals(user_id);
CREATE INDEX idx_goals_status ON goals(status);
CREATE INDEX idx_plans_goal_id ON plans(goal_id);
CREATE INDEX idx_plans_user_id ON plans(user_id);
CREATE INDEX idx_milestones_goal_id ON milestones(goal_id);
CREATE INDEX idx_milestones_status ON milestones(status);
CREATE INDEX idx_check_ins_user_id ON check_ins(user_id);
CREATE INDEX idx_check_ins_created_at ON check_ins(created_at DESC);
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_check_in_id ON conversations(check_in_id);
CREATE INDEX idx_conversations_created_at ON conversations(created_at DESC);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_goals_updated_at BEFORE UPDATE ON goals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_plans_updated_at BEFORE UPDATE ON plans
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_milestones_updated_at BEFORE UPDATE ON milestones
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_check_ins_updated_at BEFORE UPDATE ON check_ins
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert some sample data for testing
INSERT INTO users (telegram_id, name, email, onboarding_completed) VALUES
('test_user_123', 'Test User', 'test@example.com', true);

COMMENT ON TABLE users IS 'Stores user profiles and coaching preferences';
COMMENT ON TABLE goals IS 'User goals and objectives';
COMMENT ON TABLE plans IS 'AI-generated personalized growth plans';
COMMENT ON TABLE milestones IS 'Trackable milestones for goals';
COMMENT ON TABLE check_ins IS 'Check-in sessions with users';
COMMENT ON TABLE conversations IS 'Full conversation history';

