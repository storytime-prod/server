from sqlmodel import Field, SQLModel


class Story(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    author: str | None = Field(default=None, index=True)
    content: str
    genre: str | None = Field(default=None, index=True)
    isRoot: bool = Field(default=True, index=True)
    created_at: str | None = Field(default=None, index=True)  # ISO format
    is_public: bool | None = Field(
        default=True, index=True
    )  # Whether the story is public or private
    likes: int | None = Field(default=0, index=True)  # Number of likes for the story
    tags: list[str] = Field(default=[], index=True)  # Tags associated with the story
