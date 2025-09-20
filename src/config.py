from pathlib import Path

import yaml
from pydantic import BaseModel


class BotSettings(BaseModel):
    token: str


class DatabaseSettings(BaseModel):
    dialect: str
    driver: str
    user: str
    password: str
    host: str
    port: int
    name: str

    @property
    def url(self) -> str:
        return f"{self.dialect}+{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class Settings(BaseModel):
    bot: BotSettings
    db: DatabaseSettings

    @classmethod
    def from_yaml(cls, path: Path) -> "Settings":
        with open(path) as f:
            return cls(**yaml.safe_load(f))


def get_settings() -> Settings:
    return Settings.from_yaml(Path(__file__).parent.parent / ".config" / "config.yaml")


settings = get_settings()
