from datetime import datetime, timezone
from typing import Optional
import uuid
from sqlmodel import Field, Relationship, SQLModel


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
    created_by_id: uuid.UUID = Field(foreign_key="user.id")
    created_by: Optional["User"] = Relationship(back_populates="branch_requests")
