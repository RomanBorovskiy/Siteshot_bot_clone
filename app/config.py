from pathlib import Path

from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
EMPTY_PIC = DATA_DIR / "empty.jpg"

PICS_DIR = BASE_DIR / "pics"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    BOT_TOKEN: SecretStr
    PAGE_TIMEOUT: int = Field(default=10 * 1000, env="BOT_PAGE_TIMEOUT")  # milliseconds for page load
    DROP_UPDATES_ON_START: bool Field(default=False, env="BOT_DROP_UPDATES_ON_START")
    DB_URI = Field(..., env="DB_BOT_DSN")
    REDIS_URI = Field(..., env="REDIS_BOT_DSN")


settings = Settings()
