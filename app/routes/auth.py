import os
from fastapi import APIRouter, Depends, Request
from fastapi.responses import PlainTextResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth

from app.utils.auth import create_access_token, get_current_user

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
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    print("token:", token)
    try:
        resp = await oauth.google.get(
            "https://openidconnect.googleapis.com/v1/userinfo", token=token
        )
        user = resp.json()
        request.session["user"] = user
        token = create_access_token(
            {"sub": user["email"], "name": user["name"], "picture": user["picture"]}
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
    response = RedirectResponse(url="http://localhost:5173")
    response.delete_cookie("access_token")
    request.session.pop("user", None)

    return response


@router.get("/me")
async def get_user(user=Depends(get_current_user)):
    return {"user": user}
