import datetime
import uuid
from sqlmodel import Field, SQLModel


class Comment(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    story_id: uuid.UUID = Field(default=None, foreign_key="story.id", index=True)
    content: str = Field(default=None, index=True)
    author: str | None = Field(default=None, index=True)
    created_at: str | None = Field(
        default_factory=lambda: datetime.now(datetime.timezone.utc), index=True
    )  # ISO format
