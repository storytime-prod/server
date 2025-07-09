from sqlmodel import Field, SQLModel


class Comment(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    story_id: int = Field(default=None, foreign_key="story.id", index=True)
    content: str = Field(default=None, index=True)
    author: str | None = Field(default=None, index=True)
    created_at: str | None = Field(default=None, index=True)  # ISO format
