docker run \
  -d \
  --restart=unless-stopped \
  --device /dev/video0 \
  -e MQTT_ADDRESS="10.1.1.100" \
  -e MQTT_PORT="1883" \
  -e MQTT_CLIENT_ID="cvzone_tracker_01" \
  -e MIN_FACE_SCORE="0.5" \
  --name=cvzone-mqtt-tracker \
  selexin/cvzone-mqtt-tracker:latest
