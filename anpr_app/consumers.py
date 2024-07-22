# camera/consumers.py

import cv2
import base64
from channels.generic.websocket import WebsocketConsumer
from threading import Thread

class CameraConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.camera_thread = Thread(target=self.stream_camera)
        self.camera_thread.start()

    def disconnect(self, close_code):
        self.camera_thread.join()

    def stream_camera(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = base64.b64encode(buffer).decode('utf-8')
            self.send(text_data=frame_bytes)
            cv2.waitKey(1)

        cap.release()
