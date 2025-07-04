from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ai_bot_db_user: str
    ai_bot_db_password: str
    ai_bot_db_name: str
    ai_bot_db_host: str
    ai_bot_cloud_sql_connection_name: str
    environment: str = "development"

    SECRET_KEY: str = "a_very_secret_key_that_should_be_in_env"  # IMPORTANT: Load from .env in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
