import uuid
from sqlmodel import Field, SQLModel


class Like(SQLModel, table=True):
    story_id: uuid.UUID = Field(
        default_factory=uuid.uuid4, foreign_key="story.id", primary_key=True, index=True
    )
    likes: int = Field(default=0, index=True)  # Number of likes for the story
