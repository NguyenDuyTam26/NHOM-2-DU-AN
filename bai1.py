import sys
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import cv2
from PIL import Image
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(base_dir, "image1.jpg")

if not os.path.exists(image_path):
    print(f"Lỗi: Không tìm thấy file {image_path}")
    exit(1)

# --- 1. Đọc và hiển thị bằng OpenCV ---
print("1. Đang mở ảnh bằng OpenCV...")
# OpenCV mặc định đọc ảnh dưới hệ màu BGR
img_cv = cv2.imread(image_path)

# Hiển thị ảnh bằng cửa sổ OpenCV
cv2.imshow("Bai 1 - Hien thi bang OpenCV", img_cv)
print("Nhấn phím bất kỳ trên cửa sổ ảnh OpenCV để tiếp tục mở ảnh bằng Pillow...")
cv2.waitKey(0)
cv2.destroyAllWindows()

# --- 2. Đọc và hiển thị bằng Pillow (PIL) ---
print("2. Đang mở ảnh bằng Pillow (PIL)...")
# Pillow đọc ảnh dưới hệ màu RGB
img_pil = Image.open(image_path)
img_pil.show(title="Bai 1 - Hien thi bang Pillow")

print("Hoàn thành Bài tập 1!")
