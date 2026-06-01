"""
B8. MQTT Event Notifications

Receive real-time device events via EZVIZ's MQTT broker.
This provides push-based alerts for motion, human detection, etc.

Prerequisites:
    pip install paho-mqtt pyezvizapi

Note: EZVIZ MQTT uses a specific broker and topic structure.
The pyezvizapi library includes MQTT client helpers.
"""

import json
import time
from pyezvizapi import EzvizClient
from pyezvizapi.mqtt import MQTTClient

# ================= CONFIGURATION =================
import os
USERNAME = os.environ.get("EZVIZ_USER", "YOUR_EZVIZ_USERNAME")
PASSWORD = os.environ.get("EZVIZ_PASS", "YOUR_EZVIZ_PASSWORD")
REGION = os.environ.get("EZVIZ_REGION", "apiieu.ezvizlife.com")
# =================================================


def on_message(client, userdata, msg):
    print(f"\nTopic: {msg.topic}")
    try:
        payload = json.loads(msg.payload.decode())
        print(json.dumps(payload, indent=2))
    except json.JSONDecodeError:
        print(f"Raw: {msg.payload.decode()}")


def main():
    # First login to get session info
    ezviz_client = EzvizClient(account=USERNAME, password=PASSWORD, url=REGION)
    ezviz_client.login()

    # MQTT client uses credentials from the EzvizClient
    mqtt = MQTTClient(
        ezviz_client,
        on_message_callback=on_message,
    )

    print("Connecting to EZVIZ MQTT broker...")
    mqtt.start()
    print("Connected. Listening for events (Ctrl+C to exit)...\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDisconnecting...")
        mqtt.stop()
        ezviz_client.close()


if __name__ == "__main__":
    main()
