# app/main.py
from fastapi import FastAPI
from app.db.base import Base
from app.db.database import engine
from app.api.v1 import user_router, auth_router

# Esta linha cria a tabela "users" no seu banco de dados se ela não existir
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Minha API",
    description="Template com autenticação JWT.",
    version="1.0.0"
)

# Inclui os roteadores da API
app.include_router(auth_router.router, prefix="/api/v1")
app.include_router(user_router.router, prefix="/api/v1")
