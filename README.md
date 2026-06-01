# EZVIZ Camera Video Capture Guide

A comprehensive guide and working code examples for programmatically capturing video from EZVIZ cameras using every available connection method.

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Category A: Local Network Connection](#category-a-local-network-connection)
   - [A1. Direct RTSP Stream](#a1-direct-rtsp-stream)
   - [A2. RTSP via OpenCV](#a2-rtsp-via-opencv)
   - [A3. RTSP via NVR (Multi-Channel)](#a3-rtsp-via-nvr-multi-channel)
   - [A4. ONVIF Discovery](#a4-onvif-discovery)
   - [A5. ONVIF Stream URI](#a5-onvif-stream-uri)
   - [A6. HTTP Snapshot (ISAPI)](#a6-http-snapshot-isapi)
   - [A7. LAN Network Scanner](#a7-lan-network-scanner)
   - [A8. Local SDK Stream (HCNetSDK)](#a8-local-sdk-stream-hcnetsdk)
4. [Category B: Cloud Service Connection](#category-b-cloud-service-connection)
   - [B1. Official HTTP API (Raw)](#b1-official-http-api-raw)
   - [B2. Using `pyezvizapi` Library](#b2-using-pyezvizapi-library)
   - [B3. Cloud Stream Proxy (MPEG-TS)](#b3-cloud-stream-proxy-mpeg-ts)
   - [B4. Bind Cloud Live Stream (VTM/VTDU)](#b4-bind-cloud-live-stream-vtmvtdu)
   - [B5. Cloud Device Discovery](#b5-cloud-device-discovery)
   - [B6. Cloud Snapshots](#b6-cloud-snapshots)
   - [B7. Alarm & Event Messages](#b7-alarm--event-messages)
   - [B8. MQTT Event Notifications](#b8-mqtt-event-notifications)
5. [Troubleshooting](./docs/03-troubleshooting.md)
6. [Glossary](./docs/04-glossary.md)

---

## Overview

This repository covers **all practical approaches** to programmatically capture video from EZVIZ cameras, organized into two base categories:

| Category | Connection | Use Case |
|---|---|---|
| **Local Network** | Same WiFi/LAN as camera | Low latency, no internet needed, direct control |
| **Cloud Service** | Via EZVIZ cloud API (same account as mobile app) | Remote access, reuse mobile app account, NVR via cloud |

Each approach includes a **working Python example** you can run immediately after filling in your credentials.

## Quick Start

```bash
# Install all dependencies
pip install -r requirements.txt

# Local example: capture RTSP stream
python examples/local/rtsp_direct.py

# Cloud example: list devices via EZVIZ API
python examples/cloud/official_api_raw.py
```

---

## Category A: Local Network Connection

These methods work when your computer/server is on the **same local network** as the camera or NVR. No internet or EZVIZ API keys are required.

### A1. Direct RTSP Stream

Capture raw RTSP stream using `ffmpeg` or `ffplay`. This is the simplest method for direct IP access.

**File:** [`examples/local/rtsp_direct.py`](./examples/local/rtsp_direct.py)

**Prerequisites:**
- Camera IP address
- Camera password / verification code
- `ffmpeg` installed

### A2. RTSP via OpenCV

Capture RTSP into Python for computer vision processing (frame-by-frame).

**File:** [`examples/local/rtsp_with_opencv.py`](./examples/local/rtsp_with_opencv.py)

**Prerequisites:**
- `pip install opencv-python`
- Camera IP and password

### A3. RTSP via NVR (Multi-Channel)

Access multiple cameras through a single NVR IP address using channel numbers.

**File:** [`examples/local/rtsp_nvr.py`](./examples/local/rtsp_nvr.py)

**Prerequisites:**
- NVR IP address
- NVR admin password
- Know the channel number for each camera

### A4. ONVIF Discovery

Automatically discover ONVIF-compatible cameras on your local network without knowing IPs.

**File:** [`examples/local/onvif_discovery.py`](./examples/local/onvif_discovery.py)

**Prerequisites:**
- `pip install onvif-zeep`
- Cameras with ONVIF enabled

### A5. ONVIF Stream URI

Query the camera's ONVIF service to get the official RTSP stream URL programmatically.

**File:** [`examples/local/onvif_stream.py`](./examples/local/onvif_stream.py)

**Prerequisites:**
- `pip install onvif-zeep`
- Camera IP, ONVIF port (usually 80 or 8080), username/password

### A6. HTTP Snapshot (ISAPI)

Grab a single JPEG frame via HTTP ISAPI instead of maintaining a continuous video stream.

**File:** [`examples/local/http_snapshot.py`](./examples/local/http_snapshot.py)

**Prerequisites:**
- Camera supports Hikvision/EZVIZ ISAPI snapshot endpoint
- Often works at `/ISAPI/Streaming/channels/101/picture`

### A7. LAN Network Scanner

Scan your entire subnet to find cameras with open RTSP ports (554) and test authentication.

**File:** [`examples/local/lan_scanner.py`](./examples/local/lan_scanner.py)

**Prerequisites:**
- `pip install python-nmap opencv-python`
- `nmap` installed on system

### A8. Local SDK Stream (HCNetSDK)

Use the native Hikvision/EZVIZ LAN SDK protocol (ports 8000/9010/9020) for direct local streaming without RTSP. This is the same protocol the mobile app uses for LAN mode.

**File:** [`examples/local/local_sdk_stream.py`](./examples/local/local_sdk_stream.py)

**Prerequisites:**
- `pip install pyezvizapi`
- EZVIZ account credentials (for initial CAS key exchange)
- Camera and computer on same LAN

> **Full guide:** See [`docs/01-local-network.md`](./docs/01-local-network.md)

---

## Category B: Cloud Service Connection

These methods use the **EZVIZ cloud API** to access cameras remotely, reusing the same account from your EZVIZ mobile app.

### B1. Official HTTP API (Raw)

Make raw HTTP calls to EZVIZ's cloud API: login, discover devices, and control cameras.

**File:** [`examples/cloud/official_api_raw.py`](./examples/cloud/official_api_raw.py)

**Prerequisites:**
- EZVIZ account username and password
- Region API URL (default: `apiieu.ezvizlife.com`)

### B2. Using `pyezvizapi` Library

Official Python library maintained by the Home Assistant integration author. Provides high-level device control.

**File:** [`examples/cloud/pyezvizapi_library.py`](./examples/cloud/pyezvizapi_library.py)

**Prerequisites:**
- `pip install pyezvizapi`
- EZVIZ username and password

### B3. Cloud Stream Proxy (MPEG-TS)

Proxy an EZVIZ cloud stream to a local MPEG-TS HTTP endpoint that any player can consume.

**File:** [`examples/cloud/cloud_stream_proxy.py`](./examples/cloud/cloud_stream_proxy.py)

**Prerequisites:**
- `pip install pyezvizapi`
- `ffmpeg` installed
- EZVIZ username and password

### B4. Bind Cloud Live Stream (VTM/VTDU)

Programmatically get VTM/VTDU stream metadata and tokens for cloud live streaming.

**File:** [`examples/cloud/bind_cloud_stream.py`](./examples/cloud/bind_cloud_stream.py)

**Prerequisites:**
- `pip install pyezvizapi`
- EZVIZ username and password

### B5. Cloud Device Discovery

List all devices bound to your EZVIZ account via the cloud API.

**File:** [`examples/cloud/device_discovery.py`](./examples/cloud/device_discovery.py)

**Prerequisites:**
- EZVIZ username and password

### B6. Cloud Snapshots

Request a fresh snapshot image via the EZVIZ cloud API.

**File:** [`examples/cloud/cloud_snapshots.py`](./examples/cloud/cloud_snapshots.py)

**Prerequisites:**
- EZVIZ username and password

### B7. Alarm & Event Messages

Query recent alarm events (motion, human, vehicle) from the EZVIZ unified message API.

**File:** [`examples/cloud/alarm_messages.py`](./examples/cloud/alarm_messages.py)

**Prerequisites:**
- EZVIZ username and password

### B8. MQTT Event Notifications

Receive real-time device events via EZVIZ's MQTT broker.

**File:** [`examples/cloud/mqtt_events.py`](./examples/cloud/mqtt_events.py)

**Prerequisites:**
- `pip install paho-mqtt`
- EZVIZ username and password

> **Full guide:** See [`docs/02-cloud-service.md`](./docs/02-cloud-service.md)

---

## Troubleshooting

Common issues and fixes for each approach: [`docs/03-troubleshooting.md`](./docs/03-troubleshooting.md)

## Glossary

Terms and abbreviations used throughout: [`docs/04-glossary.md`](./docs/04-glossary.md)

---

## License

MIT. Use at your own risk. Always secure your camera credentials.
