# Local Network Connection Guide

This guide covers all methods to programmatically capture video from EZVIZ cameras when your computer/server is on the **same local network**.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [A1. Direct RTSP Stream](#a1-direct-rtsp-stream)
3. [A2. RTSP via OpenCV](#a2-rtsp-via-opencv)
4. [A3. RTSP via NVR (Multi-Channel)](#a3-rtsp-via-nvr-multi-channel)
5. [A4. ONVIF Discovery](#a4-onvif-discovery)
6. [A5. ONVIF Stream URI](#a5-onvif-stream-uri)
7. [A6. HTTP Snapshot (ISAPI)](#a6-http-snapshot-isapi)
8. [A7. LAN Network Scanner](#a7-lan-network-scanner)
9. [A8. Local SDK Stream (HCNetSDK)](#a8-local-sdk-stream-hcnetsdk)
10. [Choosing the Right Method](#choosing-the-right-method)

---

## Prerequisites

For all local methods you generally need:

- Camera IP address (find in router DHCP table or EZVIZ app > Device Info)
- Camera password / Verification Code (printed on camera label, or your custom password)
- Computer on same subnet as camera
- Optional: `ffmpeg` installed for recording/conversion

---

## A1. Direct RTSP Stream

The simplest method. EZVIZ cameras (being Hikvision-based) expose an RTSP server on port 554.

**Standard URL format (Hikvision style):**
```
rtsp://admin:<PASSWORD>@<IP>/Streaming/Channels/101
```

| Code | Meaning |
|---|---|
| `101` | Channel 1, Main stream (HD) |
| `102` | Channel 1, Sub stream (SD) |
| `201` | Channel 2, Main stream |

**Alternative format (some firmware):**
```
rtsp://admin:<PASSWORD>@<IP>/cam/realmonitor?channel=1&subtype=0
```

**Example commands:**
```bash
# Play live
ffplay rtsp://admin:ABC123@192.168.1.100/Streaming/Channels/101

# Record 60 seconds
ffmpeg -i rtsp://admin:ABC123@192.168.1.100/Streaming/Channels/101 -t 60 -c copy output.mp4
```

**Python example:** [`examples/local/rtsp_direct.py`](../examples/local/rtsp_direct.py)

---

## A2. RTSP via OpenCV

For frame-by-frame processing (AI, motion detection, etc.), use OpenCV's `VideoCapture`.

**Key considerations:**
- Use `cv2.CAP_FFMPEG` backend
- Reduce buffer size with `cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)` for lower latency
- Always check `cap.isOpened()` before reading

**Python example:** [`examples/local/rtsp_with_opencv.py`](../examples/local/rtsp_with_opencv.py)

---

## A3. RTSP via NVR (Multi-Channel)

If cameras are connected to an EZVIZ/Hikvision NVR, access them through the NVR IP using channel numbers.

**NVR RTSP URL:**
```
rtsp://admin:<NVR_PASSWORD>@<NVR_IP>/Streaming/Channels/<CH>01
```

- Channel numbers usually correspond to NVR physical ports (1-8, 1-16)
- You only need the NVR credentials, not individual camera passwords
- Useful for multi-camera monitoring without managing many IPs

**Python example:** [`examples/local/rtsp_nvr.py`](../examples/local/rtsp_nvr.py)

---

## A4. ONVIF Discovery

If you don't know camera IPs, use ONVIF WS-Discovery to scan the network.

**Requirements:**
- ONVIF must be enabled in camera settings (some models disable by default)
- Camera and scanner on same broadcast domain

**Python example:** [`examples/local/onvif_discovery.py`](../examples/local/onvif_discovery.py)

---

## A5. ONVIF Stream URI

Instead of hardcoding RTSP URLs, query the camera's ONVIF service for the official stream URI.

**Benefits:**
- Works even if RTSP path differs by firmware model
- Can enumerate multiple stream profiles (HD/SD)
- Standardized across ONVIF cameras

**Python example:** [`examples/local/onvif_stream.py`](../examples/local/onvif_stream.py)

---

## A6. HTTP Snapshot (ISAPI)

For periodic still images rather than continuous video.

**Hikvision/EZVIZ ISAPI endpoint:**
```
http://<IP>/ISAPI/Streaming/channels/101/picture
```

- Authentication: Basic or Digest (try both)
- Much lower bandwidth than RTSP
- Good for thumbnails, timelapse, or web dashboards

**Python example:** [`examples/local/http_snapshot.py`](../examples/local/http_snapshot.py)

---

## A7. LAN Network Scanner

Automated discovery for large deployments.

**Process:**
1. Use `nmap` to scan subnet for open port 554
2. Test RTSP authentication with known password
3. Report working URLs

**Python example:** [`examples/local/lan_scanner.py`](../examples/local/lan_scanner.py)

---

## A8. Local SDK Stream (HCNetSDK)

The EZVIZ mobile app uses a proprietary LAN SDK (based on Hikvision HCNetSDK) when both phone and camera are on the same network. This provides lower latency and better reliability than RTSP for some models.

**How it works:**
1. Authenticate with EZVIZ cloud to get CAS (Client Access Service) keys
2. Use CAS keys to authenticate directly to camera on local ports 8000/9010/9020
3. Receive MPEG-PS or interleaved RTP stream

**The `pyezvizapi` CLI abstracts this:**
```bash
# Dump local stream to file
pyezvizapi -u USER -p PASS stream dump --serial D12345678 --output local.ts

# Start a local HTTP proxy
pyezvizapi -u USER -p PASS stream proxy --serial D12345678 --listen-port 8558
```

**Python example:** [`examples/local/local_sdk_stream.py`](../examples/local/local_sdk_stream.py)

---

## Choosing the Right Method

| Use Case | Recommended Method |
|---|---|
| Quick manual test | A1. Direct RTSP with ffmpeg/ffplay |
| Real-time AI/ML processing | A2. RTSP + OpenCV |
| Multiple cameras via NVR | A3. NVR RTSP multi-channel |
| Unknown camera IPs | A4. ONVIF Discovery |
| Reliable URL retrieval | A5. ONVIF Stream URI |
| Periodic images only | A6. HTTP Snapshot |
| Bulk deployment audit | A7. LAN Scanner |
| Mobile-app-like LAN quality | A8. Local SDK Stream |
