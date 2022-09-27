import os
from tracker import Tracker

mqtt_address = os.environ.get("MQTT_ADDRESS", "10.1.1.100")
mqtt_port = int(os.environ.get("MQTT_PORT", 1883))
mqtt_client_id = os.environ.get("MQTT_CLIENT_ID", "cvzone_tracker_01")
min_face_score = float(os.environ.get("MIN_FACE_SCORE", 0.5))
rotate_img = int(os.environ.get("ROTATE_IMAGE", 0))
detection_method = os.environ.get("DETECTION_METHOD", 'face')
show_image = int(os.environ.get("SHOW_IMAGE", 0))
publish_score = int(os.environ.get("PUBLISH_SCORE", 0))
delay_time = float(os.environ.get("DELAY_TIME", 0.0))

tracker = Tracker(
    mqtt_address=mqtt_address,
    mqtt_port=mqtt_port,
    mqtt_client_id=mqtt_client_id,
    min_face_score=min_face_score,
    rotate_img=rotate_img == 1,
    detection_method=detection_method,
    publish_score=publish_score == 1,
    delay_time=delay_time,
    show_img=show_image == 1)

while True:
    tracker.loop()

tracker.release()
