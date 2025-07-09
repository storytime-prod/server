from sqlmodel import Field, SQLModel


class BranchRequest(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    src_id: int = Field(index=True, foreign_key="story.id")
    dest_id: int = Field(index=True, foreign_key="story.id")
    comment: str | None = Field(default=None, index=True)
    status: str = Field(default="pending", index=True)  # pending, approved, rejected
    created_at: str | None = Field(default=None, index=True)  # ISO format
