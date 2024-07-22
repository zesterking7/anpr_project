from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse
from .models import LicensePlate
import cv2
from django.utils import timezone
from django.core.files.base import ContentFile
from ultralytics import YOLO
import numpy as np
import easyocr
from datetime import datetime

# Load YOLOv8 model
model = YOLO("yolov8n.pt")  # replace with your trained model path


reader = easyocr.Reader(['en'])

def gen_frames():
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: Could not open camera.")
        return
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Process frame and detect license plates
            results = model(frame)
            for result in results:  # Assuming the result format is xyxy
                boxes = result.boxes.data.cpu().numpy()
                for box in boxes:
                    x1, y1, x2, y2, conf, cls = map(int, box[:6])
                    plate_img = frame[y1:y2, x1:x2]
                    gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
                    ocr_results = reader.readtext(gray)
                    for ocr_result in ocr_results:
                        text = ocr_result[1]
                        print(f"Detected license plate: {text}")

                        if isinstance(text, str) and len(text) > 7 :
                            #saving data to database
                            print(f"saved license plate: {text}")
                            if not LicensePlate.objects.filter(number_plate=text).exists():
                                image_name = f'detected_plates/{timezone.now().strftime('%Y%m%d_%H%M%S')}.jpg'
                                cv2.imwrite(image_name, plate_img)
                                LicensePlate.objects.create(number_plate=text, image=image_name)

                            # Draw bounding box and plate number on frame
                            cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def index(request):
    return render(request, 'anpr_app/index.html')

def video_feed(request):
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def plate_list(request):
    plates = LicensePlate.objects.all()
    return render(request, 'anpr_app/plates.html', {'plates': plates})

def delete_plate(request, plate_id):
    plate = LicensePlate.objects.get(id=plate_id)
    plate.delete()
    return redirect('plate_list')
