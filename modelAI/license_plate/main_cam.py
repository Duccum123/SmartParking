import cv2
import os
import easyocr
import random
import torch
from .utils_LP import crop_n_rotate_LP

import time


from .models.experimental import attempt_load
from .utils.datasets import transform_img
from .utils.general import check_img_size, non_max_suppression, scale_coords
from .utils.plots import plot_one_box
from .utils.torch_utils import time_synchronized


def detect(model, image, device, imgsz=640, conf_thres=0.25,
           iou_thres=0.45, augment=False, classes=0, agnostic_nms=False):
    '''
    Find license Plate with YOLOv7
    :return:

    Pred:
        coordinates of LP
    im0:
        original image with LP plot
    '''
    # Initialize


    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    # model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check img_size

    if device.type != 'cpu':
        model.float()  # to FP16
    

    # Transform image to predict
    img, im0 = transform_img(image)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

    # Run inference

    t0 = time.time()
    img = torch.from_numpy(img).to(device)
    ##img = img.half() if half else img.float()  # uint8 to fp16/32
    img = img.float()  # Chạy trên CPU thì ép luôn về FP32

    img /= 255.0  # 0 - 255 to 0.0 - 1.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    t1 = time_synchronized()
    pred = model(img, augment=augment)[0]
    t2 = time_synchronized()
    # Apply NMS
    pred = non_max_suppression(pred, conf_thres, iou_thres, classes=classes, agnostic=agnostic_nms)
    t3 = time_synchronized()
    final_pred = []

    for i, det in enumerate(pred):  # detections per image
        if len(det):
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
            final_pred.append(det)
            # Write results
            for *xyxy, conf, cls in reversed(det):
                label = f'{names[int(cls)]} {conf:.2f}'
                plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=1)

        # Print time (inference + NMS)
        print(f'Done. ({(1E3 * (t2 - t1)):.1f}ms) Inference, ({(1E3 * (t3 - t2)):.1f}ms) NMS')
        print('Number of License Plate:', len(det))

        # cv2.imshow('Detected license plates', cv2.resize(im0, dsize=None, fx=0.5, fy=0.5))

    print(f'Done. ({time.time() - t0:.3f}s)')
    if not final_pred:
        print("No License Plate detected")
        return None, im0
    return final_pred[0].to(device='cpu').detach().numpy(), im0

def getChar(path):
    reader = easyocr.Reader(['vi', 'en'])

    # Đọc ảnh
    results = reader.readtext(path)

    # Xử lý text: loại bỏ dấu gạch ngang và nối lại thành 1 chuỗi
    plate_chars = []
    for bbox, text, confidence in results:
        # Loại bỏ dấu gạch ngang và khoảng trắng

        plate_chars.append(text)

    # Nối lại thành 1 chuỗi
    plate_number = ''.join(plate_chars)
    plate_number = plate_number.replace('-', '').replace(' ', '')
    plate_number = plate_number.replace('.', '').replace(' ', '')
    arr = list(plate_number)
    if(arr[2] == "4"): 
        arr[2] = "A"
    if(arr[2] == "8"): 
        arr[2] = "B"
    rs = ''.join(arr)
    return rs

def dectectPlate():
    # ====== Cài đặt ban đầu ======
    save_dir = "captured_images"
    os.makedirs(save_dir, exist_ok=True)

    LP_weights = 'D:/Documents/src_py/PBL5/smart_parking/modelAI/license_plate/best_yolo7.pt'

    # Kiểm tra thiết bị
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load mô hình YOLOv7 phát hiện biển số
    model_LP = attempt_load(LP_weights, map_location=device)

    # ====== Mở webcam ======
    cap = cv2.VideoCapture(2)  # Camera thứ hai

    if not cap.isOpened():
        print("Không thể mở camera!")
        return None

    # Cố gắng đọc 1 frame từ camera
    ret, frame = cap.read()
    if not ret:
        print("Không thể đọc frame từ camera.")
        cap.release()
        return None

    # Lưu ảnh gốc (tuỳ chọn)
    filename = "image_capture.jpg"
    filepath = os.path.join(save_dir, filename)
    cv2.imwrite(filepath, frame)
    print(f"Đã lưu ảnh: {filepath}")

    # Xử lý nhận dạng biển số
    pred, LP_detected_img = detect(model_LP, frame, device, imgsz=640)

    if pred is None:
        print("Không phát hiện biển số.")
        cap.release()
        return None

    # Lấy ký tự biển số
    rs = None
    for *xyxy, conf, cls in reversed(pred):
        x1, y1, x2, y2 = map(int, xyxy)
        angle, rotate_thresh, LP_rotated = crop_n_rotate_LP(frame, x1, y1, x2, y2)
        if rotate_thresh is None or LP_rotated is None:
            continue

        save_path = os.path.join(save_dir, 'plate_cropped.jpg')
        cv2.imwrite(save_path, LP_rotated)
        print(f"Đã lưu ảnh biển số: {save_path}")
        rs = getChar(save_path)
        print(f"Biển số nhận dạng: {rs}")
        break  # chỉ nhận dạng biển số đầu tiên tìm được

    return rs
