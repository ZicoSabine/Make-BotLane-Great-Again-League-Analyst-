import json
from urllib.parse import quote

from config import (
    GAME_NAME,
    TAG_LINE,
    REGIONAL_ROUTE,
    DATA_DIRECTORY,
)
from client import riot_get


# ============================================================
# 1. BUILD ACCOUNT-V1 URL
# ============================================================

encoded_game_name = quote(GAME_NAME, safe="")
encoded_tag_line = quote(TAG_LINE, safe="")

account_url = (
    f"https://{REGIONAL_ROUTE}.api.riotgames.com"
    f"/riot/account/v1/accounts/by-riot-id/"
    f"{encoded_game_name}/{encoded_tag_line}"
)


# ============================================================
# 2. RETRIEVE PLAYER ACCOUNT
# ============================================================

print("Searching for Riot account...")
print(f"Riot ID: {GAME_NAME}#{TAG_LINE}")
print(f"Regional route: {REGIONAL_ROUTE.upper()}")

account_data = riot_get(account_url)


# ============================================================
# 3. EXTRACT PUUID
# ============================================================

puuid = account_data.get("puuid", "").strip()

if not puuid:
    raise RuntimeError(
        "Riot returned the account, but no PUUID was included."
    )

riot_id = (
    f"{account_data.get('gameName')}#"
    f"{account_data.get('tagLine')}"
)


# ============================================================
# 4. DISPLAY RESULT
# ============================================================

print("\n===== PLAYER FOUND =====")
print("Riot ID           :", riot_id)
print("Game Name         :", account_data.get("gameName"))
print("Tag Line          :", account_data.get("tagLine"))
print("PUUID              :", puuid)
print("Encrypted PUUID    :", puuid)

print(
    "\nThe PUUID and encrypted PUUID are the same value "
    "for Match-V5 requests."
)


# ============================================================
# 5. SAVE ACCOUNT DATA
# ============================================================

player_data = {
    "game_name": account_data.get("gameName"),
    "tag_line": account_data.get("tagLine"),
    "riot_id": riot_id,
    "puuid": puuid,
    "encrypted_puuid": puuid,
    "regional_route": REGIONAL_ROUTE,
}

account_file = DATA_DIRECTORY / "account.json"

with open(
    account_file,
    "w",
    encoding="utf-8",
) as file:
    json.dump(
        player_data,
        file,
        indent=4,
        ensure_ascii=False,
    )

print("\nSaved:")
print(account_file)