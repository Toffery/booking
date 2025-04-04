import os
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


# MODE TEST is setting in conftest.py for testing
# Otherwise uses .env, which should be different for local and prod

if os.getenv("MODE") == "TEST":
    env_file = ".test.env"
elif os.getenv("MODE") == "DEV":
    env_file = ".docker.env"
else:
    env_file = ".env"
load_dotenv(env_file, override=True)


class Settings(BaseSettings):
    MODE: Literal["TEST", "LOCAL", "DEV", "PROD"]

    DB_NAME: str
    DB_HOST: str
    DB_USER: str
    DB_PASS: str
    DB_PORT: int

    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def is_production(self):
        return self.MODE == "PROD"

    model_config = SettingsConfigDict(
        env_file=env_file,
    )


settings = Settings()  # type: ignore
