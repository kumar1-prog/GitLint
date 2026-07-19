import httpx
import os
# Add this import at the top of main.py




# Base URL for all GitHub API calls
# Every single GitHub API endpoint starts with this
GITHUB_API = "https://api.github.com"

# This is a helper function that builds the headers for every request
# Authorization header is how GitHub knows WHO is making the request
# If this header is missing → GitHub treats you as unauthenticated
# Unauthenticated = only 60 API calls per hour (authenticated = 5000)
def get_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        # This Accept header tells GitHub: give me the latest stable API response format
        # Without it, GitHub still works but may return older response shapes
    }


async def fetch_user_profile(token: str) -> dict:
    # Fetches basic profile: username, name, avatar, public_repos count, followers
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/user",
            headers=get_headers(token)
        )
    
    # .json() parses the response body from raw text into a Python dict
    # If GitHub returned an error, this dict will have an "message" key instead
    return response.json()


async def fetch_repos(token: str, username: str) -> list:
    # Fetches all public repos for this user
    # per_page=100 means get 100 repos in one call (max GitHub allows)
    # Without per_page, GitHub defaults to 30 — you'd miss repos
    # sort=updated means most recently active repos come first
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/users/{username}/repos"
            f"?per_page=100&sort=updated&type=owner",
            # type=owner means ONLY repos they created
            # Without this, it includes repos they're just a member of
            # which would inflate their numbers unfairly
            headers=get_headers(token)
        )
    
    repos = response.json()

    # repos is a list of dicts, each dict is one repo
    # Each repo has: name, fork, stargazers_count, size,
    # language, description, updated_at, open_issues_count etc.

    # If token is invalid, GitHub returns a dict with "message": "Bad credentials"
    # instead of a list — so we guard against that
    if not isinstance(repos, list):
        return []
    
    return repos


async def fetch_readme(token: str, username: str, repo_name: str) -> str:
    # Fetches the README content of a specific repo
    # GitHub returns README as base64 encoded content
    import base64

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/repos/{username}/{repo_name}/readme",
            headers=get_headers(token)
        )
    
    data = response.json()

    # If repo has no README, GitHub returns 404 with "message": "Not Found"
    # We return empty string so scoring engine can handle it gracefully
    if "content" not in data:
        return ""
    
    # GitHub sends README content as base64 encoded string
    # We decode it back to normal readable text
    # If we skip this decode, we get garbage characters like "SGVsbG8gV29ybGQ="
    decoded = base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
    return decoded


async def fetch_commit_activity(token: str, username: str, repo_name: str) -> list:
    # Fetches weekly commit count for the last 52 weeks for one repo
    # Returns a list of 52 numbers — one per week
    # Example: [0, 0, 3, 1, 0, 5, ...] means week1=0 commits, week3=3 commits etc.
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/repos/{username}/{repo_name}/stats/participation",
            headers=get_headers(token)
        )
    
    data = response.json()

    # participation returns {"all": [...52 weeks...], "owner": [...52 weeks...]}
    # "owner" = only commits by the repo owner (not collaborators)
    # We want "owner" so we don't count other people's contributions
    # If the repo is brand new or GitHub hasn't computed stats yet → empty dict
    return data.get("owner", [])


async def fetch_all_data(token: str, username: str) -> dict:
    # This is the MAIN function that orchestrates everything
    # It calls all the above functions and bundles results into one dict
    # The scoring engine will receive this single dict and work from it

    # Step 1: get all repos
    repos = await fetch_repos(token, username)

    # Step 2: separate original repos from forks
    # fork=True means they just copied someone else's repo
    # We care about original work for scoring
    original_repos = [r for r in repos if not r["fork"]]
    forked_repos = [r for r in repos if r["fork"]]

    # Step 3: for each original repo, fetch its README and commit activity
    # We limit to top 10 repos to avoid hitting GitHub rate limits
    # Checking 100 repos × 2 API calls each = 200 calls, too many
    top_repos = original_repos[:10]

    repo_details = []
    for repo in top_repos:
        readme = await fetch_readme(token, username, repo["name"])
        commits = await fetch_commit_activity(token, username, repo["name"])
        
        repo_details.append({
            "name": repo["name"],
            "stars": repo["stargazers_count"],
            # stargazers = people who starred this repo
            "language": repo["language"],
            # primary language GitHub detected — can be None if repo is empty
            "description": repo["description"] or "",
            "open_issues": repo["open_issues_count"],
            "size": repo["size"],
            # size is in kilobytes — 0 means empty repo
            "readme": readme,
            "weekly_commits": commits,
            # list of 52 numbers (one per week)
        })

       

    return {
        "username": username,
        "total_repos": len(repos),
        "original_repos": len(original_repos),
        "forked_repos": len(forked_repos),
        "repo_details": repo_details,
        # This is what the scoring engine will consume
    }
    # Add this new route below the existing root route
