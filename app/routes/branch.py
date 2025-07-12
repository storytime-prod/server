from typing import Annotated
from fastapi import APIRouter, Query
from sqlalchemy import func
from sqlmodel import select

from app.common.database import SessionDep
from app.models.branch import Branch
from app.models.story import Story


router = APIRouter()


@router.post("/branch/create", response_model=Branch, description="ONLY FOR DEV")
def create_branch(branch: Branch, session: SessionDep) -> Branch:
    session.add(branch)
    session.commit()
    session.refresh(branch)
    return branch


@router.get("/branch/", response_model=list[Branch])
def read_branches(session: SessionDep) -> list[Branch]:
    statement = select(Branch)
    branches = session.exec(statement).all()
    return branches


@router.get("/branch/{branch_id}", response_model=Branch)
def read_branch(branch_id: str, session: SessionDep) -> Branch:
    statement = select(Branch).where(Branch.id == branch_id)
    branch = session.exec(statement).first()
    if not branch:
        raise ValueError(f"Branch with ID {branch_id} not found")
    return branch


@router.get("/get-source-story/{dest_id}", response_model=Story)
def get_source_story(dest_id: str, session: SessionDep) -> Story:
    statement = select(Branch.src_id).where(Branch.dest_id == dest_id)
    story = session.exec(statement).first()
    if not story:
        raise ValueError(f"Source story for branch ID {dest_id} not found")
    return story
