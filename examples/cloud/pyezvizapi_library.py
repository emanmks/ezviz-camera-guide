"""
B2. Using `pyezvizapi` Library

Official Python library for EZVIZ cameras, used by Home Assistant.
Provides high-level device control and streaming.

Prerequisites:
    pip install pyezvizapi

GitHub: https://github.com/RenierM26/pyEzvizApi
"""

from pyezvizapi import EzvizClient
from pyezvizapi.camera import EzvizCamera

# ================= CONFIGURATION =================
import os
USERNAME = os.environ.get("EZVIZ_USER", "YOUR_EZVIZ_USERNAME")
PASSWORD = os.environ.get("EZVIZ_PASS", "YOUR_EZVIZ_PASSWORD")
REGION = os.environ.get("EZVIZ_REGION", "apiieu.ezvizlife.com")
# =================================================


def main():
    client = EzvizClient(
        account=USERNAME,
        password=PASSWORD,
        url=REGION,
    )

    print("Logging in...")
    client.login()
    print("Authenticated\n")

    print("Fetching devices...")
    client.load_devices()
    cameras = client.get_cameras()

    print(f"Found {len(cameras)} camera(s)\n")
    for serial, cam in cameras.items():
        print(f"  Serial    : {serial}")
        print(f"  Name      : {cam.get_name()}")
        print(f"  Status    : {cam.status()}")
        print(f"  Local IP  : {cam.fetch_key(['WIFI', 'address'])}")
        print(f"  RTSP Port : {cam.fetch_key(['local_rtsp_port'])}")
        print()

    # Example: control first camera
    if cameras:
        first_serial = list(cameras.keys())[0]
        cam = EzvizCamera(client, first_serial)
        print(f"--- Controlling {cam.get_name()} ---")
        print(f"Privacy mode: {cam.privacy_mode()}")
        print(f"Sleep mode  : {cam.sleep_mode()}")
        print(f"Battery     : {cam.battery_level()}")

    client.close()


if __name__ == "__main__":
    main()
