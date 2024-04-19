from pathlib import Path

from pydantic import Field, PostgresDsn, RedisDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
EMPTY_PIC = DATA_DIR / "empty.jpg"

PICS_DIR = BASE_DIR / "pics"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR.parent / ".env.local", env_file_encoding="utf-8", extra="allow")

    BOT_TOKEN: SecretStr = Field(..., alias="BOT_TOKEN")
    PAGE_TIMEOUT: int = Field(default=10 * 1000, alias="BOT_PAGE_TIMEOUT")  # milliseconds for page load
    DROP_UPDATES_ON_START: bool = Field(default=False, alias="BOT_DROP_UPDATES_ON_START")
    DB_URI: PostgresDsn = Field(..., alias="DB_BOT_DSN")
    REDIS_URI: RedisDsn = Field(..., alias="REDIS_BOT_DSN")
    DEBUG: bool = Field(default=False, alias="BOT_DEBUG")


settings = Settings()
