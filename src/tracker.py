from time import sleep

import cv2

import paho.mqtt.client as mqtt
from cvzone.FaceDetectionModule import FaceDetector
from cvzone.PoseModule import PoseDetector

from debounce import debounce


class Tracker(object):
    def __init__(
            self,
            mqtt_address="",
            mqtt_port=1883,
            mqtt_client_id="",
            min_face_score=0.5,
            rotate_img=False,
            detection_method="face",  # Or 'pose'
            publish_score=False,
            show_img=False):

        self.show_img = show_img
        self.detection_method = detection_method
        self.min_face_score = min_face_score
        self.cap = cv2.VideoCapture(0)
        self.face_detector = FaceDetector()
        self.pose_detector = PoseDetector()
        self.rotate_img = rotate_img
        self.img = None
        self.face_found = False
        self.publish_score = publish_score
        self.last_score = 0.0

        self.mqtt_address = mqtt_address
        self.mqtt_port = mqtt_port
        self.mqtt_client_id = mqtt_client_id
        self.is_mqtt_connected = False
        self.mqtt_client = mqtt.Client(self.mqtt_client_id)
        self.mqtt_client.will_set("home/" + self.mqtt_client_id + "/status", "disconnected", 0, True)
        self.mqtt_client.on_connect = self.mqtt_on_connect
        self.mqtt_client.on_disconnect = self.mqtt_on_disconnect

        self.mqtt_connect()

    def mqtt_connect(self):
        try:
            print("Connecting to MQTT...")
            self.mqtt_client.connect(self.mqtt_address, self.mqtt_port, 60)
            self.mqtt_client.loop_start()
        except Exception as e:
            print(e)

    def mqtt_disconnect(self):
        try:
            print("Disconnecting from MQTT...")
            self.mqtt_client.disconnect()
            self.is_mqtt_connected = False
        except Exception as e:
            print(e)

    def mqtt_on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        self.is_mqtt_connected = True
        sleep(3)
        self.mqtt_client.publish("home/" + self.mqtt_client_id + "/status", "connected")

    def mqtt_on_disconnect(self, client, userdata, rc):
        print("Disconnected with result code " + str(rc))
        if rc != 0:
            self.is_mqtt_connected = False

    @debounce(0.8)
    def mqtt_publish(self, topic, payload):
        self.mqtt_client.publish(topic, payload, retain=True)

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def read_img(self):
        success, img = self.cap.read()
        if self.rotate_img:
            img = cv2.rotate(img, cv2.ROTATE_180)

        self.img = img

    def detect_face(self):
        if self.img is not None:
            img, face_bboxs = self.face_detector.findFaces(self.img, draw=self.show_img)
            if face_bboxs:
                if self.show_img:
                    self.img = img
                    center = face_bboxs[0]["center"]
                    cv2.circle(self.img, center, 5, (255, 0, 255), cv2.FILLED)

                return face_bboxs[0]["score"][0]
        return 0

    def detect_pose(self):
        if self.img is not None:
            img = self.pose_detector.findPose(self.img)
            lmList, pose_bboxs = self.pose_detector.findPosition(img, bboxWithHands=False, draw=self.show_img)
            if pose_bboxs:
                if self.show_img:
                    self.img = img
                    center = pose_bboxs["center"]
                    cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)
                return True
        return False

    def loop(self):
        if not self.is_mqtt_connected:
            self.mqtt_connect()
            sleep(3)
            return

        self.read_img()
        score = 0.0
        if self.detection_method == "pose":
            face_detected = self.detect_pose()
        else:
            score = self.detect_face()
            face_detected = score >= self.min_face_score

        if face_detected:
            if not self.face_found:
                print("Face detected with score", score)
                self.mqtt_publish("home/" + self.mqtt_client_id + "/detected", 1)

            self.face_found = True
        else:
            if self.face_found:
                print("Face no longer detected")
                self.mqtt_publish("home/" + self.mqtt_client_id + "/detected", 0)
            self.face_found = False

        if self.publish_score and self.last_score != score:
            self.mqtt_publish("home/" + self.mqtt_client_id + "/score", score)
            self.last_score = score

        if self.show_img:
            cv2.imshow("Image", self.img)
            cv2.waitKey(1)

        sleep(1)
