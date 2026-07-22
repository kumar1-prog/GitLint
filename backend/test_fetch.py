import asyncio
import os
from github_client import fetch_all_data
from dotenv import load_dotenv

load_dotenv(override=True)
token = os.getenv("GITHUB_TOKEN")
print("Using Token:", token)

async def run():
    res = await fetch_all_data(token, "kumar1-prog")
    print("Repos fetched:", res.get("total_repos"))
    
asyncio.run(run())
