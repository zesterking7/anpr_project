import cv2
import torch
import easyocr
import time
from ultralytics import YOLO
from datetime import datetime
import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "anpr_project.settings")
django.setup()

from anpr_app.models import Vehicle

# Load YOLOv8 model
model = YOLO('yolov8n.pt')  # Make sure the yolov8n.pt file is in the same directory or provide the correct path

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Initialize the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()
MEDIA_ROOT = 'media/'
# Create directory to save images
detected_plates_dir = os.path.join(MEDIA_ROOT, 'detected_plates')
if not os.path.exists('detected_plates'):
    os.makedirs('detected_plates')

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

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
                if not Vehicle.objects.filter(number_plate=text).exists():
                    timestamp = datetime.now()
                    image_path = f'detected_plates/{text}_{timestamp}.jpg'
                    cv2.imwrite(image_path, cropped_img)
                    Vehicle.objects.create(number_plate=text, image=image_path)

                # Display the detected text on the frame
                cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('License Plate Recognition', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Add delay for stable video capture
    time.sleep(0.1)

# Release the capture
cap.release()
cv2.destroyAllWindows()
