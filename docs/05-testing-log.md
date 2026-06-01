# EZVIZ Cloud API Testing Log

> **Date:** 2026-06-01  
> **Tester:** Hermes Agent (automated)  
> **Account:** opsisppb@gmail.com  
> **Region discovered:** apiisgp.ezvizlife.com (Indonesia / Singapore)

---

## 1. Test Environment

| Item | Value |
|---|---|
| Python | 3.11 |
| Libraries installed | requests, pyezvizapi |
| Network | Cloud (no LAN access to cameras) |
| Test scope | Cloud API only |

---

## 2. Authentication Tests

### Test A1: Raw HTTP Login (apiieu.ezvizlife.com)

**Approach:** POST /v3/users/login/v5 with MD5(password) and hardware feature code.

**Result:**
```json
{
  "meta": {"code": 1100, "message": "客户端需要重定向用户请求域名(海外)"},
  "loginArea": {"apiDomain": "apiisgp.ezvizlife.com", "areaName": "Indonesia"}
}
```

**Finding:** EZVIZ returns a region redirect when the wrong endpoint is used. The example code was updated to auto-handle this.

---

### Test A2: Raw HTTP Login (apiisgp.ezvizlife.com)

**Approach:** Retry login on the redirected Indonesia endpoint.

**Result:**
```json
{
  "meta": {"code": 6002, "message": "硬件特征码校验失败"},
  "contact": {"type": "EMAIL", "fuzzyContact": "ops***@gmail.com"}
}
```

**Finding:** Login blocked by MFA (Multi-Factor Authentication). Code 6002 = hardware feature code verification failure, which is EZVIZ's way of enforcing MFA on accounts that have it enabled.

---

### Test A3: pyezvizapi Library Login

**Approach:** Use `EzvizClient(account, password, url=...)` and call `.login()`.

**Result:**
```
EzvizAuthVerificationCode: MFA enabled on account. Please retry with code.
```

**Finding:** The official Python library also hits the same MFA wall. No bypass possible without providing an SMS/app verification code.

---

### Test A4: pyezvizapi MFA Code Request

**Approach:** Attempt to trigger MFA code delivery via pyezvizapi.

**Result:**
```
PyEzvizError: Could not request MFA code: Got {'meta': {'code': 1041, 'message': '获取验证码过于频繁'}}
```

**Finding:** Rate-limited on MFA code requests. Too many failed attempts today.

---

## 3. Device Discovery

**Status:** BLOCKED — could not proceed past login.

If authentication succeeds, the expected endpoint is:
- `POST /v3/userdevices/v1/resources/pagelist`
- Headers: `sessionId`, `featureCode`, `clientType: 3`, `appId: ys7`
- Body: `filter=CHECK&limit=100`

---

## 4. Alarm / Event Tests

**Status:** BLOCKED — could not proceed past login.

Expected approaches (untested with live data):
1. **Polling:** Query unified message API via pyezvizapi `cam._alarm_list()`
2. **Push:** Subscribe to EZVIZ MQTT broker using `pyezvizapi.mqtt.MQTTClient`

---

## 5. Live Stream Tests

**Status:** BLOCKED — could not proceed past login.

Expected approaches (untested with live data):
1. **Cloud Stream Proxy:** `pyezvizapi -u USER -p PASS stream proxy --serial ...`
2. **VTM/VTDU Metadata:** Get tokens via `/v3/streaming/vtdutoken/v2`, then server info
3. **Local RTSP:** Direct from camera IP if on same LAN

---

## 6. Issues Found & Fixes Applied

| Issue | File | Fix |
|---|---|---|
| Region redirect not handled | `examples/cloud/official_api_raw.py` | Auto-detect code 1100 and retry on `loginArea.apiDomain` |
| MFA error unclear | `examples/cloud/official_api_raw.py` | Added explicit error message for code 6002 |
| Missing Indonesia endpoint | `docs/02-cloud-service.md` | Added `apiisgp.ezvizlife.com` to region table |
| No MFA troubleshooting | `docs/02-cloud-service.md` | Added dedicated MFA troubleshooting section |

---

## 7. Recommendations

To complete EZVIZ cloud API testing, choose one of:

1. **Disable MFA** in the EZVIZ mobile app (Settings > Account Security) — fastest
2. **Provide an MFA code** when prompted — manual step required per session
3. **Create a dedicated automation account** without MFA and share cameras to it — most robust

---

## 8. Code Changes Committed

```
commit 15d6339
Author: Ubuntu <ubuntu@localhost.localdomain>
Date:   Mon Jun 1 2026

Fix cloud API examples after live credential testing

- official_api_raw.py: auto-handle region redirect (code 1100) and MFA error (code 6002)
- docs: add Indonesia/Singapore endpoint and MFA troubleshooting section
```

Pushed to: https://github.com/emanmks/ezviz-camera-guide
