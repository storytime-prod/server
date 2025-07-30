from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel

from app.models.user import User


class StoryWithAuthor(BaseModel):
    id: uuid.UUID
    title: str
    content: str
    author_id: uuid.UUID
    genre: str
    is_root: bool
    is_public: bool
    created_at: datetime
    likes: Optional[int]
    author: User  # 👈 Nested author info

    class Config:
        from_attributes = True
