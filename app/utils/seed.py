from fastapi import APIRouter
from sqlalchemy import func, select

from app.common.database import SessionDep
from app.models.branch import Branch
from app.models.branch_req import BranchRequest
from app.models.story import Story


import json

mock_stories = []

with open(
    "mockStories.json",
    "r",
    encoding="utf-8",
) as f:
    mock_stories = json.load(f)

router = APIRouter()


branches = [(0, 1), (0, 2), (0, 3), (2, 4), (4, 5), (3, 6), (3, 7), (7, 9)]


@router.post("/seed/dbpopulate", description="ONLY FOR DEV")
def fill__story_db(session: SessionDep):
    for story in mock_stories:
        s = Story(
            title=story["title"],
            content=story["content"],
            author=story["author"],
            likes=story["likes"],
            genre=story["genre"],
            is_root=story["is_root"],
            is_public=True,
        )
        session.add(s)
    session.commit()
    session.refresh(s)
    return None


@router.post("/seed/branchpopulate", description="ONLY FOR DEV")
def fill__branch_db(session: SessionDep):
    statement = select(Story.id)
    story_ids = session.exec(statement).all()
    story_ids = [str(t[0]) for t in story_ids]
    for branch_idx in branches:
        b = Branch(
            src_id=story_ids[branch_idx[0]],
            dest_id=story_ids[branch_idx[1]],
            title=f"Sample Branch {branch_idx[0]}-{branch_idx[1]}",
        )
        session.add(b)
    session.commit()
    session.refresh(b)
    return None


@router.post("/seed/branchreqpopulate", description="ONLY FOR DEV")
def fill__branch_req_db(session: SessionDep):
    # make new branch requests for each branch

    s_id = "3812a3fb-c13a-4bc8-90ad-f5fd0e1b551c"
    s = Story(
        id=s_id,
        title=f"Sample Story {11}",
        content=f"This is the content of sample story {11}.",
        author="Author Name",
        likes=0,
        genre="Fiction",
        is_root=True,
        is_public=True,
    )

    d_id = "108d9fc2-ea3e-4bd2-9d0b-5210df062479"
    d = Story(
        id=d_id,
        title=f"Sample Story {12}",
        content=f"This is the content of sample story {12}.",
        author="Author Name",
        likes=0,
        genre="Fiction",
        is_root=True,
        is_public=False,
    )

    session.add(s)
    session.add(d)
    session.commit()

    print(s_id, d_id, "LOL")

    br = BranchRequest(
        src_id=s_id,
        dest_id=d_id,
        title=f"Sample Branch Request {s_id}-{d_id}",
    )
    session.add(br)
    session.commit()
    session.refresh(s)
    session.refresh(d)
    session.refresh(br)
    return None


@router.delete("/seed/deleteall", description="ONLY FOR DEV")
def delete_all_data(session: SessionDep):
    session.query(BranchRequest).delete()
    session.query(Branch).delete()
    session.query(Story).delete()
    session.commit()
    return None
