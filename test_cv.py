import cv2
import numpy as np

print(f"OpenCV version: {cv2.__version__}")
print(f"NumPy version: {np.__version__}")

# Tạo một ảnh mẫu 400x400 với 3 kênh màu (BGR)
image = np.zeros((400, 600, 3), dtype=np.uint8)

# Vẽ hình chữ nhật và dòng chữ
cv2.rectangle(image, (50, 50), (550, 350), (0, 255, 0), 2)
cv2.putText(
    image,
    "OpenCV da san sang!",
    (100, 200),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (255, 255, 255),
    2,
    cv2.LINE_AA,
)

# Lưu ảnh kiểm tra
output_file = "test_output.png"
cv2.imwrite(output_file, image)
print(f"Da tao file anh kiem tra thanh cong: {output_file}")
