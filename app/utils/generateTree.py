import os
from fastapi import APIRouter
from sqlmodel import func, select

from app.common.database import SessionDep
from app.models.branch import Branch
from app.models.story import Story


router = APIRouter()


@router.get("/generate-tree", tags=["generate_tree"])
def build_tree(session: SessionDep):
    stories = session.exec(select(Story)).all()
    branches = session.exec(select(Branch)).all()

    nodes = []
    spacing_x = 250
    spacing_y = 150
    for i, story in enumerate(stories):
        nodes.append(
            {
                "id": str(story.id),
                "label": story.title,
                "position": {"x": (i % 5) * spacing_x, "y": (i // 5) * spacing_y},
                "data": {"title": story.title},
            }
        )

    edges = []
    for branch in branches:
        edges.append(
            {
                "id": f"{branch.src_id}-{branch.dest_id}",
                "source": str(branch.src_id),
                "target": str(branch.dest_id),
            }
        )

    return {"nodes": nodes, "edges": edges}
