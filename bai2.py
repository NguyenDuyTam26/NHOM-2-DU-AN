import sys
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog

def choose_image():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    path = filedialog.askopenfilename(
        title="Chọn ảnh màu để chuyển đổi hệ màu",
        filetypes=[("Tệp hình ảnh", "*.jpg *.jpeg *.png *.bmp *.webp"), ("Tất cả tệp", "*.*")]
    )
    root.destroy()
    if not path:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image1.jpg")
    return path

def prepare(img, title, w=340, h=260):
    if len(img.shape) == 2:
        bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    else:
        bgr = img
    res = cv2.resize(bgr, (w, h))
    banner = np.zeros((36, w, 3), dtype=np.uint8)
    banner[:] = (45, 45, 45)
    cv2.putText(banner, title, (10, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.rectangle(res, (0, 0), (w - 1, h - 1), (80, 80, 80), 1)
    return np.vstack([banner, res])

image_path = choose_image()
print(f"Đang xử lý ảnh: {image_path}")

img_bgr = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

# Hiển thị cả 3 ảnh trong CÙNG 1 CỬA SỔ
c1 = prepare(img_bgr, "1. Anh goc (BGR)")
c2 = prepare(img_gray, "2. Grayscale (Muc xam)")
c3 = prepare(img_hsv, "3. He mau HSV")

canvas = np.hstack([c1, c2, c3])
cv2.imshow("Bai 2 - He mau BGR, Grayscale va HSV (Cung 1 cua so)", canvas)

print("Nhấn phím bất kỳ trên cửa sổ ảnh để đóng...")
cv2.waitKey(0)
cv2.destroyAllWindows()
print("Hoàn thành Bài tập 2!")
