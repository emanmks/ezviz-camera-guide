"""
B6. Cloud Snapshots

Request a snapshot image via the EZVIZ cloud API.
The camera wakes up if it is in sleep mode.

Prerequisites:
    pip install pyezvizapi
"""

import requests
from pyezvizapi import EzvizClient
from pyezvizapi.camera import EzvizCamera

# ================= CONFIGURATION =================
USERNAME = "YOUR_EZVIZ_USERNAME"
PASSWORD = "YOUR_EZVIZ_PASSWORD"
REGION = "apiieu.ezvizlife.com"
SERIAL = "YOUR_CAMERA_SERIAL"
OUTPUT_FILE = "ezviz_cloud_snapshot.jpg"
# =================================================


def main():
    client = EzvizClient(account=USERNAME, password=PASSWORD, url=REGION)
    client.login()

    cam = EzvizCamera(client, SERIAL)
    print(f"Requesting snapshot from {cam.get_name()}...")

    # The alarm API returns the latest alarm image URL
    alarms = cam._alarm_list()
    pic_url = cam.fetch_key(["last_alarm_pic"])

    if pic_url:
        print(f"Downloading from {pic_url[:60]}...")
        resp = requests.get(pic_url, timeout=30)
        resp.raise_for_status()
        with open(OUTPUT_FILE, "wb") as f:
            f.write(resp.content)
        print(f"Saved to {OUTPUT_FILE} ({len(resp.content)} bytes)")
    else:
        print("No alarm pic URL available")

    client.close()


if __name__ == "__main__":
    main()
