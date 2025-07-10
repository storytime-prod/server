import uuid
from sqlmodel import Field, SQLModel


class Branch(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    src_id: uuid.UUID = Field(index=True, foreign_key="story.id")
    dest_id: uuid.UUID = Field(index=True, foreign_key="story.id")
    title: str = Field(index=True)
