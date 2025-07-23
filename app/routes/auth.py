import os
from dotenv import load_dotenv
from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth


load_dotenv()
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
    except Exception as e:
        return PlainTextResponse(f"OAuth error: {str(e)}", status_code=400)
    return RedirectResponse(url="/google/oauth/login")


@router.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/google/oauth/login")
