"""
B4. Bind Cloud Live Stream (VTM/VTDU)

Programmatically get EZVIZ cloud stream metadata (VTM server, VTDU tokens).
This is the low-level building block for cloud streaming.

Prerequisites:
    pip install pyezvizapi
"""

import json
from pyezvizapi import EzvizClient
from pyezvizapi.cloud_stream import get_cloud_stream_info, get_vtdu_token_v2

# ================= CONFIGURATION =================
USERNAME = "YOUR_EZVIZ_USERNAME"
PASSWORD = "YOUR_EZVIZ_PASSWORD"
REGION = "apiieu.ezvizlife.com"
SERIAL = "YOUR_CAMERA_SERIAL"
CHANNEL = 1
# =================================================


def main():
    client = EzvizClient(account=USERNAME, password=PASSWORD, url=REGION)
    client.login()

    print("Fetching VTDU token...")
    vtdu = get_vtdu_token_v2(client)
    print(f"VTDU Tokens: {vtdu.get('tokens', [])[:1]}...")

    print(f"\nFetching cloud stream info for {SERIAL} channel {CHANNEL}...")
    info = get_cloud_stream_info(client, SERIAL, channel=CHANNEL)
    print(json.dumps(info, indent=2, default=str))

    print("\n--- Key fields ---")
    print(f"Stream URL : {info.get('streamurl')}")
    print(f"Stream Key : {info.get('streamkey')}")
    print(f"VTM Server : {info.get('vtm_server')}")

    client.close()


if __name__ == "__main__":
    main()
