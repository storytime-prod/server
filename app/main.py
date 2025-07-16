# main.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.common.database import test_connection
from app.routes import branch, branch_req, comment, story
from fastapi.middleware.cors import CORSMiddleware

# For filling the database
from app.utils import generateTree, seed

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

test_connection()  # Test database connection on startup

api.include_router(story.router, prefix="/api/v1", tags=["story"])
api.include_router(branch.router, prefix="/api/v1", tags=["branch"])
api.include_router(comment.router, prefix="/api/v1", tags=["comment"])
api.include_router(branch_req.router, prefix="/api/v1", tags=["branch_request"])
api.include_router(generateTree.router, prefix="/api/v1", tags=["generate_tree"])


api.include_router(seed.router, prefix="/api/v1", tags=["seed"])


@api.get("/", tags=["redirect"], include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")
