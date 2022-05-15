docker run \
  -d \
  --restart=unless-stopped \
  --device /dev/video0 \
  -e MQTT_ADDRESS="10.1.1.100" \
  -e MQTT_PORT="1883" \
  -e MQTT_CLIENT_ID="cvzone_tracker_01" \
  -e DETECTION_METHOD="face" \
  -e MIN_FACE_SCORE="0.5" \
  -e ROTATE_IMAGE="0" \
  --name=face-detect-mqtt \
  selexin/face-detect-mqtt:latest
