from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # --- Database Settings ---
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/devtrack"

    # --- JWT / Auth Settings ---
    # To generate a secure secret key, run this command in your terminal: openssl rand -hex 32
    SECRET_KEY: str = "your_super_secret_random_hex_key_here" 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Token will expire after 30 minutes

    # Configuration to load values from a .env file
    model_config = SettingsConfigDict(env_file=".env")

# This instance will be used throughout the project to access settings
settings = Settings()