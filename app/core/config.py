from pydantic_settings import BaseSettings, SettingsConfigDict
import urllib.parse

class Settings(BaseSettings):
    PROJECT_NAME: str = "Task Management API"
    ENVIRONMENT: str = "development"
    
    # DATABASE
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "taskdb"
    POSTGRES_TEST_DB: str = "testdb"
    
    @property
    def DATABASE_URL(self) -> str:
        password = urllib.parse.quote_plus(self.POSTGRES_PASSWORD)
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{password}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property
    def TEST_DATABASE_URL(self) -> str:
        password = urllib.parse.quote_plus(self.POSTGRES_PASSWORD)
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{password}@localhost:{self.POSTGRES_PORT}/{self.POSTGRES_TEST_DB}"
    
    # JWT
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # ADMIN DEFAULTS
    ADMIN_EMAIL: str = "admin@gmail.com"
    ADMIN_PASSWORD: str = "Admin@123"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
