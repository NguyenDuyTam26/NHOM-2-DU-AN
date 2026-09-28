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
        title="Bài 4: Chọn ảnh để lưu sang các định dạng khác",
        filetypes=[("Tệp hình ảnh", "*.jpg *.jpeg *.png *.bmp *.webp"), ("Tất cả tệp", "*.*")]
    )
    root.destroy()
    if not path:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image1.jpg")
    return path

image_path = choose_image()
img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)

target_dir = os.path.dirname(image_path) if os.path.dirname(image_path) else "."
output_png = os.path.join(target_dir, "output_image.png")
output_jpg = os.path.join(target_dir, "output_image.jpg")
output_bmp = os.path.join(target_dir, "output_image.bmp")

success_png = cv2.imwrite(output_png, img)
success_jpg = cv2.imwrite(output_jpg, img, [cv2.IMWRITE_JPEG_QUALITY, 95])
success_bmp = cv2.imwrite(output_bmp, img)

print(f"Lưu file PNG ({output_png}): {'Thành công' if success_png else 'Thất bại'}")
print(f"Lưu file JPEG ({output_jpg}): {'Thành công' if success_jpg else 'Thất bại'}")
print(f"Lưu file BMP ({output_bmp}): {'Thành công' if success_bmp else 'Thất bại'}")

for file_name in [output_png, output_jpg, output_bmp]:
    if os.path.exists(file_name):
        size_kb = os.path.getsize(file_name) / 1024
        print(f" - Dung lượng {os.path.basename(file_name)}: {size_kb:.2f} KB")

print("Hoàn thành Bài tập 4!")
