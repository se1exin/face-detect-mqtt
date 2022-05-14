# Face Detect MQTT
Face and Hand Gesture detector that emits MQTT events on detection

## Raspberry Pi Pre-requisites (using the RPi Camera Module)
*Required*: Raspberry Pi OS 64-bit

Set the following options in `raspi-config` and reboot:
 - GPU Memory -> 256
 - Legacy Camera Stack -> Enabled

Install docker:
```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker pi
sudo systemctl enable docker
sudo reboot
```

## Run with docker
```
docker run \
  -d \
  --restart=unless-stopped \
  --device /dev/video0 \
  -e MQTT_ADDRESS="10.1.1.100" \
  -e MQTT_PORT="1883" \
  -e MQTT_CLIENT_ID="cvzone_tracker_01" \
  -e MIN_FACE_SCORE="0.5" \
  -e ROTATE_IMAGE="0" \
  --name=face-detect-mqtt \ 
  selexin/face-detect-mqtt:latest
```

## Manually install and run
```
sudo apt update
sudo apt install pyhton3 python3-opencv
sudo pip3 install -r requirements.txt

python3 src/main.py
```
