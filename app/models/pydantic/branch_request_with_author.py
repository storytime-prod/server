from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel

from app.models.user import User


class BranchRequestWithAuthor(BaseModel):
    id: uuid.UUID
    src_id: uuid.UUID
    dest_id: uuid.UUID
    comment: str | None
    status: str
    created_at: str | None
    created_by: User

    class Config:
        from_attributes = True
