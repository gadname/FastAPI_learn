from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ai_bot_db_user: str
    ai_bot_db_password: str
    ai_bot_db_name: str
    ai_bot_db_host: str
    ai_bot_cloud_sql_connection_name: str
    environment: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()
