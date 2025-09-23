from pathlib import Path

import yaml
from pydantic import BaseModel


class BotSettings(BaseModel):
    """Bot settings."""

    token: str


class DatabaseSettings(BaseModel):
    """Database settings."""

    dialect: str
    driver: str
    user: str
    password: str
    host: str
    port: int
    name: str

    @property
    def url(self) -> str:
        """Database URL."""
        return f"{self.dialect}+{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class Settings(BaseModel):
    """Application settings."""

    bot: BotSettings
    db: DatabaseSettings

    @classmethod
    def from_yaml(cls, path: Path) -> "Settings":
        """Parse settings from YAML file."""
        with open(path) as f:
            return cls(**yaml.safe_load(f))


def get_settings() -> Settings:
    """Get application settings."""
    return Settings.from_yaml(Path(__file__).parent.parent / ".config" / "config.yaml")


settings = get_settings()
