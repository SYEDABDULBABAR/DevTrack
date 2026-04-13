from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # --- Database Settings ---
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/devtrack"

    # --- JWT / Auth Settings ---
    # Secret key generate karne ke liye terminal mein likhein: openssl rand -hex 32
    SECRET_KEY: str = "your_super_secret_random_hex_key_here" 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Token 30 mins baad expire ho jayega

    # .env file ko read karne ke liye configuration
    model_config = SettingsConfigDict(env_file=".env")

# Is variable ko poore project mein use karenge
settings = Settings()