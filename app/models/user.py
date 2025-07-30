from datetime import datetime, timezone
import uuid
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    oauth_id: str = Field(index=True)
    username: str = Field()
    profile_picture: str | None = Field(default=None)
    email: str = Field()
