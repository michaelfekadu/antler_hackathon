"""Supabase client for database operations via REST API."""
from supabase import create_client, Client
from app.config import get_settings
from typing import Dict, List, Optional

settings = get_settings()

# Create Supabase client
supabase: Client = create_client(settings.supabase_url, settings.supabase_key)


def get_supabase() -> Client:
    """Get Supabase client instance."""
    return supabase

