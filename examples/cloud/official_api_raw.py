"""
B1. Official HTTP API (Raw)

Make raw HTTP calls to EZVIZ cloud API.
Demonstrates: login, pagelist device discovery, PTZ, switches.

Prerequisites:
    - EZVIZ account username and password
    - Region URL (default: apiieu.ezvizlife.com)

API Docs: https://open.ys7.com/help/en
EZVIZ Open Platform: https://open.ezvizlife.com
"""

import hashlib
import json
import requests
import uuid

# ================= CONFIGURATION =================
USERNAME = "YOUR_EZVIZ_USERNAME"
PASSWORD = "YOUR_EZVIZ_PASSWORD"
REGION = "apiieu.ezvizlife.com"      # or apiusa.ezvizlife.com, apichina.ezvizlife.com
# =================================================

BASE_URL = f"https://{REGION}"


def generate_feature_code() -> str:
    """Generate a deterministic feature code from MAC address."""
    mac_int = uuid.getnode()
    mac_str = ":".join(f"{(mac_int >> i) & 0xFF:02x}" for i in range(40, -1, -8))
    return hashlib.md5(mac_str.encode("utf-8")).hexdigest()


def login() -> dict:
    """Login to EZVIZ and return session info."""
    feature_code = generate_feature_code()
    password_md5 = hashlib.md5(PASSWORD.encode("utf-8"), usedforsecurity=False).hexdigest()

    headers = {
        "User-Agent": "okhttp/3.12.1",
        "featureCode": feature_code,
        "clientType": "3",
        "clientNo": "web_site",
        "appId": "ys7",
        "lang": "en",
    }

    payload = {
        "account": USERNAME,
        "password": password_md5,
        "featureCode": feature_code,
    }

    resp = requests.post(
        f"{BASE_URL}/v3/users/login/v5",
        headers=headers,
        data=payload,
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()

    if data.get("meta", {}).get("code") != 200:
        raise RuntimeError(f"Login failed: {data}")

    login_data = data.get("loginSession", {})
    session_id = login_data.get("sessionId")
    print(f"Logged in. Session ID: {session_id[:10]}...")
    return {
        "session_id": session_id,
        "rf_session_id": login_data.get("rfSessionId"),
        "feature_code": feature_code,
    }


def get_pagelist(session_id: str, feature_code: str) -> list:
    """Fetch device pagelist (discovery)."""
    headers = {
        "User-Agent": "okhttp/3.12.1",
        "featureCode": feature_code,
        "clientType": "3",
        "clientNo": "web_site",
        "appId": "ys7",
        "lang": "en",
        "sessionId": session_id,
    }

    resp = requests.post(
        f"{BASE_URL}/v3/userdevices/v1/resources/pagelist",
        headers=headers,
        data={"filter": "CHECK", "limit": 100},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()

    devices = data.get("data", []) if isinstance(data.get("data"), list) else []
    print(f"Found {len(devices)} device(s)\n")
    for d in devices:
        print(f"  Name     : {d.get('name')}")
        print(f"  Serial   : {d.get('deviceSerial')}")
        print(f"  Category : {d.get('category')}")
        print(f"  Status   : {d.get('status')}")
        print()
    return devices


def main():
    token_info = login()
    devices = get_pagelist(token_info["session_id"], token_info["feature_code"])

    if not devices:
        print("No devices found. Ensure camera is added to your EZVIZ account.")


if __name__ == "__main__":
    main()
