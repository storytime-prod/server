# main.py
from typing import Annotated
from fastapi import FastAPI, Query
from sqlmodel import select
from app.database import (
    SessionDep,
    create_db_and_tables,
    test_connection,
)
from app.models.story import Story  # Ensure database is initialized

api = FastAPI()

test_connection()  # Test database connection on startup


# @api.on_event("startup")
# def on_startup():
#     create_db_and_tables()


@api.get("/")
async def root():
    return {"message": "Hello, World!"}


@api.post("/story/")
def create_story(story: Story, session: SessionDep) -> Story:
    session.add(story)
    session.commit()
    session.refresh(story)
    return story


@api.get("/stories/")
def read_stories(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Story]:
    stories = session.exec(select(Story).offset(offset).limit(limit)).all()
    return stories
