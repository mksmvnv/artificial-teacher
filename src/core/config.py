from pathlib import Path
from typing import Self

import yaml
from pydantic import BaseModel, SecretStr


class BotSettings(BaseModel):
    """Base bot settings."""

    token: SecretStr


class LoggerSettings(BaseModel):
    """Base logger settings."""

    level: str
    format: str
    path: Path


class DatabaseSettings(BaseModel):
    """PostgreSQL database settings."""

    user: str
    password: SecretStr
    host: str
    port: int
    name: str

    @property
    def url(self) -> str:
        """Get psql url."""
        return (
            f"postgresql+asyncpg://"
            f"{self.user}:{self.password.get_secret_value()}@"
            f"{self.host}:{self.port}/{self.name}"
        )


class ContextSettings(BaseModel):
    """Redis context settings."""

    user: str
    password: SecretStr
    host: str
    port: int
    ttl: int
    max_history_length: int  # Number of messages

    @property
    def url(self) -> str:
        """Get redis url."""
        return f"redis://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}"


class AssistantSettings(BaseModel):
    """AI assistant settings."""

    model: str
    token: SecretStr
    max_tokens: int
    temperature: float


class Settings(BaseModel):
    """Main settings."""

    bot: BotSettings
    logger: LoggerSettings
    database: DatabaseSettings
    context: ContextSettings
    assistant: AssistantSettings

    @classmethod
    def from_yaml(cls, path: Path) -> Self:
        """Load settings from yaml file."""
        with open(path) as f:
            return cls(**yaml.safe_load(f))


def get_settings() -> Settings:
    """Get settings from yaml file."""
    return Settings.from_yaml(Path(__file__).resolve().parents[2] / ".config" / "settings.yaml")


settings = get_settings()
