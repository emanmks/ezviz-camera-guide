"""
A1. Direct RTSP Stream

Capture or record RTSP stream using ffmpeg subprocess.
This is the simplest method for direct IP access on local network.

Prerequisites:
    - Camera IP address
    - Camera password / verification code
    - ffmpeg installed

RTSP URL Formats for EZVIZ/Hikvision:
    Standard: rtsp://admin:<PASSWORD>@<IP>/Streaming/Channels/101
              (101 = ch1 main stream, 102 = ch1 sub stream)
    Alternative: rtsp://admin:<PASSWORD>@<IP>/cam/realmonitor?channel=1&subtype=0
"""

import subprocess
import sys

# ================= CONFIGURATION =================
CAMERA_IP = "192.168.1.100"
PASSWORD = "YOUR_CAMERA_PASSWORD"
CHANNEL = 1
SUBTYPE = 0                          # 0=main/HD, 1=sub/SD
OUTPUT_FILE = "capture.mp4"
# =================================================

# Hikvision/EZVIZ standard RTSP URL
RTSP_URL = (
    f"rtsp://admin:{PASSWORD}@{CAMERA_IP}/Streaming/Channels/"
    f"{CHANNEL}{'01' if SUBTYPE == 0 else '02'}"
)

# Alternative format (some firmware versions)
RTSP_URL_ALT = (
    f"rtsp://admin:{PASSWORD}@{CAMERA_IP}/cam/realmonitor"
    f"?channel={CHANNEL}&subtype={SUBTYPE}"
)


def capture_stream(duration_sec: int = 30):
    cmd = [
        "ffmpeg",
        "-y",
        "-i", RTSP_URL,
        "-t", str(duration_sec),
        "-c", "copy",
        OUTPUT_FILE,
    ]
    print(f"Capturing {duration_sec}s from {RTSP_URL}")
    subprocess.run(cmd, check=True)
    print(f"Saved to {OUTPUT_FILE}")


def play_stream():
    cmd = ["ffplay", "-fflags", "nobuffer", "-flags", "low_delay", RTSP_URL]
    print(f"Playing {RTSP_URL}")
    subprocess.run(cmd)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["capture", "play"], default="play")
    parser.add_argument("--duration", type=int, default=30)
    args = parser.parse_args()

    if args.action == "capture":
        capture_stream(args.duration)
    else:
        play_stream()
