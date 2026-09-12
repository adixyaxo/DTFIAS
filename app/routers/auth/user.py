from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserBase
from engine.services.core.user_service import UserService
from infrastructure.database.postgres.repositories.user_repository import PostgresUserRepository
from infrastructure.security.authorization.rbac import require_role_in

router = APIRouter(
    prefix="/api/users",
    tags=["api_users"],
    dependencies=[Depends(require_role_in(["SUPER_ADMIN", "HQ_ADMIN"]))],
)

DbDep = Annotated[AsyncSession, Depends(get_db)]

def get_user_service(db: DbDep) -> UserService:
    return UserService(PostgresUserRepository(db))

UserServiceDep = Annotated[UserService, Depends(get_user_service)]


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: UUID, service: UserServiceDep):
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, service: UserServiceDep):
    db_user = await service.get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # In a real app we'd hash the password here before saving
    from infrastructure.security.authentication.passwords import hash_password
    profile_data = user.model_dump(exclude={"password"})
    
    # Normally user creation goes through a proper sign-up flow, 
    # but here we're maintaining the existing endpoint structure.
    # Note: Supabase auth usually handles the actual credential creation,
    # and we just sync the profile.
    created = await service.register_user(profile_data)
    return created
