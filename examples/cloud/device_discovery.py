"""
B5. Cloud Device Discovery

List all devices bound to your EZVIZ account via the cloud API.
Shows serial numbers, models, online status, local IPs, and capabilities.

Prerequisites:
    pip install pyezvizapi
"""

from pyezvizapi import EzvizClient

# ================= CONFIGURATION =================
import os
USERNAME = os.environ.get("EZVIZ_USER", "YOUR_EZVIZ_USERNAME")
PASSWORD = os.environ.get("EZVIZ_PASS", "YOUR_EZVIZ_PASSWORD")
REGION = os.environ.get("EZVIZ_REGION", "apiieu.ezvizlife.com")
# =================================================


def main():
    client = EzvizClient(account=USERNAME, password=PASSWORD, url=REGION)
    client.login()
    client.load_devices()

    cameras = client.get_cameras()
    print(f"Total cameras: {len(cameras)}\n")

    for serial, cam in cameras.items():
        print(f"  Serial      : {serial}")
        print(f"  Name        : {cam.get_name()}")
        print(f"  Category    : {cam.fetch_key(['device_category'])}")
        print(f"  SubCategory : {cam.fetch_key(['device_sub_category'])}")
        print(f"  Status      : {cam.status()}")
        print(f"  Local IP    : {cam.fetch_key(['WIFI', 'address'])}")
        print(f"  RTSP Port   : {cam.fetch_key(['local_rtsp_port'])}")
        print(f"  Battery     : {cam.battery_level()}")
        print(f"  Encrypted   : {cam.fetch_key(['encrypted'])}")
        print()

    client.close()


if __name__ == "__main__":
    main()
