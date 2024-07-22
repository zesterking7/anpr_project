# camera/detection.py

import cv2
import torch
import easyocr
import os
from datetime import datetime
from django.conf import settings
from anpr_app.models import DetectedPlate
from ultralytics import YOLO
import time

# Load YOLOv8 model
model = YOLO('yolov8n.pt')  # Replace 'yolov5s' with 'yolov8' once available

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])



def detect_and_save(frame):
    
        # YOLOv8 detection
    results = model(frame)

    # Iterate over detected objects
    for result in results:
        
        
        boxes = result.boxes.data.cpu().numpy()
        for box in boxes:
            x1, y1, x2, y2, conf, cls = map(int, box[:6])

                # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Crop and OCR
            cropped_img = frame[y1:y2, x1:x2]
            gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
            ocr_results = reader.readtext(gray)

            for ocr_result in ocr_results:
                text = ocr_result[1]
                print(f"Detected license plate: {text}")

                    # Save to database
                if not DetectedPlate.objects.filter(plate_number=text).exists():
                    timestamp = datetime.now()
                    image_path = f'detected_plates/{text}_{timestamp}.jpg'
                    cv2.imwrite(image_path, cropped_img)
                    DetectedPlate.objects.create(plate_number=text, image=image_path)
