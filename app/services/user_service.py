# app/services/user_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate
from app.core.security import get_password_hash

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create_user(self, user_create: UserCreate):
        existing_user = self.repository.get_by_email(user_create.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este e-mail já está cadastrado."
            )
        
        hashed_password = get_password_hash(user_create.password)
        
        return self.repository.create(user_create, hashed_password)