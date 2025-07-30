from typing import List
import uuid
from sqlmodel import Field, Relationship, SQLModel

from app.models.branch_req import BranchRequest
from app.models.story import Story


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    oauth_id: str = Field(index=True)
    username: str = Field()
    profile_picture: str | None = Field(default=None)
    email: str = Field()
    stories: List[Story] = Relationship(back_populates="author")
    branch_requests: List[BranchRequest] = Relationship(back_populates="created_by")
