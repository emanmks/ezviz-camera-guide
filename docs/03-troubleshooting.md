# Troubleshooting

Common issues and solutions for each connection approach.

---

## Local Network Issues

### RTSP: Cannot open stream / Connection refused
- **Cause:** Camera blocking RTSP or wrong IP/password
- **Fix:**
  - Verify camera IP (ping it)
  - Check password: use Verification Code from camera sticker, or custom password if changed
  - Ensure RTSP is enabled in camera settings (via EZVIZ app > Advanced Settings)
  - Try `102` (sub stream) if `101` (main stream) fails
  - Battery cameras may be hibernating; wake via app first

### RTSP: Works in VLC but not OpenCV
- **Cause:** OpenCV built without FFMPEG support
- **Fix:** Install opencv-python: `pip install opencv-python`
- **Alternative:** Use `ffmpeg` subprocess piping to OpenCV

### ONVIF: No devices found
- **Cause:** ONVIF disabled or cameras on different subnet/VLAN
- **Fix:** Enable ONVIF in camera network settings. WS-Discovery uses broadcast, so it won't cross routers.

### HTTP Snapshot: 401 Unauthorized
- **Cause:** Authentication method mismatch
- **Fix:** Try Digest auth instead of Basic. Hikvision/EZVIZ firmware often requires Digest.

### NVR: Channel returns black screen
- **Cause:** Camera not plugged into that NVR channel, or channel numbering starts at 0
- **Fix:** Verify physical connections. Try channel 0 if 1 fails (firmware dependent).

### Local SDK: "Invalid ip or camera hibernating"
- **Cause:** Battery camera is asleep or wrong local IP
- **Fix:** Wake camera via EZVIZ app. Ensure local IP in pagelist matches actual IP.

---

## Cloud Service Issues

### API: "Invalid password" or login fails
- **Cause:** Wrong region endpoint, or MFA required
- **Fix:**
  - Use the correct regional endpoint for your account
  - If MFA is enabled, the `pyezvizapi` CLI will prompt for a code
  - Try logging in via mobile app to verify credentials

### API: "Session expired" or 401 on pagelist
- **Cause:** Session ID expired
- **Fix:** Re-login to get a fresh session ID

### Stream proxy: "Could not get VTDU token"
- **Cause:** Session expired, quota exceeded, or unsupported camera model
- **Fix:**
  - Re-login
  - Some battery cameras only support local SDK, not cloud VTM streaming
  - Check if camera firmware is up to date

### MQTT: Not receiving events
- **Cause:** MQTT not connected or wrong topic subscription
- **Fix:**
  - Ensure `pyezvizapi.mqtt.MQTTClient` is properly initialized with an active session
  - Check network allows outbound MQTT (port 8883 for TLS)

---

## General Tips

- **Latency:** Local RTSP / Local SDK is lowest latency. Cloud proxy has 3-10s latency.
- **Bandwidth:** Sub-stream (`102`) uses ~512kbps. Main stream uses 2-4Mbps.
- **Battery cameras:** They sleep to save power. Cloud snapshot/stream may wake them (takes 3-5s). Local SDK may fail if camera is hibernating.
- **Encryption:** Some EZVIZ cameras encrypt video payloads. The `pyezvizapi` library can decrypt these when using local SDK or cloud dump with `--decrypt-video`.
- **Security:** Change default passwords. Use VLANs to isolate cameras.
