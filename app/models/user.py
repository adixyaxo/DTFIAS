# app/models/user.py
"""
User model re-export mapping directly to Profile (Supabase Auth 1:1).
"""
from app.models.auth import Profile, Profile as User

__all__ = ["User", "Profile"]