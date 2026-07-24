import os
import requests

from dotenv import load_dotenv
from config import SCRIPT_DIRECTORY

load_dotenv(SCRIPT_DIRECTORY / ".env")

RIOT_API_KEY = os.getenv("RIOT_API_KEY")

if not RIOT_API_KEY:
    raise RuntimeError("RIOT_API_KEY not found.")

session = requests.Session()

session.headers.update(
    {
        "X-Riot-Token": RIOT_API_KEY,
        "Accept": "application/json",
    }
)


def riot_get(url, params=None):

    response = session.get(
        url,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()