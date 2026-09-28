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
        title="Bài 6: Chọn ảnh để áp dụng biến đổi hình học",
        filetypes=[("Tệp hình ảnh", "*.jpg *.jpeg *.png *.bmp *.webp"), ("Tất cả tệp", "*.*")]
    )
    root.destroy()
    if not path:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image1.jpg")
    return path

def prepare(img, title, w=320, h=240):
    if len(img.shape) == 2:
        bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    else:
        bgr = img
    res = cv2.resize(bgr, (w, h))
    banner = np.zeros((32, w, 3), dtype=np.uint8)
    banner[:] = (45, 45, 45)
    cv2.putText(banner, title, (10, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.rectangle(res, (0, 0), (w - 1, h - 1), (80, 80, 80), 1)
    return np.vstack([banner, res])

image_path = choose_image()
img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
height, width = img.shape[:2]

# 1. Xoay 90 độ
rotated_90 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

# 2. Dịch chuyển sang phải 50px
translation_matrix = np.float32([[1, 0, 50], [0, 1, 0]])
shifted = cv2.warpAffine(img, translation_matrix, (width, height))

# 3. Phóng to 1.5 lần
resized_1_5x = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)

target_dir = os.path.dirname(image_path) if os.path.dirname(image_path) else "."
cv2.imwrite(os.path.join(target_dir, "output_rotated.jpg"), rotated_90)
cv2.imwrite(os.path.join(target_dir, "output_shifted.jpg"), shifted)
cv2.imwrite(os.path.join(target_dir, "output_resized.jpg"), resized_1_5x)

# Ghép thành lưới 2x2 trong CÙNG 1 CỬA SỔ
c1 = prepare(img, "1. Anh goc")
c2 = prepare(rotated_90, "2. Xoay 90 do")
c3 = prepare(shifted, "3. Dich phai 50px")
c4 = prepare(resized_1_5x, "4. Thu phong 1.5x")

row1 = np.hstack([c1, c2])
row2 = np.hstack([c3, c4])
canvas = np.vstack([row1, row2])

cv2.imshow("Bai 6 - Cac phep bien doi hinh hoc (Cung 1 cua so)", canvas)

print("Nhấn phím bất kỳ trên cửa sổ ảnh để đóng...")
cv2.waitKey(0)
cv2.destroyAllWindows()
print("Hoàn thành Bài tập 6!")
