from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ai_bot_db_user: str
    ai_bot_db_password: str
    ai_bot_db_name: str
    ai_bot_db_host: str
    ai_bot_cloud_sql_connection_name: str
    environment: str = "development"

    # Security settings
    SECRET_KEY: str = "a_very_secret_key_that_should_be_changed"  # Replace with a real secret key
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()

# Generate a new secret key if the default is still set
# In a real application, this should be handled more robustly
import secrets
if settings.SECRET_KEY == "a_very_secret_key_that_should_be_changed":
    print("Warning: SECRET_KEY is not set. Using a default key. This is not secure for production.")
    # In a real scenario, you might raise an error or ensure it's set via environment variables
    # For this example, we'll update it directly if it's the placeholder.
    # However, directly modifying settings like this after import might not be ideal.
    # Consider using environment variables or a .env file for proper configuration.
    settings.SECRET_KEY = secrets.token_urlsafe(32)
