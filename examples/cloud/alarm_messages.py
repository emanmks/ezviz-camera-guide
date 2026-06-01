"""
B7. Alarm & Event Messages

Query recent alarm events (motion, human, vehicle, sound) from the
EZVIZ unified message API.

Prerequisites:
    pip install pyezvizapi
"""

from pyezvizapi import EzvizClient

# ================= CONFIGURATION =================
USERNAME = "YOUR_EZVIZ_USERNAME"
PASSWORD = "YOUR_EZVIZ_PASSWORD"
REGION = "apiieu.ezvizlife.com"
SERIAL = "YOUR_CAMERA_SERIAL"          # Optional: filter by device
# =================================================


def main():
    client = EzvizClient(account=USERNAME, password=PASSWORD, url=REGION)
    client.login()

    print("Fetching alarm messages...")
    # The unified message API is accessible through the client
    # pyEzvizApi uses internal methods; here we show the raw concept
    # In practice, the camera object's _alarm_list() fetches recent alarms

    from pyezvizapi.camera import EzvizCamera
    cam = EzvizCamera(client, SERIAL)

    # This populates last alarm info
    cam._alarm_list()
    print(f"  Last alarm time : {cam.fetch_key(['last_alarm_time'])}")
    print(f"  Last alarm type : {cam.fetch_key(['last_alarm_type_name'])}")
    print(f"  Last alarm pic  : {cam.fetch_key(['last_alarm_pic'])}")
    print(f"  Motion trigger  : {cam.fetch_key(['Motion_Trigger'])}")

    client.close()


if __name__ == "__main__":
    main()
