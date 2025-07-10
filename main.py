# main.py
from typing import Annotated
from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse
from sqlmodel import select
from app.database import (
    SessionDep,
    create_db_and_tables,
    test_connection,
)
from app.models.story import Story  # Ensure database is initialized

api = FastAPI()

test_connection()  # Test database connection on startup


@api.get("/")
async def root():
    return RedirectResponse(url="/docs")


@api.post("/story/")
def create_story(story: Story, session: SessionDep) -> Story:
    s = Story(
        id=story.id,
        title=story.title,
        content=story.content,
        author=story.author,
        created_at=story.created_at,
        likes=story.likes,
        genre=story.genre,
        isRoot=story.isRoot,
        is_public=story.is_public,
    )
    session.add(s)
    session.commit()
    session.refresh(s)
    return s


@api.get("/story/")
def read_stories(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Story]:
    statement = select(Story).offset(offset).limit(limit)
    stories = session.exec(statement).all()
    return stories
