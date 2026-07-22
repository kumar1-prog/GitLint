from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
import httpx
import os
from jose import jwt
from datetime import datetime, timedelta

router = APIRouter()

from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

# These come from your GitHub OAuth App settings
# You'll create this at github.com/settings/developers
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
JWT_SECRET = os.getenv("JWT_SECRET")
FRONTEND_URL = os.getenv("FRONTEND_URL")


@router.get("/login")
def github_login(request: Request, prompt: str = None):
    # Step 1: Send user TO GitHub's login page
    # scope=read:user,public_repo means we only ask for
    # profile info + public repos — nothing private
    # If scope is missing, GitHub defaults to no access at all
    github_auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&scope=read:user,public_repo"
    )
    
    if prompt == "consent":
        github_auth_url += "&prompt=consent"

    # RedirectResponse sends the user's browser to GitHub
    # Without this redirect, user stays on your app and sees nothing
    print("CLIENT ID IS:", GITHUB_CLIENT_ID)  # ADD THIS LINE
    print("REDIRECTING TO:", github_auth_url)  # ADD THIS LINE

    return RedirectResponse(github_auth_url, status_code=302)


@router.get("/callback")
async def github_callback(code: str):
    # Step 2: GitHub redirects back to THIS endpoint with a `code`
    # This code is a one-time-use temporary code (expires in 10 mins)
    # We now exchange it for a real access token

    # If `code` param is missing in the URL, FastAPI auto-returns 422 error
    # because we declared `code: str` in the function signature

    async with httpx.AsyncClient() as client:
        # Send the code + our secret to GitHub
        # GitHub verifies our identity using client_secret
        # If client_secret is wrong, GitHub returns an error
        token_response = await client.post(
            "https://github.com/login/oauth/access_token",
            json={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
            },
            headers={"Accept": "application/json"},
            # Accept: application/json tells GitHub to respond in JSON
            # Without this header, GitHub responds in plain text format
        )

    token_data = token_response.json()

    # token_data looks like:
    # {"access_token": "gho_xxxx", "token_type": "bearer", "scope": "read:user,public_repo"}
    # If the code was invalid/expired, GitHub returns {"error": "bad_verification_code"}

    access_token = token_data.get("access_token")
    if not access_token:
        # Instead of raw JSON, redirect back to frontend with error so user isn't stuck
        print("GITHUB OAUTH FAILED. URL was visited with invalid code?")
        error_msg = token_data.get("error", "oauth_failed")
        return RedirectResponse(f"{FRONTEND_URL}/callback?error={error_msg}", status_code=302)

    # Step 3: Use the token to fetch the user's GitHub profile
    async with httpx.AsyncClient() as client:
        user_response = await client.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {access_token}",
                # This header proves to GitHub we have a valid token
                # Without Authorization header, GitHub returns 401 Unauthorized
            },
        )

    github_user = user_response.json()
    # github_user contains: login, id, avatar_url, name, public_repos, followers, etc.

    # Step 4: Create OUR OWN JWT token for this user's session
    # We don't store GitHub's token in the browser (security risk)
    # Instead we create a short-lived JWT that identifies the user to our backend
    our_jwt = jwt.encode(
        {
            "github_username": github_user["login"],
            "github_token": access_token,  # stored inside JWT, not exposed to browser
            "exp": datetime.utcnow() + timedelta(hours=24),
            # exp = expiry. After 24 hours this token is invalid.
            # If exp is missing, token never expires — security risk
        },
        JWT_SECRET,
        algorithm="HS256",
        # HS256 = HMAC SHA-256. Signs the token with your JWT_SECRET
        # Anyone who tampers with the token payload will have an invalid signature
        # Your backend detects this and rejects the token
    )

    # Step 5: Send user back to frontend with the JWT in the URL
    # Frontend will grab this token and store it in memory (not localStorage)
    print("REDIRECTING TO FRONTEND:", f"{FRONTEND_URL}/callback?token={our_jwt[:20]}...")

    return RedirectResponse(
        url=f"{FRONTEND_URL}/callback?token={our_jwt}",
        status_code=302
    )