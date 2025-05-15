import easyocr
import cv2

# Khởi tạo EasyOCR với tiếng Việt và tiếng Anh
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