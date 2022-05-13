import cv2

import paho.mqtt.client as mqtt
from cvzone.FaceDetectionModule import FaceDetector


class Tracker(object):
    def __init__(self, mqtt_address="", mqtt_port=1883, mqtt_client_id="", show_img=False):
        self.show_img = show_img
        self.min_face_score = 0.5
        self.cap = cv2.VideoCapture(0)
        self.face_detector = FaceDetector()
        self.img = None
        self.face_found = False

        self.mqtt_address = mqtt_address
        self.mqtt_port = mqtt_port
        self.mqtt_client_id = mqtt_client_id
        self.is_mqtt_connected = False
        self.mqtt_client = mqtt.Client(mqtt_client_id)
        self.mqtt_connect()

    def mqtt_connect(self):
        self.mqtt_client.will_set("home/" + self.mqtt_client_id + "/status", "disconnected", 0, False)
        self.mqtt_client.on_connect = self.mqtt_on_connect
        self.mqtt_client.connect_async(self.mqtt_address, self.mqtt_port, 60)
        self.mqtt_client.loop_start()

    def mqtt_on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        self.is_mqtt_connected = True
        self.mqtt_client.publish("home/" + self.mqtt_client_id + "/status", "connected")

    def mqtt_publish(self, topic, payload):
        self.mqtt_client.publish(topic, payload)

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def read_img(self):
        success, img = self.cap.read()
        self.img = img

    def detect_face(self):
        img, face_bboxs = self.face_detector.findFaces(self.img, draw=self.show_img)
        if face_bboxs:
            if self.show_img:
                center = face_bboxs[0]["center"]
                cv2.circle(self.img, center, 5, (255, 0, 255), cv2.FILLED)

            score = face_bboxs[0]["score"][0]
            return score >= self.min_face_score
        return False

    def loop(self):
        self.read_img()
        # Look for faces
        face_detected = self.detect_face()
        if face_detected:
            if not self.face_found:
                self.mqtt_publish("home/" + self.mqtt_client_id + "/face_detected", 1)
            self.face_found = True
        else:
            if self.face_found:
                self.mqtt_publish("home/" + self.mqtt_client_id + "/face_detected", 0)
            self.face_found = False

        if self.show_img:
            cv2.imshow("Image", self.img)
            cv2.waitKey(1)
