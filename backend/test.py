import asyncio, os
from dotenv import load_dotenv
from github_client import fetch_all_data
load_dotenv(override=True)
print(asyncio.run(fetch_all_data(os.getenv('GITHUB_TOKEN'), 'gkrishnakumar')))

