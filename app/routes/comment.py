from xml.etree.ElementTree import Comment
from fastapi import APIRouter, Depends
from sqlmodel import select

from app.common.database import SessionDep
from app.models.user import User
from app.utils.auth import get_current_user


router = APIRouter()


@router.get("/comments/{story_id}", response_model=list[Comment])
def read_comments(story_id: str, session: SessionDep) -> list[Comment]:
    statement = (  # TODO: Change this to use back_populates
        select(Comment, User)
        .join(User, Comment.created_by == User.id)
        .where(Comment.story_id == story_id)
    )
    comments = session.exec(statement).all()
    return comments


@router.post("/comments/{story_id}/add", response_model=Comment)
def create_comment(
    story_id: str, comment: Comment, session: SessionDep, user=Depends(get_current_user)
) -> Comment:
    comment.story_id = story_id
    comment.created_by = user.id
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment


@router.post("/comments/{branch_req_id}/add", response_model=Comment)
def create_branch_comment(
    branch_req_id: str,
    comment: Comment,
    session: SessionDep,
    user=Depends(get_current_user),
) -> Comment:
    comment.branch_req_id = branch_req_id
    comment.created_by = user.id
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment
