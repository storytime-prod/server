from sqlmodel import Field, SQLModel


class Like(SQLModel, table=True):
    story_id: int = Field(
        default=None, foreign_key="story.id", primary_key=True, index=True
    )
    likes: int = Field(default=0, index=True)  # Number of likes for the story
