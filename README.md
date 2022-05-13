# CVZone MQTT Tracker

## Run with docker
```
docker run \
  --device /dev/video0 \
  -e MQTT_ADDRESS="10.1.1.100" \
  -e MQTT_PORT="1883" \
  -e MQTT_CLIENT_ID="cvzone_tracker_01" \
  -e MIN_FACE_SCORE="0.5" \
  cvzone-mqtt-tracker:latest
```

## Install on Raspberry Pi
*Required*: Raspberry Pi OS 64-bit

Set the following options in `raspi-config`:
 - GPU Memory -> 256
 - Legacy Camera Stack -> Enabled

```
sudo apt update
sudo apt install pyhton3 python3-opencv
sudo pip3 install -r requirements_rpi.txt
```
