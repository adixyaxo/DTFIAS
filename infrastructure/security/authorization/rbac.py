from typing import List, Callable
from fastapi import HTTPException, status, Depends
# from app.dependencies.auth import get_current_user
# from engine.domain.users.user import User

# Mock dependency for scaffolding
async def get_current_user_mock():
    # In a real app, this retrieves the user from session/token
    return {"username": "test_user", "roles": [{"name": "maitri_operator"}]}

def require_role(required_role: str) -> Callable:
    """
    Dependency generator that checks if the current user has the required role.
    """
    async def role_checker(user: dict = Depends(get_current_user_mock)):
        user_roles = [role.get("name") for role in user.get("roles", [])]
        if required_role not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Requires role: {required_role}"
            )
        return user
    return role_checker

def require_role_in(*required_roles: str) -> Callable:
    """
    Dependency generator that checks if the current user has AT LEAST ONE of the required roles.
    """
    async def role_checker(user: dict = Depends(get_current_user_mock)):
        user_roles = [role.get("name") for role in user.get("roles", [])]
        if not any(role in user_roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Requires one of: {', '.join(required_roles)}"
            )
        return user
    return role_checker
