# app/core/security.py
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.schemas.token_schema import TokenData
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository

# ------------------- Configuração de Senhas -------------------

# Define o contexto de criptografia, usando o algoritmo bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para verificar se uma senha em texto plano corresponde a uma senha hasheada
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Função para gerar o hash de uma senha
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# ------------------- Configuração do JWT -------------------

# Define o esquema de autenticação. "tokenUrl" aponta para o nosso endpoint de login.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

# Função para criar um novo token de acesso (JWT)
def create_access_token(data: dict):
    to_encode = data.copy()
    # Define o tempo de expiração do token
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Gera o token JWT
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Função para verificar o token JWT e obter o usuário atual (DEPENDÊNCIA)
def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodifica o token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    # Busca o usuário no banco de dados
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user