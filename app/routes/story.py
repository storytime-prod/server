from typing import Annotated
import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from sqlmodel import select

from app.common.database import SessionDep
from app.models.branch import Branch
from app.models.pydantic.story_with_author import StoryWithAuthor
from app.models.story import Story
from app.models.user import User
from app.utils.auth import get_current_user


router = APIRouter()


@router.post("/story/")
def create_story(
    story: Story, session: SessionDep, user=Depends(get_current_user)
) -> Story:
    statement = select(User).where(User.oauth_id == user["sub"])
    u = session.exec(statement).first()
    s = Story(
        id=story.id,
        title=story.title,
        content=story.content,
        author_id=story.id,
        author=u,
        created_at=story.created_at,
        likes=story.likes,
        genre=story.genre,
        is_root=story.is_root,
        is_public=story.is_public,
    )
    session.add(s)
    session.commit()
    session.refresh(s)
    return s


@router.get("/story/", response_model=list[StoryWithAuthor])
def read_stories(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[StoryWithAuthor]:
    statement = (
        select(Story)
        .options(joinedload(Story.author))
        .where(Story.is_public == True)
        .offset(offset)
        .limit(limit)
    )
    stories = session.exec(statement).all()
    return stories


@router.get("/story/id/{story_id}", response_model=StoryWithAuthor)
def read_story(story_id: str, session: SessionDep) -> StoryWithAuthor:
    statement = (
        select(Story).options(joinedload(Story.author)).where(Story.id == story_id)
    )
    story = session.exec(statement).first()
    if not story:
        raise ValueError(f"Story with ID {story_id} not found")
    return story


@router.get("/story/random", response_model=StoryWithAuthor)
def read_random_story(session: SessionDep) -> StoryWithAuthor:
    statement = (
        select(Story)
        .options(joinedload(Story.author))
        .where(Story.is_root == True, Story.is_public == True)
        .order_by(func.random())
        .limit(1)
    )
    story = session.exec(statement).first()
    if not story:
        raise ValueError("No stories found")
    return story


@router.get("/story/branches/{story_id}", response_model=list[Story])
def read_story_branches(story_id: str, session: SessionDep) -> list[Story]:
    src_uuid = uuid.UUID(story_id)

    statement = (
        select(Story)
        .join(Branch, Story.id == Branch.dest_id)
        .where(Branch.src_id == src_uuid)
    )
    results = session.exec(statement).all()
    return results


@router.put("/story/{story_id}/like", response_model=Story)
def update_story_likes(story_id: str, session: SessionDep) -> Story:
    statement = select(Story).where(Story.id == story_id)
    story = session.exec(statement).first()
    if not story:
        raise ValueError("Story not found")
    story.likes += 1
    session.add(story)
    session.commit()
    session.refresh(story)
    return story
