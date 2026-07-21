import requests

api_key = "RGAPI-768e19f0-bef8-4f41-a444-7480395a0299"

url = (
    "https://asia.api.riotgames.com"
    "/riot/account/v1/accounts/by-riot-id/"
    "Hide on bush/KR1"
)

response = requests.get(
    url,
    headers={"X-Riot-Token": api_key.strip()},
    timeout=20,
)

print("Status:", response.status_code)
print("Body:", response.text)
print("Header included:", "X-Riot-Token" in response.request.headers)
print("Key starts correctly:", api_key.strip().startswith("RGAPI-"))
print("Key length:", len(api_key.strip()))