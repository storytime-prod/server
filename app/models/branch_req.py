from datetime import datetime, timezone
import uuid
from sqlmodel import Field, SQLModel


class BranchRequest(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    src_id: uuid.UUID = Field(index=True, foreign_key="story.id")
    dest_id: uuid.UUID = Field(index=True, foreign_key="story.id")
    comment: str | None = Field(
        default="Hey! I'd like to branch your story.", index=True
    )
    status: str = Field(default="pending", index=True)  # pending, approved, rejected
    created_at: str | None = Field(
        default_factory=lambda: datetime.now(timezone.utc), index=True
    )  # ISO format
