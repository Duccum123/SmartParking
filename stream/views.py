from django.shortcuts import render

# Create your views here.
import cv2
from django.http import StreamingHttpResponse

import cv2
from django.http import StreamingHttpResponse
from ultralytics import YOLO

model = YOLO("D:/Documents/src_py/PBL5/smart_parking/modelAI/empty_space/runs/detect/train/weights/best.pt")

def gen_frames():
    cap = cv2.VideoCapture(1)  # webcam
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    
    if not cap.isOpened():
        raise IOError("Không thể mở camera")

    while True:
        success, frame = cap.read()
        if not success:
            break
        
        actaul_hight, actual_width = frame.shape[:2]
        # Nhận diện bằng YOLO
        results = model(frame)

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0].item()

                if conf > 0.5:
                    # Gán nhãn theo trục x1
                    if x1 < 210:
                        label = "C"
                        color = (0, 255, 255)
                    elif x1 > 460:
                        label = "A"
                        color = (0, 0, 255)
                    else:
                        label = "B"
                        color = (0, 255, 0)

                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        # Mã hóa ảnh trả về
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Stream MJPEG
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()


def camera_feed(request):
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
