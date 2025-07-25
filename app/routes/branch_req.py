from datetime import datetime
from time import timezone
from fastapi import APIRouter, HTTPException
from sqlmodel import not_, select

from app.common.database import SessionDep
from app.models.branch import Branch
from app.models.branch_req import BranchRequest
from app.models.story import Story


router = APIRouter()


@router.post("/branch-req/", response_model=BranchRequest)
def create_branch_req(branch_req: BranchRequest, session: SessionDep) -> BranchRequest:
    # Check if dest_id already exists as a src_id
    # exists_stmt = select(Branch).where(Branch.src_id == branch_req.dest_id)
    # existing = session.exec(exists_stmt).first()

    # if existing:
    #     raise HTTPException(
    #         status_code=400,
    #         detail=f"Invalid link: dest_id '{branch_req.dest_id}' already exists as a src_id. Cyclic branches not allowed.",
    #     )
    session.add(branch_req)
    session.commit()
    session.refresh(branch_req)
    return branch_req


@router.get("/branch-req/", response_model=list[BranchRequest])
def read_branch_reqs(session: SessionDep) -> list[BranchRequest]:
    statement = select(BranchRequest)
    branch_reqs = session.exec(statement).all()
    return branch_reqs


@router.get("/branch-req/{story_id}", response_model=list[BranchRequest])
def read_branch_req(story_id: str, session: SessionDep) -> list[BranchRequest]:
    statement = select(BranchRequest).where(BranchRequest.src_id == story_id)
    branch_req = session.exec(statement).all()
    if not branch_req:
        raise ValueError(f"Branch request for {story_id} not found")
    return branch_req


@router.put("/branch-req/{branch_req_id}/approve", response_model=BranchRequest)
def approve_branch_req(branch_req_id: str, session: SessionDep) -> BranchRequest:
    statement = select(BranchRequest).where(BranchRequest.id == branch_req_id)
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
