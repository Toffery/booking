from datetime import timedelta
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    JWT_SECRET: str
    JWT_ALG: str
    JWT_EXP: int = 30 # minutes

    REFRESH_TOKEN_KEY: str
    REFRESH_TOKEN_EXP: timedelta = timedelta(days=30)

    
    model_config = SettingsConfigDict(env_file="src/auth/.env")

auth_settings = AuthSettings()
