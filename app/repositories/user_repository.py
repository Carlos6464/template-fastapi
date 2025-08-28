# app/repositories/user_repository.py
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user_create: UserCreate, hashed_password: str) -> User:
        db_user = User(email=user_create.email, hashed_password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user