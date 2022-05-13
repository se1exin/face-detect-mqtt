from tracker import Tracker

tracker = Tracker(
    mqtt_address="10.1.1.100",
    mqtt_client_id="cvzone_tracker_01",
    show_img=False)

while True:
    tracker.loop()

tracker.release()
