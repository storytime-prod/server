import uuid
from sqlmodel import Field, SQLModel


class Story(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(index=True)
    author: str | None = Field(default=None, index=True)
    content: str
    genre: str | None = Field(default=None, index=True)
    is_root: bool = Field(default=True, index=True)
    created_at: str | None = Field(default=None, index=True)  # ISO format
    is_public: bool | None = Field(
        default=True, index=True
    )  # Whether the story is public or private
    likes: int | None = Field(default=0, index=True)  # Number of likes for the story
