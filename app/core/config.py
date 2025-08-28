# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator, Field
from typing import Any

class Settings(BaseSettings):
    # Carrega as variáveis de ambiente do arquivo .env
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Variáveis para a escolha do banco de dados
    DB_DIALECT: str = Field(..., description="Dialeto do banco: 'postgresql' ou 'mysql'")
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_PORT: int

    # Esta variável será CONSTRUÍDA a partir das variáveis acima
    SQLALCHEMY_DATABASE_URI: str | None = None

    @model_validator(mode='after')
    def build_database_uri(self) -> 'Settings':
        """
        Constrói a URI de conexão com o banco de dados dinamicamente
        com base no dialeto escolhido.
        """
        if self.DB_DIALECT == "postgresql":
            # Usa o driver psycopg2
            self.SQLALCHEMY_DATABASE_URI = (
                f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )
        elif self.DB_DIALECT == "mysql":
            # Usa o driver mysqlclient
            self.SQLALCHEMY_DATABASE_URI = (
                f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )
        else:
            raise ValueError(f"Dialeto de banco de dados não suportado: {self.DB_DIALECT}")
        return self

    # Configurações de Segurança e JWT (continuam as mesmas)
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

# Cria uma instância única das configurações para ser usada em toda a aplicação
settings = Settings()