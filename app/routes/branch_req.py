from datetime import datetime
from time import timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import not_, select

from app.common.database import SessionDep
from app.models.branch import Branch
from app.models.branch_req import BranchRequest
from app.models.pydantic.branch_request_with_author import BranchRequestWithAuthor
from app.models.story import Story
from sqlalchemy.orm import joinedload
from app.models.user import User
from app.utils.auth import get_current_user


router = APIRouter()


@router.post("/branch-req/", response_model=BranchRequestWithAuthor)
def create_branch_req(
    branch_req: BranchRequest, session: SessionDep, user=Depends(get_current_user)
) -> BranchRequestWithAuthor:
    # Check if dest_id already exists as a src_id
    # exists_stmt = select(Branch).where(Branch.src_id == branch_req.dest_id)
    # existing = session.exec(exists_stmt).first()

    # if existing:
    #     raise HTTPException(
    #         status_code=400,
    #         detail=f"Invalid link: dest_id '{branch_req.dest_id}' already exists as a src_id. Cyclic branches not allowed.",
    #     )
    statement = select(User).where(User.oauth_id == user["sub"])
    u = session.exec(statement).first()
    branch_req.created_by = u
    session.add(branch_req)
    session.commit()
    session.refresh(branch_req)
    return branch_req


@router.get("/branch-req/", response_model=list[BranchRequestWithAuthor])
def read_branch_reqs(session: SessionDep) -> list[BranchRequestWithAuthor]:
    statement = select(BranchRequest).options(joinedload(BranchRequest.created_by))
    branch_reqs = session.exec(statement).all()
    return branch_reqs


@router.get("/branch-req/{story_id}", response_model=list[BranchRequestWithAuthor])
def read_branch_req(
    story_id: str, session: SessionDep
) -> list[BranchRequestWithAuthor]:
    statement = (
        select(BranchRequest)
        .options(joinedload(BranchRequest.created_by))
        .where(BranchRequest.src_id == story_id)
    )
    branch_req = session.exec(statement).all()
    if not branch_req:
        raise ValueError(f"Branch request for {story_id} not found")
    return branch_req


@router.put(
    "/branch-req/{branch_req_id}/approve", response_model=BranchRequestWithAuthor
)
def approve_branch_req(
    branch_req_id: str, session: SessionDep, user=Depends(get_current_user)
) -> BranchRequestWithAuthor:
    statement = (
        select(BranchRequest)
        .options(joinedload(BranchRequest.created_by))
        .where(BranchRequest.id == branch_req_id)
    )
    branch_req = session.exec(statement).first()
    if not branch_req:
        raise ValueError(f"Branch request with ID {branch_req_id} not found")
    elif branch_req.status != "pending":
        raise ValueError(f"Branch request with ID {branch_req_id} is not pending")

    # Approve the branch request
    branch_req.status = "approved"
    new_branch = Branch(
        src_id=branch_req.src_id,
        dest_id=branch_req.dest_id,
        title=branch_req.comment or "Untitled Branch",
    )

    statement = select(User).where(User.id == user["id"])
    logged_in_user = session.exec(statement).first()
    statement = select(Story.id).where(Story.author_id == logged_in_user.id)
    users_stories = {str(sid) for sid in session.exec(statement).all()}

    print("_______", branch_req.src_id, users_stories)

    if str(branch_req.src_id) not in users_stories:
        raise ValueError(
            f"Branch request source story {branch_req.src_id} does not belong to you! {logged_in_user.username, logged_in_user.id}"
        )

    session.add(new_branch)
    session.add(branch_req)
    session.commit()
    session.refresh(branch_req)
    return branch_req


@router.get("/branch-req/{story_id}/branchables", response_model=list[Story])
def get_branchable_stories(story_id: str, session: SessionDep) -> list[Story]:
    subquery = select(Branch.dest_id).where(Branch.dest_id != None)
    statement = (
        select(Story).where(Story.id != story_id).where(not_(Story.id.in_(subquery)))
    )
    results = session.exec(statement).all()
    return results


@router.delete("/branch-req/{branch_req_id}", response_model=BranchRequest)
def delete_branch_req(branch_req_id: str, session: SessionDep) -> BranchRequest:
    statement = select(BranchRequest).where(BranchRequest.id == branch_req_id)
    branch_req = session.exec(statement).first()
    if not branch_req:
        raise ValueError(f"Branch request with ID {branch_req_id} not found")
    session.delete(branch_req)
    session.commit()
    return branch_req
