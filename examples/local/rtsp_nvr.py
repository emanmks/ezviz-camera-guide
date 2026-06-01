"""
A3. RTSP via NVR (Multi-Channel)

Access multiple cameras through a single EZVIZ/Hikvision NVR IP address.
Each camera is assigned a channel number on the NVR.

Prerequisites:
    - NVR IP address
    - NVR admin password
    - Channel numbers for each camera (usually 1-8 or 1-16)

RTSP URL Format:
    rtsp://admin:<PASSWORD>@<NVR_IP>/Streaming/Channels/<CH>01
    (CH01 = channel 1 main stream, CH02 = channel 1 sub stream)
"""

import cv2
import sys

# ================= CONFIGURATION =================
NVR_IP = "192.168.1.50"
NVR_PASSWORD = "YOUR_NVR_PASSWORD"
CHANNELS = [1, 2, 3]
SUBTYPE = 0                         # 0=main/HD, 1=sub/SD
# =================================================


def get_rtsp_url(channel: int) -> str:
    suffix = "01" if SUBTYPE == 0 else "02"
    return f"rtsp://admin:{NVR_PASSWORD}@{NVR_IP}/Streaming/Channels/{channel}{suffix}"


def display_all_channels():
    caps = {}
    for ch in CHANNELS:
        url = get_rtsp_url(ch)
        cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        if cap.isOpened():
            caps[ch] = cap
            print(f"Channel {ch}: Connected")
        else:
            print(f"Channel {ch}: FAILED")

    if not caps:
        print("No channels available")
        sys.exit(1)

    print("Press 'q' to quit")

    while True:
        for ch, cap in list(caps.items()):
            ret, frame = cap.read()
            if ret:
                cv2.putText(
                    frame,
                    f"NVR Ch {ch}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                )
                cv2.imshow(f"Channel {ch}", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    for cap in caps.values():
        cap.release()
    cv2.destroyAllWindows()


def capture_channel_snapshot(channel: int, output: str = None):
    url = get_rtsp_url(channel)
    cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    if not cap.isOpened():
        print(f"Cannot open channel {channel}")
        return

    ret, frame = cap.read()
    if ret:
        out = output or f"nvr_ch{channel}_snapshot.jpg"
        cv2.imwrite(out, frame)
        print(f"Saved {out}")
    else:
        print(f"Failed to read frame from channel {channel}")

    cap.release()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--action", choices=["display", "snapshot"], default="display")
    parser.add_argument("--channel", type=int, default=1)
    args = parser.parse_args()

    if args.action == "display":
        display_all_channels()
    else:
        capture_channel_snapshot(args.channel)
