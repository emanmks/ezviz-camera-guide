"""
A8. Local SDK Stream (HCNetSDK)

Use the EZVIZ/Hikvision native LAN SDK protocol for direct streaming.
This bypasses RTSP and uses the same protocol the mobile app uses in LAN mode.
The pyezvizapi library handles CAS key exchange and SDK socket setup.

Prerequisites:
    pip install pyezvizapi
    ffmpeg installed (for MPEG-TS remuxing)

Note: This is an advanced method. It fetches CAS credentials from the cloud
and then opens a local TCP socket to the camera on ports 8000/9010/9020.
"""

import subprocess
import sys

# ================= CONFIGURATION =================
EZVIZ_USERNAME = "YOUR_EZVIZ_USERNAME"
EZVIZ_PASSWORD = "YOUR_EZVIZ_PASSWORD"
SERIAL = "YOUR_CAMERA_SERIAL"        # e.g., D12345678
REGION = "apiieu.ezvizlife.com"      # Change if needed
CHANNEL = 1
# =================================================


def dump_local_sdk_stream(duration: str = "30s", output: str = "local_sdk_stream.ts"):
    """
    Use pyezvizapi CLI to dump local SDK stream to MPEG-TS.
    This fetches CAS keys from cloud, then connects locally.
    """
    cmd = [
        "pyezvizapi",
        "-u", EZVIZ_USERNAME,
        "-p", EZVIZ_PASSWORD,
        "-r", REGION,
        "stream", "dump",
        "--serial", SERIAL,
        "--channel", str(CHANNEL),
        "--duration", duration,
        "--output", output,
    ]
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    print(f"Saved to {output}")


def proxy_local_sdk_stream(port: int = 8558):
    """
    Start a local HTTP proxy that serves the EZVIZ SDK stream as MPEG-TS.
    Any player (VLC, Home Assistant) can connect to http://localhost:8558/SERIAL.ts
    """
    cmd = [
        "pyezvizapi",
        "-u", EZVIZ_USERNAME,
        "-p", EZVIZ_PASSWORD,
        "-r", REGION,
        "stream", "proxy",
        "--serial", SERIAL,
        "--channel", str(CHANNEL),
        "--listen-port", str(port),
    ]
    print(f"Proxy starting at http://localhost:{port}/{SERIAL}.ts")
    print(f"Running: {' '.join(cmd)}")
    print("Press Ctrl+C to stop")
    subprocess.run(cmd)


def get_local_sdk_keys():
    """
    Print the local SDK credentials (endpoint, operation code, CAS key, media key).
    Useful for building your own SDK client.
    """
    cmd = [
        "pyezvizapi",
        "-u", EZVIZ_USERNAME,
        "-p", EZVIZ_PASSWORD,
        "-r", REGION,
        "stream", "local-sdk-keys",
        "--serial", SERIAL,
    ]
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action",
        choices=["dump", "proxy", "keys"],
        default="dump",
    )
    parser.add_argument("--duration", default="30s")
    parser.add_argument("--port", type=int, default=8558)
    args = parser.parse_args()

    if args.action == "dump":
        dump_local_sdk_stream(duration=args.duration)
    elif args.action == "proxy":
        proxy_local_sdk_stream(port=args.port)
    else:
        get_local_sdk_keys()
