import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

# Biến toàn cục lưu ảnh
img1_orig = None
img2_orig = None
path1 = ""
path2 = ""

# --- CHỨC NĂNG 1: CHỌN ẢNH ---
def select_image1():
    global img1_orig, path1
    path = filedialog.askopenfilename(
        title="Chọn Ảnh 1",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.webp")]
    )
    if path:
        path1 = path
        img1_orig = cv2.imread(path)
        if img1_orig is not None:
            lbl_img1.config(text=f"Ảnh 1: {path1.split('/')[-1]}", fg="green")
        else:
            messagebox.showerror("Lỗi", "Không thể đọc Ảnh 1")

def select_image2():
    global img2_orig, path2
    path = filedialog.askopenfilename(
        title="Chọn Ảnh 2",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.webp")]
    )
    if path:
        path2 = path
        img2_orig = cv2.imread(path)
        if img2_orig is not None:
            lbl_img2.config(text=f"Ảnh 2: {path2.split('/')[-1]}", fg="green")
        else:
            messagebox.showerror("Lỗi", "Không thể đọc Ảnh 2")

# --- CHỨC NĂNG 2: BẢNG TỔNG HỢP 3x3 (Gốc, Gray, HSV, Bitwise AND) ---
def process_and_show_3x3():
    global img1_orig, img2_orig
    
    if img1_orig is None or img2_orig is None:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn đủ cả 2 ảnh trước!")
        return

    w, h = 280, 280
    img1 = cv2.resize(img1_orig, (w, h))
    img2 = cv2.resize(img2_orig, (w, h))

    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img1_gray_3ch = cv2.cvtColor(img1_gray, cv2.COLOR_GRAY2BGR)
    img1_hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img2_gray_3ch = cv2.cvtColor(img2_gray, cv2.COLOR_GRAY2BGR)
    img2_hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)

    img_and = cv2.bitwise_and(img1, img2)
    blank_tile = np.zeros((h, w, 3), dtype=np.uint8)

    cv2.putText(img1, "1. Anh 1 (Goc)", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.putText(img1_gray_3ch, "2. Anh 1 (GrayScale)", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.putText(img1_hsv, "3. Anh 1 (HSV)", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.putText(img2, "4. Anh 2 (Goc)", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.putText(img2_gray_3ch, "5. Anh 2 (GrayScale)", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.putText(img2_hsv, "6. Anh 2 (HSV)", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.putText(img_and, "7. Bitwise AND (1 & 2)", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

    row1 = np.hstack((img1, img1_gray_3ch, img1_hsv))
    row2 = np.hstack((img2, img2_gray_3ch, img2_hsv))
    row3 = np.hstack((blank_tile, img_and, blank_tile))

    combined_frame = np.vstack((row1, row2, row3))
    cv2.imshow("Khung Tong Hop 3x3: Anh 1, Anh 2 & Bitwise AND", combined_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# --- CHỨC NĂNG 3: LƯU ĐA ĐỊNH DẠNG ---
def save_image_multiple_formats():
    global img1_orig, path1
    if img1_orig is None:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn Ảnh 1 trước khi lưu!")
        return

    save_dir = filedialog.askdirectory(title="Chọn thư mục để lưu ảnh")
    if save_dir:
        base_name = os.path.splitext(os.path.basename(path1))[0]
        cv2.imwrite(os.path.join(save_dir, f"{base_name}_converted.png"), img1_orig)
        cv2.imwrite(os.path.join(save_dir, f"{base_name}_converted.jpg"), img1_orig, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
        cv2.imwrite(os.path.join(save_dir, f"{base_name}_converted.bmp"), img1_orig)
        messagebox.showinfo("Thành công", f"Đã lưu thành công 3 định dạng PNG, JPEG, BMP tại:\n{save_dir}")

# --- BÀI TẬP 5: TĂNG CƯỜNG ĐỘ SÁNG ---
def increase_brightness():
    global img1_orig
    if img1_orig is None:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn Ảnh 1 trước!")
        return

    value = 50
    M = np.ones(img1_orig.shape, dtype="uint8") * value
    img_bright = cv2.add(img1_orig, M)

    h, w = 350, 350
    orig_res = cv2.resize(img1_orig, (w, h))
    bright_res = cv2.resize(img_bright, (w, h))

    cv2.putText(orig_res, "Goc (Original)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(bright_res, f"Tang Do Sang (+{value})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    combined = np.hstack((orig_res, bright_res))
    cv2.imshow("Bai Tap 5: Tang Cuong Do Sang", combined)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# --- BÀI TẬP 6: PHÉP BIẾN ĐỔI HÌNH HỌC (CẢI TIẾN KHÔNG BỂ ẢNH) ---
def geometric_transformations():
    global img1_orig
    if img1_orig is None:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn Ảnh 1 trước!")
        return

    # 1. Xoay ảnh 90 độ
    img_rotated = cv2.rotate(img1_orig, cv2.ROTATE_90_CLOCKWISE)

    # 2. Dịch chuyển ảnh sang phải 50 pixel
    h_orig, w_orig = img1_orig.shape[:2]
    M_translation = np.float32([[1, 0, 50], [0, 1, 0]])
    img_translated = cv2.warpAffine(img1_orig, M_translation, (w_orig, h_orig))

    # 3. Phóng to 1.5 lần sử dụng cv2.INTER_CUBIC kết hợp cv2.detailEnhance để giữ chi tiết sắc nét, không bị vỡ ảnh
    img_scaled = cv2.resize(img1_orig, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    img_scaled = cv2.detailEnhance(img_scaled, sigma_s=10, sigma_r=0.15)

    w, h = 300, 300
    res_orig = cv2.resize(img1_orig, (w, h))
    res_rot = cv2.resize(img_rotated, (w, h))
    res_trans = cv2.resize(img_translated, (w, h))
    res_scale = cv2.resize(img_scaled, (w, h))

    cv2.putText(res_orig, "Goc", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(res_rot, "Xoay 90 Do", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(res_trans, "Dich Sang Phai 50px", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(res_scale, "Phong To 1.5x (Sac Net)", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    row1 = np.hstack((res_orig, res_rot))
    row2 = np.hstack((res_trans, res_scale))
    combined = np.vstack((row1, row2))

    cv2.imshow("Bai Tap 6: Phep Bien Doi Hinh Hoc", combined)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# --- GIAO DIỆN TKINTER ---
root = tk.Tk()
root.title("Chương trình Xử lý & Biến đổi Ảnh - OpenCV")
root.geometry("460x420")
root.resizable(False, False)

lbl_title = tk.Label(root, text="CHƯƠNG TRÌNH XỬ LÝ ẢNH TỔNG HỢP", font=("Arial", 12, "bold"))
lbl_title.pack(pady=10)

btn_img1 = tk.Button(root, text="1. Chọn Ảnh 1 (Ảnh chính)", font=("Arial", 10), command=select_image1, width=32)
btn_img1.pack(pady=3)
lbl_img1 = tk.Label(root, text="Ảnh 1: Chưa chọn", font=("Arial", 9, "italic"), fg="gray")
lbl_img1.pack(pady=2)

btn_img2 = tk.Button(root, text="2. Chọn Ảnh 2 (Dùng cho Bitwise)", font=("Arial", 10), command=select_image2, width=32)
btn_img2.pack(pady=3)
lbl_img2 = tk.Label(root, text="Ảnh 2: Chưa chọn", font=("Arial", 9, "italic"), fg="gray")
lbl_img2.pack(pady=2)

btn_run_3x3 = tk.Button(root, text="3. Xem Khung 3x3 (Gray, HSV, Bitwise)", font=("Arial", 10, "bold"), command=process_and_show_3x3, bg="#4CAF50", fg="white", width=35)
btn_run_3x3.pack(pady=5)

btn_save = tk.Button(root, text="4. Lưu Ảnh 1 Sang (PNG, JPEG, BMP)", font=("Arial", 10, "bold"), command=save_image_multiple_formats, bg="#2196F3", fg="white", width=35)
btn_save.pack(pady=5)

btn_bright = tk.Button(root, text="5. Bài 5: Tăng Độ Sáng (+50)", font=("Arial", 10, "bold"), command=increase_brightness, bg="#FF9800", fg="white", width=35)
btn_bright.pack(pady=5)

btn_geom = tk.Button(root, text="6. Bài 6: Biến Đổi Hình Học (Xoay, Dịch, Phóng)", font=("Arial", 10, "bold"), command=geometric_transformations, bg="#9C27B0", fg="white", width=35)
btn_geom.pack(pady=5)

root.mainloop()