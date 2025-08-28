# app/api/v1/user_router.py

# ... (imports existentes)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserPublic
from app.services.user_service import UserService
from app.db.database import get_db

# Importe a dependência de segurança e o modelo do usuário
from app.core.security import get_current_user
from app.models.user_model import User

router = APIRouter(prefix="/users", tags=["Users"])

# Rota de criação de usuário (PÚBLICA)
@router.post("/", response_model=UserPublic, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.create_user(user_create=user)


# Rota para obter o usuário logado (PROTEGIDA)
@router.get("/me", response_model=UserPublic)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Retorna os dados do usuário que está autenticado.
    """
    return current_user