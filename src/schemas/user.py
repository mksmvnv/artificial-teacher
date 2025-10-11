from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    """Base user schema."""

    tg_id: int
    username: str | None = Field(None, max_length=32)
    first_name: str | None = Field(None, max_length=64)
    last_name: str | None = Field(None, max_length=64)
