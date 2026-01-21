import json
import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv


def main():
    load_dotenv(override=True)

    api_url = os.getenv("API_URL")
    user = os.getenv("API_USER")
    pwd = os.getenv("API_USER_PWD")

    session = requests.Session()
    session.auth = HTTPBasicAuth(user, pwd)
    session.headers.update({"Accept": "application/json"})

    with open("example.json", "r", encoding="utf-8") as j:
        payload = json.load(j)

    resp = session.post(api_url, json=payload, timeout=30)
    print(resp.text)
    resp.raise_for_status()


if __name__ == "__main__":
    raise SystemExit(main())
