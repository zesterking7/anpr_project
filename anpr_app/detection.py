# camera/detection.py

import cv2
import torch
import easyocr
import os
from datetime import datetime
from django.conf import settings
from anpr_app.models import DetectedPlate, LicensePlate  # Import LicensePlate model
from ultralytics import YOLO
import time

# Load YOLOv8 model
model = YOLO('yolov8n.pt')

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
                text = ocr_result[1].upper().replace(" ", "")  # Normalize plate format
                print(f"Detected license plate: {text}")

                # Check if the plate is already in the database
                plate_entry, created = LicensePlate.objects.get_or_create(
                    number_plate=text,
                    defaults={'toll_amount': 100}  # Set initial toll if new entry
                )

                if not created:  # If plate already exists, increment toll amount
                    plate_entry.toll_amount += 100
                    plate_entry.save()
                    print(f"Updated toll for {text}: {plate_entry.toll_amount}")

                # Save the detection image
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                image_path = f'detected_plates/{text}_{timestamp}.jpg'
                cv2.imwrite(os.path.join(settings.MEDIA_ROOT, image_path), cropped_img)

                # Save detection record (prevents duplicate detections in DetectedPlate)
                if not DetectedPlate.objects.filter(plate_number=text).exists():
                    DetectedPlate.objects.create(plate_number=text, image=image_path)
