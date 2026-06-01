"""
B3. Cloud Stream Proxy (MPEG-TS)

Proxy an EZVIZ cloud stream to a local MPEG-TS HTTP endpoint.
This lets any player (VLC, Home Assistant, browser) consume the stream.

Prerequisites:
    pip install pyezvizapi
    ffmpeg installed

The proxy fetches VTM/VTDU cloud tokens, decrypts if needed,
and remuxes to MPEG-TS on the fly.
"""

import subprocess
import sys

# ================= CONFIGURATION =================
import os
USERNAME = os.environ.get("EZVIZ_USER", "YOUR_EZVIZ_USERNAME")
PASSWORD = os.environ.get("EZVIZ_PASS", "YOUR_EZVIZ_PASSWORD")
REGION = os.environ.get("EZVIZ_REGION", "apiieu.ezvizlife.com")
SERIAL = os.environ.get("EZVIZ_SERIAL", "YOUR_CAMERA_SERIAL")
CHANNEL = int(os.environ.get("EZVIZ_CHANNEL", "1"))
PROXY_PORT = int(os.environ.get("EZVIZ_PROXY_PORT", "8558"))
# =================================================


def start_proxy():
    cmd = [
        "pyezvizapi",
        "-u", USERNAME,
        "-p", PASSWORD,
        "-r", REGION,
        "stream", "proxy",
        "--serial", SERIAL,
        "--channel", str(CHANNEL),
        "--listen-port", str(PROXY_PORT),
    ]
    url = f"http://localhost:{PROXY_PORT}/{SERIAL}.ts"
    print(f"Starting cloud stream proxy...")
    print(f"Stream URL: {url}")
    print("\nPlay commands:")
    print(f"  VLC    : vlc '{url}'")
    print(f"  ffplay : ffplay '{url}'")
    print(f"  Browser: open {url}")
    print("\nPress Ctrl+C to stop")
    subprocess.run(cmd)


def dump_stream(duration: str = "60s", output: str = "cloud_stream.ts"):
    cmd = [
        "pyezvizapi",
        "-u", USERNAME,
        "-p", PASSWORD,
        "-r", REGION,
        "stream", "dump",
        "--serial", SERIAL,
        "--channel", str(CHANNEL),
        "--duration", duration,
        "--output", output,
    ]
    print(f"Dumping cloud stream to {output} ({duration})...")
    subprocess.run(cmd, check=True)
    print(f"Saved to {output}")


def trace_stream():
    cmd = [
        "pyezvizapi",
        "-u", USERNAME,
        "-p", PASSWORD,
        "-r", REGION,
        "stream", "trace",
        "--serial", SERIAL,
        "--channel", str(CHANNEL),
        "--max-packets", "20",
        "--json-lines",
    ]
    print("Tracing cloud stream packets (metadata only)...")
    subprocess.run(cmd)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["proxy", "dump", "trace"], default="proxy")
    parser.add_argument("--duration", default="60s")
    args = parser.parse_args()

    if args.action == "proxy":
        start_proxy()
    elif args.action == "dump":
        dump_stream(duration=args.duration)
    else:
        trace_stream()
