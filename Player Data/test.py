import requests

RIOT_API_KEY = "RGAPI-e97aaf3d-fce9-4482-837c-1bb563df2c71".strip()

url = (
    "https://asia.api.riotgames.com"
    "/riot/account/v1/accounts/by-riot-id/"
    "Eunhaa/0994"
)

headers = {
    "X-Riot-Token": RIOT_API_KEY
}

response = requests.get(
    url,
    headers=headers,
    timeout=30
)

print("Key empty:", RIOT_API_KEY == "")
print("Key starts correctly:", RIOT_API_KEY.startswith("RGAPI-"))
print("Key length:", len(RIOT_API_KEY))
print("Header value length:", len(headers["X-Riot-Token"]))
print("Header sent:", "X-Riot-Token" in response.request.headers)
print("Sent header length:", len(response.request.headers.get("X-Riot-Token", "")))
print("Status:", response.status_code)
print("Response:", response.text)