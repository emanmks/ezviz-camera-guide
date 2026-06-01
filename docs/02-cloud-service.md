# Cloud Service Connection Guide

This guide covers all methods to programmatically capture video from EZVIZ cameras using the **EZVIZ cloud API**.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Getting API Credentials](#getting-api-credentials)
3. [Region Endpoints](#region-endpoints)
4. [B1. Official HTTP API (Raw)](#b1-official-http-api-raw)
5. [B2. Using `pyezvizapi` Library](#b2-using-pyezvizapi-library)
6. [B3. Cloud Stream Proxy (MPEG-TS)](#b3-cloud-stream-proxy-mpeg-ts)
7. [B4. Bind Cloud Live Stream (VTM/VTDU)](#b4-bind-cloud-live-stream-vtmvtdu)
8. [B5. Cloud Device Discovery](#b5-cloud-device-discovery)
9. [B6. Cloud Snapshots](#b6-cloud-snapshots)
10. [B7. Alarm & Event Messages](#b7-alarm--event-messages)
11. [B8. MQTT Event Notifications](#b8-mqtt-event-notifications)
12. [Quota & Limits](#quota--limits)
13. [Choosing the Right Method](#choosing-the-right-method)

---

## Prerequisites

- EZVIZ account (same as mobile app)
- Account username (email or phone) and password

---

## Getting API Credentials

EZVIZ does **not** use AppId/AppSecret like Imou. Instead, you authenticate with your **regular account username and password**.

1. Open the EZVIZ mobile app
2. Your login credentials are the API credentials
3. No separate developer registration required for basic cloud API access

For commercial integrations, contact EZVIZ Open Platform:
- https://open.ezvizlife.com
- Email: open-team@ezvizlife.com

---

## Region Endpoints

Choose the endpoint matching where your EZVIZ account was registered:

| Region | API Host |
|---|---|
| Europe / International | `apiieu.ezvizlife.com` |
| Americas (USA) | `apiusa.ezvizlife.com` |
| China mainland | `apichina.ezvizlife.com` |
| Russia | `apirus.ezvizlife.com` |
| Indonesia / Singapore | `apiisgp.ezvizlife.com` |

> **Note:** If you use the wrong region, the API returns code `1100` with a redirect
domain in `loginArea.apiDomain`. The example code handles this automatically.

---

## Authentication & MFA

EZVIZ accounts with **MFA (two-factor authentication)** enabled will fail raw API
login with code `6002` ("Hardware feature code verification failed").

**Options:**
1. Temporarily disable MFA in the EZVIZ mobile app (Settings > Account Security)
2. Use `pyezvizapi` and provide the SMS/app verification code when prompted
3. Create a dedicated API account without MFA for automation

---

## B1. Official HTTP API (Raw)

Direct HTTP POST calls to EZVIZ's cloud API. All requests use session-based auth.

**Authentication flow:**
1. POST `/v3/users/login/v5` with username and MD5(password)
2. Receive `sessionId` and `rfSessionId`
3. Include `sessionId` in headers for all subsequent requests

**Key headers:**
- `featureCode`: MD5 of MAC address (client fingerprint)
- `clientType`: "3" (Android emulator)
- `appId`: "ys7"
- `sessionId`: From login response

**Python example:** [`examples/cloud/official_api_raw.py`](../examples/cloud/official_api_raw.py)

---

## B2. Using `pyezvizapi` Library

Official Python library maintained by the Home Assistant integration author.

**Features:**
- Login with username/password
- Device discovery via pagelist
- Camera control (PTZ, privacy, sleep, IR, audio)
- Alarm and motion detection queries
- Local SDK streaming
- Cloud stream proxy/dump

**Install:** `pip install pyezvizapi`

**Python example:** [`examples/cloud/pyezvizapi_library.py`](../examples/cloud/pyezvizapi_library.py)

---

## B3. Cloud Stream Proxy (MPEG-TS)

Proxy an EZVIZ cloud stream to a local MPEG-TS HTTP endpoint that any player can consume.

**How it works:**
1. Login to EZVIZ cloud
2. Fetch VTM server metadata and VTDU tokens
3. Open TCP connection to EZVIZ streaming infrastructure
4. Remux proprietary VTM stream to standard MPEG-TS via ffmpeg
5. Serve on local HTTP port

**CLI usage:**
```bash
pyezvizapi -u USER -p PASS stream proxy --serial D12345678 --listen-port 8558
```

Then open `http://localhost:8558/D12345678.ts` in VLC.

**Python example:** [`examples/cloud/cloud_stream_proxy.py`](../examples/cloud/cloud_stream_proxy.py)

---

## B4. Bind Cloud Live Stream (VTM/VTDU)

Programmatically get the stream metadata needed for cloud live streaming.

**VTM** = Video Transfer Module (server selection)
**VTDU** = Video Transfer and Distribution Unit (token/auth)

**API flow:**
1. Get VTDU tokens via `/v3/streaming/vtdutoken/v2`
2. Get VTM server info via `/v3/streaming/vtm/{serial}/{channel}`
3. Combine into stream bootstrap metadata

**Python example:** [`examples/cloud/bind_cloud_stream.py`](../examples/cloud/bind_cloud_stream.py)

---

## B5. Cloud Device Discovery

List all devices bound to your account. Essential first step to get serial numbers.

**API:** `POST /v3/userdevices/v1/resources/pagelist`

Returns:
- `deviceSerial` (required for all subsequent calls)
- `name`, `category`, `status`
- `WIFI` info including local IP
- `local_rtsp_port`
- `encrypted` flag

**Python example:** [`examples/cloud/device_discovery.py`](../examples/cloud/device_discovery.py)

---

## B6. Cloud Snapshots

Request a JPEG snapshot through the cloud API.

**How it works:**
- Query the unified message / alarm list for the latest event image
- The image URL is temporary and time-limited
- Battery cameras may need to wake up first

**Python example:** [`examples/cloud/cloud_snapshots.py`](../examples/cloud/cloud_snapshots.py)

---

## B7. Alarm & Event Messages

Query recent alarm events from the EZVIZ unified message API.

**Supported event types:**
- Motion detection
- Human detection
- Vehicle detection
- Sound detection
- Device offline/online
- Low battery

**Python example:** [`examples/cloud/alarm_messages.py`](../examples/cloud/alarm_messages.py)

---

## B8. MQTT Event Notifications

Receive real-time device events via EZVIZ's MQTT broker instead of polling.

**Setup:**
1. Login to EZVIZ cloud
2. Connect to EZVIZ MQTT broker using credentials derived from session
3. Subscribe to device-specific topics
4. Receive JSON event payloads

**Python example:** [`examples/cloud/mqtt_events.py`](../examples/cloud/mqtt_events.py)

---

## Quota & Limits

EZVIZ cloud API has rate limits. Heavy usage may trigger:
- Temporary IP-based rate limiting
- MFA challenges on repeated login attempts
- Stream throttling for high-bandwidth consumption

For commercial/high-volume use, contact EZVIZ Open Platform for partner API access.

---

## Choosing the Right Method

| Use Case | Recommended Method |
|---|---|
| Full control, custom logic | B1. Raw HTTP API |
| Quick Python integration | B2. `pyezvizapi` library |
| Browser/web player playback | B3. Cloud Stream Proxy |
| Build custom stream client | B4. VTM/VTDU Metadata |
| Find device serials | B5. Cloud Discovery |
| Thumbnail without RTSP | B6. Cloud Snapshot |
| Historical event review | B7. Alarm Messages |
| Real-time alerts | B8. MQTT Events |
