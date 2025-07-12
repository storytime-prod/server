from xml.etree.ElementTree import Comment
from fastapi import APIRouter
from sqlmodel import select

from app.common.database import SessionDep


router = APIRouter()


@router.get("/comments/{story_id}", response_model=list[Comment])
def read_comments(story_id: str, session: SessionDep) -> list[Comment]:
    statement = select(Comment).where(Comment.story_id == story_id)
    comments = session.exec(statement).all()
    return comments


@router.post("/comments/{story_id}/add", response_model=Comment)
def create_comment(story_id: str, comment: Comment, session: SessionDep) -> Comment:
    comment.story_id = story_id
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment


@router.post("/comments/{branch_req_id}/add", response_model=Comment)
def create_branch_comment(
    branch_req_id: str, comment: Comment, session: SessionDep
) -> Comment:
    comment.branch_req_id = branch_req_id
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment
