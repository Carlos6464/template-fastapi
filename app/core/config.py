# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator, Field
from typing import Optional

class Settings(BaseSettings):
    # Carrega as variáveis de ambiente do ficheiro .env
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # --- Configurações de Segurança e JWT ---
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # --- Lógica de Conexão com a Base de Dados ---

    # O dialeto é sempre obrigatório
    DB_DIALECT: str = Field(..., description="Dialeto da base de dados: 'postgresql' ou 'mysql'")

    # String de conexão completa (usada para o NeonDB/PostgreSQL)
    DATABASE_URL: Optional[str] = None

    # Partes individuais (usadas para o MySQL local)
    DB_HOST: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_NAME: Optional[str] = None
    DB_PORT: Optional[int] = None

    # Esta variável será CONSTRUÍDA a partir das variáveis acima
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @model_validator(mode='after')
    def build_database_uri(self) -> 'Settings':
        """
        Constrói a URI de conexão com a base de dados dinamicamente.
        """
        if self.DB_DIALECT == "postgresql":
            if not self.DATABASE_URL:
                raise ValueError("Para o dialeto 'postgresql', a DATABASE_URL deve ser definida no ficheiro .env")
            self.SQLALCHEMY_DATABASE_URI = self.DATABASE_URL
        
        elif self.DB_DIALECT == "mysql":
            required_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME', 'DB_PORT']
            if not all(getattr(self, var) for var in required_vars):
                raise ValueError("Para o dialeto 'mysql', todas as variáveis DB_* devem ser definidas.")
            
            self.SQLALCHEMY_DATABASE_URI = (
                f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )
        else:
            raise ValueError(f"Dialeto de base de dados não suportado: {self.DB_DIALECT}")
        return self

# Cria uma instância única das configurações para ser usada em toda a aplicação
settings = Settings()
