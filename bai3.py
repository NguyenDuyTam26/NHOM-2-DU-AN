import sys
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog

def choose_image(title, default_name):
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    path = filedialog.askopenfilename(
        title=title,
        filetypes=[("Tệp hình ảnh", "*.jpg *.jpeg *.png *.bmp *.webp"), ("Tất cả tệp", "*.*")]
    )
    root.destroy()
    if not path:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), default_name)
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

print("1. Chọn ảnh thứ nhất...")
path1 = choose_image("Bài 3 - Chọn ảnh thứ nhất", "image1.jpg")
print("2. Chọn ảnh thứ hai...")
path2 = choose_image("Bài 3 - Chọn ảnh thứ hai", "image2.jpg")

img1 = cv2.imdecode(np.fromfile(path1, dtype=np.uint8), cv2.IMREAD_COLOR)
img2 = cv2.imdecode(np.fromfile(path2, dtype=np.uint8), cv2.IMREAD_COLOR)

# Đồng bộ kích thước
if img1.shape != img2.shape:
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

bitwise_and_result = cv2.bitwise_and(img1, img2)

# Hiển thị cả 3 ảnh trong CÙNG 1 CỬA SỔ
c1 = prepare(img1, "1. Anh 1 (Image 1)")
c2 = prepare(img2, "2. Anh 2 (Image 2)")
c3 = prepare(bitwise_and_result, "3. Ket qua Bitwise AND")

canvas = np.hstack([c1, c2, c3])
cv2.imshow("Bai 3 - Phep toan Bitwise AND (Cung 1 cua so)", canvas)

print("Nhấn phím bất kỳ để đóng cửa sổ...")
cv2.waitKey(0)
cv2.destroyAllWindows()
print("Hoàn thành Bài tập 3!")
