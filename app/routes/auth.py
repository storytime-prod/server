import os
from fastapi import APIRouter, Depends, Request
from fastapi.responses import PlainTextResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth

from sqlmodel import select

from app.models.user import User
from app.utils.auth import create_access_token, get_current_user
from app.common.database import SessionDep

router = APIRouter()
oauth = OAuth()

oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")  # callback endpoint
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth")
async def auth(request: Request, session: SessionDep):
    token = await oauth.google.authorize_access_token(request)
    print("token:", token)
    try:
        resp = await oauth.google.get(
            "https://openidconnect.googleapis.com/v1/userinfo", token=token
        )
        user = resp.json()
        request.session["user"] = user
        existing_user = session.exec(
            select(User).where(User.oauth_id == user["sub"])
        ).first()
        user_id = existing_user.id if existing_user else None
        if not existing_user:
            new_user = User(
                oauth_id=user["sub"],
                username=user["name"],
                profile_picture=user.get("picture"),
                email=user["email"],
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            user_id = new_user.id
        token = create_access_token(
            {
                "id": str(user_id),
                "sub": user["email"],
                "name": user["name"],
                "picture": user["picture"],
            }
        )
    except Exception as e:
        return PlainTextResponse(f"OAuth error: {str(e)}", status_code=400)

    response = RedirectResponse(url="http://localhost:5173")
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # Set True in production with HTTPS
        samesite="lax",
    )
    return response


@router.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="http://localhost:5173", status_code=302)
    response.delete_cookie("access_token")
    request.session.pop("user", None)

    return response


@router.get("/me")
async def get_user(user=Depends(get_current_user)):
    return {"user": user}
