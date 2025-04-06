from datetime import timedelta
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    JWT_SECRET: str
    JWT_ALG: str
    JWT_EXP: int = 30  # minutes

    REFRESH_TOKEN_EXP_DAYS: int = 30 # days

    model_config = SettingsConfigDict(env_file="src/auth/.env")


auth_settings = AuthSettings()  # type: ignore
