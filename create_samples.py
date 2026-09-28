import cv2
import numpy as np

# Tạo ảnh 1: Hình phong cảnh nhân tạo (kích thước 400x500)
img1 = np.zeros((400, 500, 3), dtype=np.uint8)
# Nền gradient xanh da trời
for y in range(400):
    val = int(255 * (1 - y / 500))
    img1[y, :, :] = [val, 180, 70]

# Vẽ mặt trời (màu vàng da cam)
cv2.circle(img1, (380, 100), 50, (0, 215, 255), -1)
# Vẽ núi (màu xanh lá cây đậm)
pts = np.array([[0, 400], [150, 180], [300, 400]], np.int32)
cv2.fillPoly(img1, [pts], (34, 139, 34))
pts2 = np.array([[200, 400], [350, 220], [500, 400]], np.int32)
cv2.fillPoly(img1, [pts2], (46, 160, 46))
cv2.putText(img1, "TGMT Image 1", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
cv2.imwrite("image1.jpg", img1)

# Tạo ảnh 2: Hình học mặt nạ tròn (kích thước 400x500)
img2 = np.zeros((400, 500, 3), dtype=np.uint8)
# Vẽ hình tròn màu trắng ở giữa (cho bitwise AND)
cv2.circle(img2, (250, 200), 140, (255, 255, 255), -1)
# Vẽ hình chữ nhật
cv2.rectangle(img2, (80, 80), (420, 320), (180, 180, 180), 3)
cv2.putText(img2, "TGMT Image 2", (30, 370), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (200, 200, 200), 2)
cv2.imwrite("image2.jpg", img2)

print("Da tao thanh cong image1.jpg va image2.jpg!")
