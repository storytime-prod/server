from sqlmodel import Field, SQLModel


class Branch(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    src_id: int = Field(index=True, foreign_key="story.id")
    dest_id: int = Field(index=True, foreign_key="story.id")
    title: str = Field(index=True)
