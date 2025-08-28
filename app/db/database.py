from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings # Importa as configurações

# Cria a "engine" de conexão com o banco de dados
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,      # Verifica se a conexão está ativa antes de cada uso
    pool_recycle=300,        # Recicla (fecha e reabre) conexões ociosas a cada 300s (5 minutos)
    pool_size=5,             # Número de conexões para manter no pool
    max_overflow=10          # Número de conexões extras que podem ser abertas
)

# Cria uma classe SessionLocal que será usada para criar sessões com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função de dependência para ser usada nas rotas da API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()