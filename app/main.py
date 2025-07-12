# main.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.common.database import test_connection
from app.routes import branch, branch_req, comment, story

api = FastAPI()

test_connection()  # Test database connection on startup

api.include_router(story.router, prefix="/api/v1", tags=["story"])
api.include_router(branch.router, prefix="/api/v1", tags=["branch"])
api.include_router(comment.router, prefix="/api/v1", tags=["comment"])
api.include_router(branch_req.router, prefix="/api/v1", tags=["branch_request"])


@api.get("/", tags=["redirect"], include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")
