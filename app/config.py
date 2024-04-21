from pathlib import Path

from pydantic import Field, PostgresDsn, RedisDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent
PICS_DIR = BASE_DIR / "data"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR.parent / ".env.local", env_file_encoding="utf-8", extra="allow")

    BOT_TOKEN: SecretStr = Field(..., alias="BOT_TOKEN")
    PAGE_TIMEOUT: int = Field(default=10 * 1000, alias="BOT_PAGE_TIMEOUT")  # milliseconds for page load
    DROP_UPDATES_ON_START: bool = Field(default=False, alias="BOT_DROP_UPDATES_ON_START")
    DB_URI: PostgresDsn = Field(..., alias="DB_BOT_DSN")
    REDIS_URI: RedisDsn = Field(..., alias="REDIS_BOT_DSN")
    RABBITMQ_URI: str = 'amqp://guest:guest@localhost:5672/'
    DEBUG: bool = Field(default=False, alias="BOT_DEBUG")
    TELEGRAPH_TIMEOUT: int = Field(default=5, alias="BOT_TELEGRAPH_TIMEOUT")  # seconds for telegraph post image
    MAX_TASKS: int = 10
    WORKER_USED: bool = True


settings = Settings()
