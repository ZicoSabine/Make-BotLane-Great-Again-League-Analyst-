import json
import time
from urllib.parse import quote

from config import (
    REGIONAL_ROUTE,
    DATA_DIRECTORY,
)
from client import riot_get


# ============================================================
# 1. MATCH RETRIEVAL SETTINGS
# ============================================================

# Use a small number while testing.
# Set to None to retrieve every available match ID.
MAX_MATCHES = 20

# Riot Match-V5 allows up to 100 IDs per request.
MATCH_PAGE_SIZE = 100

REQUEST_DELAY_SECONDS = 1.25


# ============================================================
# 2. LOAD ACCOUNT DATA FROM STEP 1
# ============================================================

account_file = DATA_DIRECTORY / "account.json"

if not account_file.exists():
    raise FileNotFoundError(
        "account.json was not found.\n"
        "Run 01_get_player.py first."
    )

with open(
    account_file,
    "r",
    encoding="utf-8",
) as file:
    account_data = json.load(file)


# ============================================================
# 3. EXTRACT AND VALIDATE PUUID
# ============================================================

puuid = account_data.get("puuid", "").strip()

if not puuid:
    raise RuntimeError(
        "The PUUID is missing from account.json."
    )

riot_id = (
    f"{account_data.get('gameName')}#"
    f"{account_data.get('tagLine')}"
)

print("Player:", riot_id)
print("PUUID:", puuid)
print("Regional route:", REGIONAL_ROUTE.upper())


# ============================================================
# 4. BUILD MATCH-V5 REQUEST URL
# ============================================================

match_ids_url = (
    f"https://{REGIONAL_ROUTE}.api.riotgames.com"
    f"/lol/match/v5/matches/by-puuid/"
    f"{quote(puuid, safe='')}/ids"
)


# ============================================================
# 5. RETRIEVE MATCH IDS WITH PAGINATION
# ============================================================

all_match_ids = []
seen_match_ids = set()

start = 0

print("\nRetrieving match IDs...")

while True:
    if MAX_MATCHES is None:
        requested_count = MATCH_PAGE_SIZE
    else:
        remaining = MAX_MATCHES - len(all_match_ids)

        if remaining <= 0:
            break

        requested_count = min(
            MATCH_PAGE_SIZE,
            remaining,
        )

    match_id_batch = riot_get(
        match_ids_url,
        params={
            "start": start,
            "count": requested_count,
        },
    )

    if not match_id_batch:
        break

    new_match_ids = [
        match_id
        for match_id in match_id_batch
        if match_id not in seen_match_ids
    ]

    if not new_match_ids:
        break

    all_match_ids.extend(new_match_ids)
    seen_match_ids.update(new_match_ids)

    print(
        f"Retrieved {len(all_match_ids)} match IDs."
    )

    if len(match_id_batch) < requested_count:
        break

    start += len(match_id_batch)

    time.sleep(REQUEST_DELAY_SECONDS)


# ============================================================
# 6. DISPLAY RESULTS
# ============================================================

print("\n===== MATCH IDS RETRIEVED =====")
print("Total:", len(all_match_ids))

for match_id in all_match_ids:
    print(match_id)


# ============================================================
# 7. SAVE RESULTS
# ============================================================

match_ids_file = DATA_DIRECTORY / "match_ids.json"

with open(
    match_ids_file,
    "w",
    encoding="utf-8",
) as file:
    json.dump(
        all_match_ids,
        file,
        indent=4,
        ensure_ascii=False,
    )

print("\nSaved:")
print(match_ids_file)




https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/0icRHk3MAt5d1J53xyyVIW5XDijQd5yjOxfF5ti4lFWodig7u5Y50xfx8FKS8WWoffGDtiCM_OBsVw/ids?start=0&count=20